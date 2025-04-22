from __future__ import annotations

import threading
from typing import Any
from typing import Callable


def _or_set(event: Any) -> None:
    event._set()
    event.changed()


def _or_clear(event: Any) -> None:
    event._clear()
    event.changed()


def _orify(
    event: threading.Event,
    changed_callback: Callable[[], None],
) -> None:
    event._set = event.set  # type: ignore[attr-defined]
    event._clear = event.clear  # type: ignore[attr-defined]
    event.changed = changed_callback  # type: ignore[attr-defined]
    event.set = lambda: _or_set(event)  # type: ignore[method-assign]
    event.clear = lambda: _or_clear(event)  # type: ignore[method-assign]


def or_event(*events: threading.Event) -> threading.Event:
    """Create a combined event that is set when any input events are set.

    Note:
        The creator can wait on the combined event, but must still check
        each individual event to see which was set.

    Warning:
        This works by dynamically replacing methods on the inputs events
        with custom methods that trigger callbacks.

    Note:
        Based on the
        [Stack Overflow answer][https://stackoverflow.com/a/12320352].

    Args:
        events: One or more events to combine.

    Returns:
        A single event that is set when any of the input events is set.
    """
    combined = threading.Event()

    def changed() -> None:
        bools = [e.is_set() for e in events]
        if any(bools):
            combined.set()
        else:
            combined.clear()

    for e in events:
        _orify(e, changed)

    changed()
    return combined
