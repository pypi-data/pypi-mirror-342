from __future__ import annotations

import base64
import enum
import logging
import sys
import threading
import uuid
from types import TracebackType
from typing import Any
from typing import get_args
from typing import TypeVar

if sys.version_info >= (3, 11):  # pragma: >=3.11 cover
    from typing import Self
else:  # pragma: <3.11 cover
    from typing_extensions import Self

import redis

from academy.behavior import Behavior
from academy.exception import BadEntityIdError
from academy.exception import MailboxClosedError
from academy.exchange import ExchangeMixin
from academy.exchange.queue import Queue
from academy.exchange.queue import QueueClosedError
from academy.identifier import AgentId
from academy.identifier import ClientId
from academy.identifier import EntityId
from academy.message import BaseMessage
from academy.message import Message
from academy.serialize import NoPickleMixin
from academy.socket import address_by_hostname
from academy.socket import address_by_interface
from academy.socket import SimpleSocket
from academy.socket import SimpleSocketServer
from academy.socket import SocketClosedError

logger = logging.getLogger(__name__)

BehaviorT = TypeVar('BehaviorT', bound=Behavior)

_CLOSE_SENTINEL = b'<CLOSED>'
_THREAD_START_TIMEOUT = 5
_THREAD_JOIN_TIMEOUT = 5
_SERVER_ACK = b'<ACK>'
_SOCKET_POLL_TIMEOUT_MS = 50


class _MailboxState(enum.Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'


class HybridExchange(ExchangeMixin):
    """Hybrid exchange.

    The hybrid exchange uses peer-to-peer communication via TCP and a
    central Redis server for mailbox state and queueing messages for
    offline entities.

    Args:
        redis_host: Redis server hostname.
        redis_port: Redis server port.
        interface: Network interface use for peer-to-peer communication. If
            `None`, the hostname of the local host is used.
        namespace: Redis key namespace. If `None` a random key prefix is
            generated.
        redis_kwargs: Extra keyword arguments to pass to
            [`redis.Redis()`][redis.Redis].

    Raises:
        redis.exceptions.ConnectionError: If the Redis server is not reachable.
    """

    _address_cache: dict[EntityId, str]
    _redis_client: redis.Redis
    _socket_pool: _SocketPool

    def __init__(
        self,
        redis_host: str,
        redis_port: int,
        *,
        interface: str | None = None,
        namespace: str | None = 'default',
        redis_kwargs: dict[str, Any] | None = None,
    ) -> None:
        self._namespace = (
            namespace
            if namespace is not None
            else uuid_to_base32(uuid.uuid4())
        )
        self._interface = interface
        self._redis_host = redis_host
        self._redis_port = redis_port
        self._redis_kwargs = redis_kwargs if redis_kwargs is not None else {}

        self._init_connections()

    def _init_connections(self) -> None:
        self._address_cache = {}
        self._redis_client = redis.Redis(
            host=self._redis_host,
            port=self._redis_port,
            decode_responses=False,
            **self._redis_kwargs,
        )
        self._redis_client.ping()
        self._socket_pool = _SocketPool()

    def __getstate__(self) -> dict[str, Any]:
        return {
            '_redis_host': self._redis_host,
            '_redis_port': self._redis_port,
            '_redis_kwargs': self._redis_kwargs,
            '_interface': self._interface,
            '_namespace': self._namespace,
        }

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__dict__.update(state)
        self._init_connections()

    def __repr__(self) -> str:
        redis_addr = f'{self._redis_host}:{self._redis_port}'
        return (
            f'{type(self).__name__}(namespace={self._namespace}, '
            f'redis={redis_addr})'
        )

    def __str__(self) -> str:
        redis_addr = f'{self._redis_host}:{self._redis_port}'
        return f'{type(self).__name__}<{redis_addr}; {self._namespace}>'

    def _address_key(self, uid: EntityId) -> str:
        return f'{self._namespace}:address:{uuid_to_base32(uid.uid)}'

    def _behavior_key(self, aid: AgentId[Any]) -> str:
        return f'{self._namespace}:behavior:{uuid_to_base32(aid.uid)}'

    def _status_key(self, uid: EntityId) -> str:
        return f'{self._namespace}:status:{uuid_to_base32(uid.uid)}'

    def _queue_key(self, uid: EntityId) -> str:
        return f'{self._namespace}:queue:{uuid_to_base32(uid.uid)}'

    def close(self) -> None:
        """Close the exchange interface."""
        self._redis_client.close()
        self._socket_pool.close()
        logger.debug('Closed exchange (%s)', self)

    def register_agent(
        self,
        behavior: type[BehaviorT],
        *,
        agent_id: AgentId[BehaviorT] | None = None,
        name: str | None = None,
    ) -> AgentId[BehaviorT]:
        """Create a new agent identifier and associated mailbox.

        Args:
            behavior: Type of the behavior this agent will implement.
            agent_id: Specify the ID of the agent. Randomly generated
                default.
            name: Optional human-readable name for the agent. Ignored if
                `agent_id` is provided.

        Returns:
            Unique identifier for the agent's mailbox.
        """
        aid = AgentId.new(name=name) if agent_id is None else agent_id
        self._redis_client.set(
            self._status_key(aid),
            _MailboxState.ACTIVE.value,
        )
        self._redis_client.set(
            self._behavior_key(aid),
            ','.join(behavior.behavior_mro()),
        )
        logger.debug('Registered %s in %s', aid, self)
        return aid

    def register_client(
        self,
        *,
        name: str | None = None,
    ) -> ClientId:
        """Create a new client identifier and associated mailbox.

        Args:
            name: Optional human-readable name for the client.

        Returns:
            Unique identifier for the client's mailbox.
        """
        cid = ClientId.new(name=name)
        self._redis_client.set(
            self._status_key(cid),
            _MailboxState.ACTIVE.value,
        )
        logger.debug('Registered %s in %s', cid, self)
        return cid

    def terminate(self, uid: EntityId) -> None:
        """Close the mailbox for an entity from the exchange.

        This sets the state of the mailbox to inactive in the Redis server,
        and deletes any queued messages in Redis.

        Args:
            uid: Entity identifier of the mailbox to close.
        """
        self._redis_client.set(
            self._status_key(uid),
            _MailboxState.INACTIVE.value,
        )
        # Sending a close sentinel to the queue is a quick way to force
        # the entity waiting on messages to the mailbox to stop blocking.
        # This assumes that only one entity is reading from the mailbox.
        self._redis_client.rpush(self._queue_key(uid), _CLOSE_SENTINEL)
        if isinstance(uid, AgentId):
            self._redis_client.delete(self._behavior_key(uid))
        logger.debug('Closed mailbox for %s (%s)', uid, self)

    def discover(
        self,
        behavior: type[Behavior],
        *,
        allow_subclasses: bool = True,
    ) -> tuple[AgentId[Any], ...]:
        """Discover peer agents with a given behavior.

        Warning:
            This method is O(n) and scans all keys in the Redis server.

        Args:
            behavior: Behavior type of interest.
            allow_subclasses: Return agents implementing subclasses of the
                behavior.

        Returns:
            Tuple of agent IDs implementing the behavior.
        """
        found: list[AgentId[Any]] = []
        fqp = f'{behavior.__module__}.{behavior.__name__}'
        for key in self._redis_client.scan_iter(
            f'{self._namespace}:behavior:*',
        ):
            mro_str = self._redis_client.get(key)
            assert isinstance(mro_str, str)
            mro = mro_str.split(',')
            if fqp == mro[0] or (allow_subclasses and fqp in mro):
                aid: AgentId[Any] = AgentId(
                    uid=base32_to_uuid(key.split(':')[-1]),
                )
                found.append(aid)
        active: list[AgentId[Any]] = []
        for aid in found:
            status = self._redis_client.get(self._status_key(aid))
            if status == _MailboxState.ACTIVE.value:  # pragma: no branch
                active.append(aid)
        return tuple(active)

    def get_mailbox(self, uid: EntityId) -> HybridMailbox:
        """Get a client to a specific mailbox.

        Args:
            uid: EntityId of the mailbox.

        Returns:
            Mailbox client.

        Raises:
            BadEntityIdError: if a mailbox for `uid` does not exist.
        """
        status = self._redis_client.get(self._status_key(uid))
        if status is None:
            raise BadEntityIdError(uid)
        return HybridMailbox(uid, self, interface=self._interface)

    def _send_direct(self, address: str, message: Message) -> None:
        self._socket_pool.send(address, message.model_serialize())
        logger.debug(
            'Sent %s to %s via p2p at %s',
            type(message).__name__,
            message.dest,
            address,
        )

    def send(self, uid: EntityId, message: Message) -> None:
        """Send a message to a mailbox.

        To send a message, the client first checks that the state of the
        mailbox in Redis is active; otherwise, an error is raised. Then,
        the client checks to see if the peer entity is available by
        checking for an address of the peer in Redis. If the peer's address
        is found, the message is sent directly to the peer via ZMQ; otherwise,
        the message is put in a Redis queue for later retrieval.

        Args:
            uid: Destination address of the message.
            message: Message to send.

        Raises:
            BadEntityIdError: if a mailbox for `uid` does not exist.
            MailboxClosedError: if the mailbox was closed.
        """
        address = self._address_cache.get(uid, None)
        if address is not None:
            try:
                # This is as optimistic as possible. If the address of the
                # peer is cached, we assume the mailbox is still active and
                # the peer is still listening.
                self._send_direct(address, message)
            except (SocketClosedError, OSError):
                # Our optimism let us down so clear the cache and try the
                # standard flow.
                self._address_cache.pop(uid)
            else:
                return

        status = self._redis_client.get(self._status_key(uid))
        if status is None:
            raise BadEntityIdError(uid)
        elif status == _MailboxState.INACTIVE.value:
            raise MailboxClosedError(uid)

        maybe_address = self._redis_client.get(self._address_key(uid))
        try:
            # This branching is a little odd. We want to fall back to
            # Redis for message sending on two conditions: direct send fails
            # or no address was found. We raise a TypeError if no address
            # was found as a shortcut to get to the fall back.
            if isinstance(maybe_address, (bytes, str)):
                decoded_address = (
                    maybe_address.decode('utf-8')
                    if isinstance(maybe_address, bytes)
                    else maybe_address
                )
                self._send_direct(decoded_address, message)
                self._address_cache[uid] = decoded_address
            else:
                raise TypeError('Did not active peer address in Redis.')
        except (TypeError, SocketClosedError, OSError):
            self._redis_client.rpush(
                self._queue_key(uid),
                message.model_serialize(),
            )
            logger.debug(
                'Sent %s to %s via redis',
                type(message).__name__,
                uid,
            )


class _SocketPool:
    def __init__(self) -> None:
        self._sockets: dict[str, SimpleSocket] = {}

    def close(self) -> None:
        for address in tuple(self._sockets.keys()):
            self.close_socket(address)

    def close_socket(self, address: str) -> None:
        conn = self._sockets.pop(address, None)
        if conn is not None:  # pragma: no branch
            conn.close(shutdown=True)

    def get_socket(self, address: str) -> SimpleSocket:
        try:
            return self._sockets[address]
        except KeyError:
            parts = address.split(':')
            host, port = parts[0], int(parts[1])
            conn = SimpleSocket(host, port)
            self._sockets[address] = conn
            return conn

    def send(self, address: str, message: bytes) -> None:
        conn = self.get_socket(address)
        try:
            conn.send(message)
        except (SocketClosedError, OSError):
            self.close_socket(address)
            raise


class HybridMailbox(NoPickleMixin):
    """Client protocol that listens to incoming messages to a mailbox.

    This class acts as the endpoint for messages sent to a particular
    mailbox. This is done via starting two threads once initialized:
    (1) a ZMQ server thread that listens for messages from peers, and
    (2) a thread that checks the Redis server for any offline messages and
    state changes to the mailbox (i.e., mailbox closure).

    Args:
        uid: EntityId of the mailbox.
        exchange: Exchange client.
        interface: Network interface use for peer-to-peer communication. If
            `None`, the hostname of the local host is used.
        port: Port to use for peer-to-peer communication. Randomly selected
            if `None`.
    """

    def __init__(
        self,
        uid: EntityId,
        exchange: HybridExchange,
        *,
        interface: str | None = None,
        port: int | None = None,
    ) -> None:
        self._uid = uid
        self._exchange = exchange
        self._interface = interface
        self._messages: Queue[Message] = Queue()

        self._closed = threading.Event()
        self._socket_poll_timeout_ms = _SOCKET_POLL_TIMEOUT_MS

        host = (
            address_by_interface(interface)
            if interface is not None
            else address_by_hostname()
        )
        self._server = SimpleSocketServer(
            handler=self._server_handler,
            host=host,
            port=port,
            timeout=_THREAD_JOIN_TIMEOUT,
        )
        self._server.start_server_thread()

        self.exchange._redis_client.set(
            self.exchange._address_key(uid),
            f'{self._server.host}:{self._server.port}',
        )

        self._redis_thread = threading.Thread(
            target=self._redis_watcher,
            name=f'hybrid-mailbox-redis-watcher-{uid}',
        )
        self._redis_started = threading.Event()
        self._redis_thread.start()
        self._redis_started.wait(timeout=_THREAD_START_TIMEOUT)

    @property
    def exchange(self) -> HybridExchange:
        """Exchange client."""
        return self._exchange

    @property
    def mailbox_id(self) -> EntityId:
        """Mailbox address/identifier."""
        return self._uid

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_traceback: TracebackType | None,
    ) -> None:
        self.close()

    def _pull_messages_from_redis(self, timeout: int = 1) -> None:
        # Note: we use blpop instead of lpop here for the timeout.
        raw = self.exchange._redis_client.blpop(
            [self.exchange._queue_key(self.mailbox_id)],
            timeout=timeout,
        )
        if raw is None:
            return

        # Only passed one key to blpop to result is [key, item]
        assert isinstance(raw, (tuple, list))
        assert len(raw) == 2  # noqa: PLR2004
        if raw[1] == _CLOSE_SENTINEL:  # pragma: no cover
            raise MailboxClosedError(self.mailbox_id)
        message = BaseMessage.model_deserialize(raw[1])
        assert isinstance(message, get_args(Message))
        logger.debug(
            'Received %s to %s via redis',
            type(message).__name__,
            self.mailbox_id,
        )
        self._messages.put(message)

    def _redis_watcher(self) -> None:
        self._redis_started.set()
        logger.debug('Started redis watcher thread for %s', self.mailbox_id)
        try:
            while not self._closed.is_set():
                status = self.exchange._redis_client.get(
                    self.exchange._status_key(self.mailbox_id),
                )
                if status is None:  # pragma: no cover
                    raise AssertionError(
                        f'Status for mailbox {self.mailbox_id} did not exist '
                        'in Redis server. This means that something '
                        'incorrectly deleted the key.',
                    )
                elif (
                    status == _MailboxState.INACTIVE.value
                ):  # pragma: no cover
                    self._messages.close()
                    break

                self._pull_messages_from_redis(timeout=1)
        except MailboxClosedError:  # pragma: no cover
            pass
        except Exception:
            logger.exception(
                'Error in redis watcher thread for %s',
                self.mailbox_id,
            )
        finally:
            self._server.stop_server_thread()
            self._messages.close()
            logger.debug(
                'Stopped redis watcher thread for %s',
                self.mailbox_id,
            )

    def _server_handler(self, payload: bytes) -> bytes | None:
        message = BaseMessage.model_deserialize(payload)
        logger.debug(
            'Received %s to %s via p2p',
            type(message).__name__,
            self.mailbox_id,
        )
        self._messages.put(message)
        return None

    def close(self) -> None:
        """Close this mailbox client.

        Warning:
            This does not close the mailbox in the exchange. I.e., the exchange
            will still accept new messages to this mailbox, but this client
            will no longer be listening for them.
        """
        self._closed.set()
        self.exchange._redis_client.delete(
            self.exchange._address_key(self.mailbox_id),
        )

        self._server.stop_server_thread()

        self._redis_thread.join(_THREAD_JOIN_TIMEOUT)
        if self._redis_thread.is_alive():  # pragma: no cover
            raise TimeoutError(
                'Redis watcher thread failed to exit within '
                f'{_THREAD_JOIN_TIMEOUT} seconds.',
            )

        self._messages.close()

    def recv(self, timeout: float | None = None) -> Message:
        """Receive the next message in the mailbox.

        This blocks until the next message is received or the mailbox
        is closed.

        Args:
            timeout: Optional timeout in seconds to wait for the next
                message. If `None`, the default, block forever until the
                next message or the mailbox is closed. Note that this will
                be cast to an int which is required by the Redis API.

        Raises:
            MailboxClosedError: if the mailbox was closed.
            TimeoutError: if a `timeout` was specified and exceeded.
        """
        try:
            return self._messages.get(timeout=timeout)
        except QueueClosedError:
            raise MailboxClosedError(self.mailbox_id) from None


def base32_to_uuid(uid: str) -> uuid.UUID:
    """Parse a base32 string as a UUID."""
    padding = '=' * ((8 - len(uid) % 8) % 8)
    padded = uid + padding
    uid_bytes = base64.b32decode(padded)
    return uuid.UUID(bytes=uid_bytes)


def uuid_to_base32(uid: uuid.UUID) -> str:
    """Encode a UUID as a trimmed base32 string."""
    uid_bytes = uid.bytes
    base32_bytes = base64.b32encode(uid_bytes).rstrip(b'=')
    return base32_bytes.decode('utf-8')
