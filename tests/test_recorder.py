from decimal import Decimal
from uuid import UUID

import pytest
from anthropic.types import MessageParam

from agent_orchestration import llm
from agent_orchestration.config import settings
from agent_orchestration.events import Event, EventType
from agent_orchestration.fakes import ScriptedClient, text_reply, tool_call
from agent_orchestration.guardrails import Spend
from agent_orchestration.recorder import MemorySink, Recorder

RUN_ID = UUID("00000000-0000-4000-8000-000000000002")


def test_recorder_numbers_events_in_order_and_feeds_every_sink() -> None:
    sink = MemorySink()
    rec = Recorder(run_id=RUN_ID, sinks=[sink])
    first = rec.emit(agent="supervisor", type=EventType.RUN_STARTED, text="task")
    second = rec.emit(
        agent="researcher", type=EventType.MESSAGE, text="hi", parent_id=first.event_id
    )

    assert [e.seq for e in rec.events] == [0, 1]
    assert all(e.run_id == RUN_ID for e in rec.events)
    assert second.parent_id == first.event_id
    assert sink.events == rec.events


def test_recorder_events_is_a_copy() -> None:
    rec = Recorder()
    rec.emit(agent="a", type=EventType.MESSAGE, text="x")
    rec.events.clear()
    assert len(rec.events) == 1


def test_spend_from_events_counts_calls_cost_and_revisions() -> None:
    rec = Recorder()
    rec.emit(agent="a", type=EventType.MODEL_CALL, text="", cost_usd=Decimal("0.001"))
    rec.emit(agent="a", type=EventType.MODEL_CALL, text="", cost_usd=Decimal("0.002"))
    rec.emit(agent="reviewer", type=EventType.REVIEW, text="", payload={"verdict": "revise"})
    rec.emit(agent="reviewer", type=EventType.REVIEW, text="", payload={"verdict": "approve"})

    assert Spend.from_events(rec.events) == Spend(turns=2, cost_usd=Decimal("0.003"), revisions=1)


def test_scripted_client_replays_and_records_requests() -> None:
    client = ScriptedClient([tool_call("calculator", {"expr": "1+1"}), text_reply("2")])
    messages: list[MessageParam] = [{"role": "user", "content": "add"}]
    first = client.create(model="m", max_tokens=10, system="s", messages=messages, tools=[])
    messages.append({"role": "assistant", "content": "changed later"})

    assert first.stop_reason == "tool_use"
    # The recorded request is a snapshot, so later mutation can't hide an edit-history bug.
    assert client.requests[0].messages == [{"role": "user", "content": "add"}]
    assert client.create(model="m", max_tokens=10, system="s", messages=[], tools=[]).content


def test_scripted_client_fails_loudly_when_script_runs_out() -> None:
    client = ScriptedClient([])
    with pytest.raises(AssertionError, match="ran out"):
        client.create(model="m", max_tokens=10, system="s", messages=[], tools=[])


def test_real_client_fails_fast_without_a_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "anthropic_api_key", None)
    with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
        llm.AnthropicMessages()


def test_events_are_frozen() -> None:
    event = Recorder().emit(agent="a", type=EventType.MESSAGE, text="x")
    assert isinstance(event, Event)
    with pytest.raises(ValueError):
        event.text = "edited"
