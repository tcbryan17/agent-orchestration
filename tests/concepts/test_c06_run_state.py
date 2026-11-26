"""Acceptance tests for C6, RunState.from_events. Delete `pytestmark` to switch them on.

Invariants for any design: state is a pure function of the events (rebuilding twice gives the
same answer, order of arrival is by `seq`), and an empty log is a valid, fresh run.
"""

from collections.abc import Callable

import pytest

from agent_orchestration.events import Event, EventType
from agent_orchestration.state import RunState

pytestmark = [
    pytest.mark.human_todo,
    pytest.mark.skip(reason="C6 not written yet: docs/concepts/c06-run-state.md"),
]

MakeEvent = Callable[..., Event]


def test_empty_log_is_a_valid_fresh_state() -> None:
    assert RunState.from_events([]) is not None


def test_rebuilding_twice_gives_the_same_state(make_event: MakeEvent) -> None:
    events = [make_event(0, type=EventType.RUN_STARTED), make_event(1, type=EventType.PLAN)]
    assert RunState.from_events(events) == RunState.from_events(events)


def test_state_does_not_depend_on_input_order(make_event: MakeEvent) -> None:
    events = [make_event(i) for i in range(3)]
    assert RunState.from_events(events) == RunState.from_events(list(reversed(events)))


def test_more_events_never_remove_information(make_event: MakeEvent) -> None:
    # Append-only: the state built from a longer log still reflects the shorter log's events.
    events = [make_event(0), make_event(1)]
    short, long = RunState.from_events(events[:1]), RunState.from_events(events)
    assert short != long
