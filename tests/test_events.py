"""Event: the guarantees the replay, cost tracking and audit log rely on."""

from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest
from pydantic import ValidationError

from agent_orchestration.events import Event, EventType, TokenUsage
from agent_orchestration.pricing import cost_from_usage

MakeEvent = Callable[..., Event]


def test_required_fields_are_the_five_an_agent_must_decide() -> None:
    with pytest.raises(ValidationError) as exc:
        Event.model_validate({})
    missing = {err["loc"][0] for err in exc.value.errors() if err["type"] == "missing"}
    assert missing == {"run_id", "seq", "agent", "type", "text"}


def test_events_are_frozen(make_event: MakeEvent) -> None:
    event = make_event()
    with pytest.raises(ValidationError):
        event.text = "edited after the fact"


def test_frozen_is_shallow_and_payload_is_not_shared(make_event: MakeEvent) -> None:
    # frozen stops reassigning `payload`, not changing the dict inside it. The hash-chained
    # audit log will hash serialized JSON, so a later change like this would show up there.
    a, b = make_event(0), make_event(1)
    a.payload["note"] = "changed"
    assert b.payload == {}  # default_factory: each event gets its own dict


def test_each_event_gets_its_own_id(make_event: MakeEvent) -> None:
    assert make_event(0).event_id != make_event(1).event_id


def test_timestamp_defaults_to_now_in_utc(make_event: MakeEvent) -> None:
    before = datetime.now(UTC)
    event = Event(run_id=make_event().run_id, seq=0, agent="x", type=EventType.PLAN, text="t")
    assert event.ts.tzinfo is not None
    assert before <= event.ts <= datetime.now(UTC) + timedelta(seconds=1)


def test_naive_timestamp_is_rejected(make_event: MakeEvent) -> None:
    with pytest.raises(ValidationError):
        make_event(ts=datetime(2026, 11, 15, 12, 0))  # no timezone


def test_event_type_accepts_its_string_value(make_event: MakeEvent) -> None:
    event = make_event(type="model_call")
    assert event.type is EventType.MODEL_CALL


def test_unknown_event_type_is_rejected(make_event: MakeEvent) -> None:
    with pytest.raises(ValidationError):
        make_event(type="modle_call")  # typo: would silently drop out of cost totals


def test_json_round_trip_is_lossless(make_event: MakeEvent) -> None:
    parent = make_event(0, type=EventType.HANDOFF)
    usage = TokenUsage(input_tokens=1_000, output_tokens=500, cache_read_input_tokens=2_000)
    event = make_event(
        1,
        after_ms=1_250,
        parent_id=parent.event_id,
        agent="researcher",
        type=EventType.MODEL_CALL,
        model="claude-haiku-5-5",
        usage=usage,
        cost_usd=cost_from_usage(usage, "claude-haiku-5-5"),
        latency_ms=840,
        payload={"stop_reason": "tool_use"},
    )
    assert Event.model_validate_json(event.model_dump_json()) == event


def test_cost_is_serialized_as_an_exact_string(make_event: MakeEvent) -> None:
    # JSON numbers are floats to most readers; a string keeps the Decimal exact.
    event = make_event(type=EventType.MODEL_CALL, cost_usd=Decimal("0.00035"))
    assert '"cost_usd":"0.00035"' in event.model_dump_json()
