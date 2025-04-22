from __future__ import annotations

import enum
import logging
import uuid
from typing import Any
from typing import get_args
from typing import TypeVar

import redis

from academy.behavior import Behavior
from academy.exception import BadEntityIdError
from academy.exception import MailboxClosedError
from academy.exchange import ExchangeMixin
from academy.identifier import AgentId
from academy.identifier import ClientId
from academy.identifier import EntityId
from academy.message import BaseMessage
from academy.message import Message
from academy.serialize import NoPickleMixin

logger = logging.getLogger(__name__)

BehaviorT = TypeVar('BehaviorT', bound=Behavior)

_CLOSE_SENTINEL = b'<CLOSED>'


class _MailboxState(enum.Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'


class RedisExchange(ExchangeMixin):
    """Redis-hosted message exchange interface.

    Args:
        hostname: Redis server hostname.
        port: Redis server port.
        kwargs: Extra keyword arguments to pass to
            [`redis.Redis()`][redis.Redis].
        timeout: Timeout for waiting on the next message. If `None`, the
            timeout will be set to one second but will loop indefinitely.

    Raises:
        redis.exceptions.ConnectionError: If the Redis server is not reachable.
    """

    def __init__(
        self,
        hostname: str,
        port: int,
        *,
        timeout: int | None = None,
        **kwargs: Any,
    ) -> None:
        self.hostname = hostname
        self.port = port
        self.timeout = timeout
        self._kwargs = kwargs
        self._client = redis.Redis(
            host=hostname,
            port=port,
            decode_responses=False,
            **kwargs,
        )
        self._client.ping()

    def __getstate__(self) -> dict[str, Any]:
        return {
            'hostname': self.hostname,
            'port': self.port,
            'timeout': self.timeout,
            '_kwargs': self._kwargs,
        }

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__dict__.update(state)
        self._client = redis.Redis(
            host=self.hostname,
            port=self.port,
            decode_responses=False,
            **self._kwargs,
        )

    def __repr__(self) -> str:
        return (
            f'{type(self).__name__}(hostname={self.hostname}, '
            f'port={self.port}, timeout={self.timeout})'
        )

    def __str__(self) -> str:
        return f'{type(self).__name__}<{self.hostname}:{self.port}>'

    def _active_key(self, uid: EntityId) -> str:
        return f'active:{uid.uid}'

    def _behavior_key(self, uid: AgentId[Any]) -> str:
        return f'behavior:{uid.uid}'

    def _queue_key(self, uid: EntityId) -> str:
        return f'queue:{uid.uid}'

    def close(self) -> None:
        """Close the exchange interface."""
        self._client.close()
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
        self._client.set(self._active_key(aid), _MailboxState.ACTIVE.value)
        self._client.set(
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
        self._client.set(self._active_key(cid), _MailboxState.ACTIVE.value)
        logger.debug('Registered %s in %s', cid, self)
        return cid

    def terminate(self, uid: EntityId) -> None:
        """Close the mailbox for an entity from the exchange.

        Note:
            This method is a no-op if the mailbox does not exist.

        Args:
            uid: Entity identifier of the mailbox to close.
        """
        self._client.set(self._active_key(uid), _MailboxState.INACTIVE.value)
        # Sending a close sentinel to the queue is a quick way to force
        # the entity waiting on messages to the mailbox to stop blocking.
        # This assumes that only one entity is reading from the mailbox.
        self._client.rpush(self._queue_key(uid), _CLOSE_SENTINEL)
        if isinstance(uid, AgentId):
            self._client.delete(self._behavior_key(uid))
        logger.debug('Closed mailbox for %s (%s)', uid, self)

    def discover(
        self,
        behavior: type[Behavior],
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
        for key in self._client.scan_iter('behavior:*'):
            mro_str = self._client.get(key)
            assert isinstance(mro_str, str)
            mro = mro_str.split(',')
            if fqp == mro[0] or (allow_subclasses and fqp in mro):
                aid: AgentId[Any] = AgentId(uid=uuid.UUID(key.split(':')[-1]))
                found.append(aid)
        active: list[AgentId[Any]] = []
        for aid in found:
            status = self._client.get(self._active_key(aid))
            if status == _MailboxState.ACTIVE.value:  # pragma: no branch
                active.append(aid)
        return tuple(active)

    def get_mailbox(self, uid: EntityId) -> RedisMailbox:
        """Get a client to a specific mailbox.

        Args:
            uid: EntityId of the mailbox.

        Returns:
            Mailbox client.

        Raises:
            BadEntityIdError: if a mailbox for `uid` does not exist.
        """
        return RedisMailbox(uid, self)

    def send(self, uid: EntityId, message: Message) -> None:
        """Send a message to a mailbox.

        Args:
            uid: Destination address of the message.
            message: Message to send.

        Raises:
            BadEntityIdError: if a mailbox for `uid` does not exist.
            MailboxClosedError: if the mailbox was closed.
        """
        status = self._client.get(self._active_key(uid))
        if status is None:
            raise BadEntityIdError(uid)
        elif status == _MailboxState.INACTIVE.value:
            raise MailboxClosedError(uid)
        else:
            self._client.rpush(self._queue_key(uid), message.model_serialize())
            logger.debug('Sent %s to %s', type(message).__name__, uid)


class RedisMailbox(NoPickleMixin):
    """Client protocol that listens to incoming messages to a mailbox.

    Args:
        uid: EntityId of the mailbox.
        exchange: Exchange client.

    Raises:
        BadEntityIdError: if a mailbox with `uid` does not exist.
    """

    def __init__(self, uid: EntityId, exchange: RedisExchange) -> None:
        self._uid = uid
        self._exchange = exchange

        status = self.exchange._client.get(self.exchange._active_key(uid))
        if status is None:
            raise BadEntityIdError(uid)

    @property
    def exchange(self) -> RedisExchange:
        """Exchange client."""
        return self._exchange

    @property
    def mailbox_id(self) -> EntityId:
        """Mailbox address/identifier."""
        return self._uid

    def close(self) -> None:
        """Close this mailbox client.

        Warning:
            This does not close the mailbox in the exchange. I.e., the exchange
            will still accept new messages to this mailbox, but this client
            will no longer be listening for them.
        """
        pass

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
        _timeout = int(timeout) if timeout is not None else 1
        while True:
            status = self.exchange._client.get(
                self.exchange._active_key(self.mailbox_id),
            )
            if status is None:
                raise AssertionError(
                    f'Status for mailbox {self.mailbox_id} did not exist in '
                    'Redis server. This means that something incorrectly '
                    'deleted the key.',
                )
            elif status == _MailboxState.INACTIVE.value:
                raise MailboxClosedError(self.mailbox_id)

            raw = self.exchange._client.blpop(
                [self.exchange._queue_key(self.mailbox_id)],
                timeout=_timeout,
            )
            if raw is None and timeout is not None:
                raise TimeoutError(
                    f'Timeout waiting for next message for {self.mailbox_id} '
                    f'after {timeout} seconds.',
                )
            elif raw is None:  # pragma: no cover
                continue

            # Only passed one key to blpop to result is [key, item]
            assert isinstance(raw, (tuple, list))
            assert len(raw) == 2  # noqa: PLR2004
            if raw[1] == _CLOSE_SENTINEL:  # pragma: no cover
                raise MailboxClosedError(self.mailbox_id)
            message = BaseMessage.model_deserialize(raw[1])
            assert isinstance(message, get_args(Message))
            logger.debug(
                'Received %s to %s',
                type(message).__name__,
                self.mailbox_id,
            )
            return message
