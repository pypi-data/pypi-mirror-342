import threading
from typing import Callable, Dict, Optional, TypeVar, Generic
from typing import Type
from typing import Union

import zenoh
from google.protobuf.message import Message

from make87.session import get_session
from make87.utils import parse_endpoints, REQ, PRV, IS_IN_RELEASE_MODE, RingChannel, FifoChannel

T_REQ = TypeVar("T_REQ", bound=Optional[Message])
T_RES = TypeVar("T_RES", bound=Optional[Message])


class ProviderNotAvailable(Exception): ...


class ResponseTimeout(Exception): ...


class Endpoint:
    """Base class for endpoints."""

    def __init__(self, name: str):
        self.name = name


class TypedProvider(Generic[T_REQ, T_RES]):
    """A typed publisher endpoint that publishes messages of type `T`."""

    def __init__(self, inner: "Provider", request_message_type: Type[T_REQ], response_message_type: Type[T_RES]):
        self._inner = inner
        self._request_message_type = request_message_type
        self._response_message_type = response_message_type

    def provide(self, callback: Callable[[T_REQ], T_RES]) -> None:
        """Subscribe to the topic with a callback that expects messages of type `T`."""

        def _decode_message(query: zenoh.Query):
            request_message = None
            if self._request_message_type is not None:
                request_message = self._request_message_type()
                try:
                    request_message.ParseFromString(query.payload.to_bytes())
                except Exception as e:
                    raise Exception(f"Failed to decode message on endpoint '{self._inner.name}': {e}")

            response_message = callback(request_message)

            encoded_message = b""
            if self._response_message_type is not None:
                encoded_message = response_message.SerializeToString()

            query.reply(
                key_expr=query.key_expr,
                payload=zenoh.ZBytes(encoded_message),
                encoding=zenoh.Encoding.APPLICATION_PROTOBUF,
                priority=zenoh.Priority.REAL_TIME,
                express=True,
                congestion_control=zenoh.CongestionControl.BLOCK,
            )

        self._inner.provide(_decode_message)


class Provider(Endpoint):
    """An endpoint used for providing data to an incoming request."""

    def __init__(
        self,
        name: str,
        session: zenoh.Session,
        handler_type: Union[Type[zenoh.handlers.RingChannel], Type[zenoh.handlers.FifoChannel]] = None,
        handler_capacity: int = None,
    ):
        super().__init__(name)
        self._session = session
        # TODO: Implement handler-based provider
        self._handler_type = zenoh.handlers.FifoChannel if handler_type is None else handler_type
        self._handler_capacity = 100 if handler_capacity is None else handler_capacity

        self._queryable: Optional[zenoh.Queryable] = None
        self._token: Optional[zenoh.LivelinessToken] = None

    def provide(self, callback: Callable[[zenoh.Query], None]) -> None:
        self._queryable = self._session.declare_queryable(self.name, handler=callback)
        self._token = self._session.liveliness().declare_token(self.name)


class TypedRequester(Generic[T_REQ, T_RES]):
    """A typed subscriber endpoint that provides messages of type `T`."""

    def __init__(self, inner: "Requester", request_message_type: Type[T_REQ], response_message_type: Type[T_RES]):
        self._inner = inner
        self._request_message_type = request_message_type
        self._response_message_type = response_message_type

    def request(self, message: T_REQ, timeout: float = 10.0) -> T_RES:
        """Receive a message from the endpoint."""

        encoded_message = b""
        if self._request_message_type is not None:
            encoded_message = message.SerializeToString()

        response_bytes = self._inner.request(zenoh.ZBytes(encoded_message), timeout=timeout)
        if self._response_message_type is None:
            return None

        response_message = self._response_message_type()
        response_message.ParseFromString(response_bytes.to_bytes())
        return response_message


class Requester(Endpoint):
    """An endpoint used for requesting data from a provider."""

    def __init__(
        self,
        name: str,
        session: zenoh.Session,
        congestion_control: zenoh.CongestionControl = None,
        priority: zenoh.Priority = None,
        express: bool = None,
    ):
        super().__init__(name)
        self._session = session
        self._congestion_control = zenoh.CongestionControl.BLOCK if congestion_control is None else congestion_control
        self._priority = zenoh.Priority.DEFAULT if priority is None else priority
        self._express = True if express is None else express

    def request(self, message: zenoh.ZBytes, timeout: float = 10.0) -> zenoh.ZBytes:
        reply = self._session.get(
            selector=self.name,
            payload=message,
            encoding=zenoh.Encoding.APPLICATION_PROTOBUF,
            priority=self._priority,
            express=self._express,
            congestion_control=self._congestion_control,
            timeout=timeout,
        )

        try:
            reply = reply.recv()
        except zenoh.ZError as e:
            if all(token in str(e).upper() for token in ("CHANNEL", "CLOSED")):
                raise ProviderNotAvailable(f"Endpoint '{self.name}' is not available.")
            else:
                raise Exception(f"Error while requesting endpoint '{self.name}': {e}")

        if reply.ok is not None:
            return reply.ok.payload
        elif reply.err is not None:
            if bytes(reply.err.payload).decode("utf-8").strip().upper() == "TIMEOUT":
                raise ResponseTimeout(
                    f"Waited {timeout}s for response until timed out. Consider increasing your timeout or checking with the provider side."
                )
            else:
                raise Exception(
                    f"Error returned while requesting endpoint '{self.name}': {reply.err.payload.to_string()}"
                )


class _EndpointManager:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self._endpoints: Dict[str, Union[Provider, Requester]] = {}
        self._endpoint_names: Dict[str, str] = {}
        self._initialized: bool = False

    @classmethod
    def get_instance(cls):
        """Singleton pattern to ensure only one instance exists."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def initialize(self):
        """Initialize endpoints based on the ENDPOINTS environment variable."""
        with self._lock:
            if self._initialized:
                return  # Already initialized

            session = get_session()

            endpoint_data = parse_endpoints()

            for endpoint in endpoint_data.endpoints:
                if endpoint.endpoint_key in self._endpoints:
                    continue  # Endpoint already initialized
                if isinstance(endpoint, REQ):
                    endpoint_type = Requester(
                        name=endpoint.endpoint_key,
                        session=session,
                        priority=endpoint.priority.to_zenoh(),
                        congestion_control=endpoint.congestion_control.to_zenoh(),
                        express=endpoint.express,
                    )
                elif isinstance(endpoint, PRV):
                    if isinstance(endpoint.handler, RingChannel):
                        handler_type = zenoh.handlers.RingChannel
                    elif isinstance(endpoint.handler, FifoChannel):
                        handler_type = zenoh.handlers.FifoChannel
                    else:
                        raise ValueError(f"Invalid handler type {endpoint.handler.handler_type}")

                    handler_capacity = endpoint.handler.capacity

                    endpoint_type = Provider(
                        name=endpoint.endpoint_key,
                        session=session,
                        handler_type=handler_type,
                        handler_capacity=handler_capacity,
                    )
                else:
                    raise ValueError(f"Invalid endpoint type {endpoint.endpoint_type}")
                self._endpoints[endpoint.endpoint_key] = endpoint_type
                self._endpoint_names[endpoint.endpoint_name] = endpoint.endpoint_key

            self._initialized = True

    def _get_untyped_endpoint(self, name: str) -> Union[Provider, Requester]:
        """Retrieve an endpoint by name."""
        if not self._initialized:
            raise RuntimeError("SessionManager not initialized. Call initialize() first.")
        if name not in self._endpoints:
            available_endpoints = ", ".join(self._endpoints.keys())
            raise ValueError(f"Endpoint '{name}' not found. Available endpoints: {available_endpoints}")
        return self._endpoints[name]

    def get_provider_endpoint(
        self, name: str, request_message_type: Type[T_REQ] = None, response_message_type: Type[T_RES] = None
    ) -> TypedProvider[T_REQ, T_RES]:
        """Retrieve a provider endpoint by name."""
        name = self.resolve_endpoint_name(name)
        try:
            endpoint = self._get_untyped_endpoint(name=name)
        except ValueError as e:
            if IS_IN_RELEASE_MODE:
                raise e
            endpoint = Provider(name=name, session=get_session())
            return TypedProvider(
                inner=endpoint, request_message_type=request_message_type, response_message_type=response_message_type
            )
        if not isinstance(endpoint, Provider):
            raise ValueError(f"Endpoint '{name}' is not a provide endpoint.")
        return TypedProvider(
            inner=endpoint, request_message_type=request_message_type, response_message_type=response_message_type
        )

    def get_requester_endpoint(
        self, name: str, request_message_type: Type[T_REQ] = None, response_message_type: Type[T_RES] = None
    ) -> TypedRequester[T_REQ, T_RES]:
        """Retrieve a requester endpoint by name."""
        name = self.resolve_endpoint_name(name)
        try:
            endpoint = self._get_untyped_endpoint(name=name)
        except ValueError as e:
            if IS_IN_RELEASE_MODE:
                raise e
            endpoint = Requester(name=name, session=get_session())
            return TypedRequester(
                inner=endpoint, request_message_type=request_message_type, response_message_type=response_message_type
            )
        if not isinstance(endpoint, Requester):
            raise ValueError(f"Endpoint '{name}' is not a request endpoint.")
        return TypedRequester(
            inner=endpoint, request_message_type=request_message_type, response_message_type=response_message_type
        )

    def resolve_endpoint_name(self, name: str) -> str:
        """Resolve a endpoint name to a endpoint key."""
        if not self._initialized:
            raise RuntimeError("SessionManager not initialized. Call initialize() first.")
        if name not in self._endpoint_names:
            if IS_IN_RELEASE_MODE:
                raise ValueError(f"Endpoint name '{name}' not found.")
            else:
                return name
        return self._endpoint_names[name]


def get_provider(
    name: str, requester_message_type: Type[T_REQ] = None, provider_message_type: Type[T_RES] = None
) -> TypedProvider[T_REQ, T_RES]:
    """Retrieve a publisher endpoint by name.

    Args:
        name: The name of the endpoint to retrieve used in the `MAKE87.yml` file.
        requester_message_type: The type of message that's send to the endpoint.
        provider_message_type: The type of message that's received from the endpoint.

    Returns:
        The publisher endpoint object.

    Raises:
        RuntimeError: If the make87 library has not been initialized correctly. Call `make87.initialize()`.
        ValueError: If the endpoint is not found.
        ValueError: If the endpoint is not a publisher endpoint.

    """
    return _EndpointManager.get_instance().get_provider_endpoint(
        name=name, request_message_type=requester_message_type, response_message_type=provider_message_type
    )


def get_requester(
    name: str, requester_message_type: Type[T_REQ] = None, provider_message_type: Type[T_RES] = None
) -> TypedRequester[T_REQ, T_RES]:
    """Retrieve a subscriber endpoint by name.

    Args:
        name: The name of the endpoint to retrieve used in the `MAKE87.yml` file.
        requester_message_type: The type of message that's send to the endpoint.
        provider_message_type: The type of message that's received from the endpoint.

    Returns:
        The subscriber endpoint object.

    Raises:
        RuntimeError: If the make87 library has not been initialized correctly. Call `make87.initialize()`.
        ValueError: If the endpoint is not found.
        ValueError: If the endpoint is not a subscriber endpoint.
    """
    return _EndpointManager.get_instance().get_requester_endpoint(
        name=name, request_message_type=requester_message_type, response_message_type=provider_message_type
    )


def resolve_endpoint_name(name: str) -> str:
    """Resolve a endpoint name to its dynamic endpoint key.

    Args:
        name: Name of the endpoint used in the `MAKE87.yml` file.

    Returns:
        The dynamic endpoint key used to reference the endpoint.

    Raises:
        RuntimeError: If the make87 library has not been initialized correctly. Call `make87.initialize()`.
        ValueError: If the endpoint name is not found.
    """
    return _EndpointManager.get_instance().resolve_endpoint_name(name)
