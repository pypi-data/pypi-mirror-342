from __future__ import annotations

import functools
import inspect
import logging
import sys
import threading
from datetime import timedelta
from typing import Any
from typing import Callable
from typing import Generic
from typing import Literal
from typing import Protocol
from typing import TypeVar

if sys.version_info >= (3, 10):  # pragma: >=3.10 cover
    from typing import Concatenate
    from typing import ParamSpec
else:  # pragma: <3.10 cover
    from typing_extensions import Concatenate
    from typing_extensions import ParamSpec

if sys.version_info >= (3, 11):  # pragma: >=3.11 cover
    from typing import Self
else:  # pragma: <3.11 cover
    from typing_extensions import Self

from academy.event import or_event
from academy.handle import Handle
from academy.handle import HandleDict
from academy.handle import HandleList

P = ParamSpec('P')
R = TypeVar('R')
R_co = TypeVar('R_co', covariant=True)
BehaviorT = TypeVar('BehaviorT', bound='Behavior')

logger = logging.getLogger(__name__)


class Behavior:
    """Agent behavior base class.

    All [`Agent`][academy.agent.Agent] instances execute a behavior which is
    defined by a subclass of the [`Behavior`][academy.behavior.Behavior]. Each
    behavior is composed of three parts:
      1. The [`on_startup()`][academy.behavior.Behavior.setup] and
         [`on_shutdown()`][academy.behavior.Behavior.shutdown] methods define
         callbacks that are invoked once at the start and end of an agent's
         execution, respectively. The methods should be used to initialize and
         cleanup stateful resources. Resource initialization should not be
         performed in `__init__`.
      2. Action methods annotated with [`@action`][academy.behavior.action]
         are methods that other agents can invoke on this agent. An agent
         may also call it's own action methods as normal methods.
      3. Control loop methods annotated with [`@loop`][academy.behavior.loop]
         are executed in separate threads when the agent is executed.

    Warning:
        This class cannot be instantiated directly and must be subclassed.
    """

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:  # noqa: D102
        if cls is Behavior:
            raise TypeError(
                f'The {cls.__name__} type cannot be instantiated directly '
                'and must be subclassed.',
            )
        return super().__new__(cls)

    def __repr__(self) -> str:
        return f'{type(self).__name__}()'

    def __str__(self) -> str:
        return f'Behavior<{type(self).__name__}>'

    def behavior_actions(self) -> dict[str, Action[Any, Any]]:
        """Get methods of this behavior type that are decorated as actions.

        Returns:
            Dictionary mapping method names to action methods.
        """
        actions: dict[str, Action[Any, Any]] = {}
        for name in dir(self):
            attr = getattr(self, name)
            if _is_agent_method_type(attr, 'action'):
                actions[name] = attr
        return actions

    def behavior_loops(self) -> dict[str, ControlLoop]:
        """Get methods of this behavior type that are decorated as loops.

        Returns:
            Dictionary mapping method names to loop methods.
        """
        loops: dict[str, ControlLoop] = {}
        for name in dir(self):
            attr = getattr(self, name)
            if _is_agent_method_type(attr, 'loop'):
                loops[name] = attr
        return loops

    def behavior_handles(
        self,
    ) -> dict[
        str,
        Handle[Any] | HandleDict[Any, Any] | HandleList[Any],
    ]:
        """Get instance attributes that are agent handles.

        Returns:
            Dictionary mapping attribute names to agent handles or \
            data structures of handles.
        """
        from academy.handle import Handle

        # This import is deferred to prevent a cyclic import with
        # academy.handle.
        handles: dict[
            str,
            Handle[Any] | HandleDict[Any, Any] | HandleList[Any],
        ] = {}
        for name in dir(self):
            attr = getattr(self, name)
            if isinstance(attr, (Handle, HandleDict, HandleList)):
                handles[name] = attr
        return handles

    def behavior_handles_bind(
        self,
        bind: Callable[[Handle[BehaviorT]], Handle[BehaviorT]],
    ) -> None:
        """Bind all instance attributes that are agent handles.

        Args:
            bind: A callback that takes a handle and returns the same handle
                or a bound version of the handle.
        """
        for attr, handles in self.behavior_handles().items():
            if isinstance(handles, Handle):
                setattr(self, attr, bind(handles))
            elif isinstance(handles, HandleDict):
                setattr(
                    self,
                    attr,
                    HandleDict({k: bind(h) for k, h in handles.items()}),
                )
            elif isinstance(handles, HandleList):
                setattr(self, attr, HandleList(bind(h) for h in handles))
            else:
                raise AssertionError('Unreachable.')

    @classmethod
    def behavior_mro(cls) -> tuple[str, ...]:
        """Get the method resolution order of the behavior.

        Example:
            ```python
            >>> from academy.behavior import Behavior
            >>>
            >>> class A(Behavior): ...
            >>> class B(Behavior): ...
            >>> class C(A): ...
            >>> class D(A, B): ...
            >>>
            >>> A.behavior_mro()
            ('__main__.A',)
            >>> B.behavior_mro()
            ('__main__.B',)
            >>> C.behavior_mro()
            ('__main__.C', '__main__.A')
            >>> D.behavior_mro()
            ('__main__.D', '__main__.A', '__main__.B')
            ```

        Returns:
            Tuple of fully-qualified paths of types in the MRO of this \
            behavior type, not including the base \
            [`Behavior`][academy.behavior.Behavior] or [`object`][object].
        """
        mro = cls.mro()
        base_index = mro.index(Behavior)
        mro = mro[:base_index]
        return tuple(f'{t.__module__}.{t.__qualname__}' for t in mro)

    def on_setup(self) -> None:
        """Setup up resources needed for the agents execution.

        This is called before any control loop threads are started.
        """
        pass

    def on_shutdown(self) -> None:
        """Shutdown resources after the agents execution.

        This is called after control loop threads have exited.
        """
        pass


class Action(Generic[P, R_co], Protocol):
    """Action method protocol."""

    _agent_method_type: Literal['action'] = 'action'

    def __call__(self, *arg: P.args, **kwargs: P.kwargs) -> R_co:
        """Expected signature of methods decorated as an action.

        In general, action methods can implement any signature.
        """
        ...


class ControlLoop(Protocol):
    """Control loop method protocol."""

    _agent_method_type: Literal['loop'] = 'loop'

    def __call__(self, shutdown: threading.Event) -> None:
        """Expected signature of methods decorated as a control loop.

        Args:
            shutdown: Event indicating that the agent has been instructed to
                shutdown and all control loops should exit.

        Returns:
            Control loops should not return anything.
        """
        ...


def action(method: Callable[P, R]) -> Callable[P, R]:
    """Decorator that annotates a method of a behavior as an action.

    Marking a method of a behavior as an action makes the method available
    to other agents. I.e., peers within a multi-agent system can only invoke
    methods marked as actions on each other. This enables behaviors to
    define "private" methods.

    Example:
        ```python
        from academy.behavior import Behavior, action

        class Example(Behavior):
            @action
            def perform(self):
                ...
        ```
    """
    method._agent_method_type = 'action'  # type: ignore[attr-defined]
    return method


def loop(
    method: Callable[Concatenate[BehaviorT, P], R],
) -> Callable[Concatenate[BehaviorT, P], R]:
    """Decorator that annotates a method of a behavior as a control loop.

    Control loop methods of a behavior are run as threads when an agent
    starts. A control loop can run for a well-defined period of time or
    indefinitely, provided the control loop exits when the `shutdown`
    event, passed as a parameter to all control loop methods, is set.

    Example:
        ```python
        import threading
        from academy.behavior import Behavior, loop

        class Example(Behavior):
            @loop
            def listen(self, shutdown: threading.Event) -> None:
                while not shutdown.is_set():
                    ...
        ```

    Raises:
        TypeError: if the method signature does not conform to the
            [`ControlLoop`][academy.behavior.ControlLoop] protocol.
    """
    method._agent_method_type = 'loop'  # type: ignore[attr-defined]

    if sys.version_info >= (3, 10):  # pragma: >=3.10 cover
        found_sig = inspect.signature(method, eval_str=True)
        expected_sig = inspect.signature(ControlLoop.__call__, eval_str=True)
    else:  # pragma: <3.10 cover
        found_sig = inspect.signature(method)
        expected_sig = inspect.signature(ControlLoop.__call__)

    if found_sig != expected_sig:
        raise TypeError(
            f'Signature of loop method "{method.__name__}" is {found_sig} '
            f'but should be {expected_sig}. If the signatures look the same '
            'except that types are stringified, try importing '
            '"from __future__ import annotations" at the top of the module '
            'where the behavior is defined.',
        )

    @functools.wraps(method)
    def _wrapped(self: BehaviorT, *args: P.args, **kwargs: P.kwargs) -> R:
        logger.debug('Started %r loop for %s', method.__name__, self)
        result = method(self, *args, **kwargs)
        logger.debug('Exited %r loop for %s', method.__name__, self)
        return result

    return _wrapped


def event(
    name: str,
) -> Callable[
    [Callable[[BehaviorT], None]],
    Callable[[BehaviorT, threading.Event], None],
]:
    """Decorator that annotates a method of a behavior as an event loop.

    An event loop is a special type of control loop that runs when a
    [`threading.Event`][threading.Event] is set. The event is cleared
    after the loop runs.

    Example:
        ```python
        import threading
        from academy.behavior import Behavior, timer

        class Example(Behavior):
            def __init__(self) -> None:
                self.alert = threading.Event()

            @event('alert')
            def handle(self) -> None:
                # Runs every time alter is set
                ...
        ```

    Args:
        name: Attribute name of the [`threading.Event`][theading.Event]
            to wait on.

    Raises:
        AttributeError: Raised at runtime if no attribute named `name`
            exists on the behavior.
        TypeError: Raised at runtime if the attribute named `name` is not
            a [`threading.Event`][threading.Event].
    """

    def decorator(
        method: Callable[[BehaviorT], None],
    ) -> Callable[[BehaviorT, threading.Event], None]:
        method._agent_method_type = 'loop'  # type: ignore[attr-defined]

        @functools.wraps(method)
        def _wrapped(self: BehaviorT, shutdown: threading.Event) -> None:
            event = getattr(self, name)
            if not isinstance(event, threading.Event):
                raise TypeError(
                    f'Attribute {name} of {type(self).__class__} has type '
                    f'{type(event).__class__}. Expected threading.Event.',
                )

            logger.debug(
                'Started %r event loop for %s (event: %r)',
                method.__name__,
                self,
                name,
            )
            combined = or_event(shutdown, event)
            while True:
                combined.wait()
                if shutdown.is_set():
                    break
                elif event.is_set():
                    try:
                        method(self)
                    finally:
                        event.clear()
                else:
                    raise AssertionError('Unreachable.')
            logger.debug('Exited %r event loop for %s', method.__name__, self)

        return _wrapped

    return decorator


def timer(
    interval: float | timedelta,
) -> Callable[
    [Callable[[BehaviorT], None]],
    Callable[[BehaviorT, threading.Event], None],
]:
    """Decorator that annotates a method of a behavior as a timer loop.

    A timer loop is a special type of control loop that runs at a set
    interval. The method will always be called once before the first
    sleep.

    Example:
        ```python
        from academy.behavior import Behavior, timer

        class Example(Behavior):
            @timer(interval=1)
            def listen(self) -> None:
                # Runs every 1 second
                ...
        ```

    Args:
        interval: Seconds or a [`timedelta`][datetime.timedelta] to wait
            between invoking the method.
    """
    interval = (
        interval.total_seconds()
        if isinstance(interval, timedelta)
        else interval
    )

    def decorator(
        method: Callable[[BehaviorT], None],
    ) -> Callable[[BehaviorT, threading.Event], None]:
        method._agent_method_type = 'loop'  # type: ignore[attr-defined]

        @functools.wraps(method)
        def _wrapped(self: BehaviorT, shutdown: threading.Event) -> None:
            logger.debug(
                'Started %r timer loop for %s (interval: %fs)',
                method.__name__,
                self,
                interval,
            )
            while not shutdown.wait(interval):
                method(self)
            logger.debug('Exited %r timer loop for %s', method.__name__, self)

        return _wrapped

    return decorator


def _is_agent_method_type(obj: Any, kind: str) -> bool:
    return (
        callable(obj)
        and hasattr(obj, '_agent_method_type')
        and obj._agent_method_type == kind
    )
