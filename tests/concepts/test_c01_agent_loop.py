"""Acceptance tests for C1, the agent loop (loop.run_agent).

Skipped until you write the loop: delete the `pytestmark` line below to switch them on.
They check invariants every design must keep, not which option you pick. Add one test of
your own for your `max_tokens` and `refusal` choices once you've made them.
"""

from typing import Any, cast

import pytest
from anthropic.types import MessageParam

from agent_orchestration.events import EventType
from agent_orchestration.fakes import ScriptedClient, text_reply, tool_call, tool_calls
from agent_orchestration.guardrails import Limits
from agent_orchestration.loop import AgentResult, run_agent
from agent_orchestration.recorder import Recorder
from agent_orchestration.tools.base import ToolOutcome

pytestmark = [
    pytest.mark.human_todo,
    pytest.mark.skip(reason="C1 not written yet: docs/concepts/c01-agent-loop.md"),
]

TOOLS: list[Any] = [
    {"name": "calculator", "description": "Arithmetic", "input_schema": {"type": "object"}}
]


def echo_dispatch(name: str, tool_input: dict[str, Any]) -> ToolOutcome:
    if name == "broken":
        return ToolOutcome(content="tool failed: timeout", is_error=True)
    return ToolOutcome(content=f"{name} ok")


def tool_results(message: MessageParam) -> list[dict[str, Any]]:
    """The tool_result blocks of a user message (typed once here, so tests stay readable)."""
    blocks = cast(list[dict[str, Any]], message["content"])
    return [b for b in blocks if b["type"] == "tool_result"]


def run(client: ScriptedClient, recorder: Recorder, **kw: Any) -> AgentResult:
    args: dict[str, Any] = dict(
        client=client,
        recorder=recorder,
        agent="analyst",
        model="claude-haiku-5-5",
        system="You are an analyst.",
        task="Compare revenue.",
        tools=TOOLS,
        dispatch=echo_dispatch,
        limits=Limits(),
    )
    args.update(kw)
    return run_agent(**args)


def test_end_turn_returns_the_text_after_one_call() -> None:
    client, rec = ScriptedClient([text_reply("Done.")]), Recorder()
    result = run(client, rec)

    assert result.text == "Done."
    assert result.stop_reason == "end_turn"
    assert result.turns == 1
    calls = [e for e in rec.events if e.type is EventType.MODEL_CALL]
    assert len(calls) == 1 and calls[0].cost_usd is not None and calls[0].usage is not None


def test_tool_use_result_goes_back_with_the_matching_id() -> None:
    client = ScriptedClient([tool_call("calculator", {"x": 1}, tool_id="toolu_A"), text_reply("2")])
    rec = Recorder()
    run(client, rec)

    last_user = client.requests[1].messages[-1]
    assert last_user["role"] == "user"
    results = tool_results(last_user)
    assert [r["tool_use_id"] for r in results] == ["toolu_A"]
    types = [e.type for e in rec.events]
    assert EventType.TOOL_CALL in types and EventType.TOOL_RESULT in types


def test_parallel_tool_calls_answered_in_one_message() -> None:
    reply = tool_calls([("t1", "calculator", {}), ("t2", "calculator", {})])
    client = ScriptedClient([reply, text_reply("ok")])
    run(client, Recorder())

    ids = [r["tool_use_id"] for r in tool_results(client.requests[1].messages[-1])]
    assert ids == ["t1", "t2"]


def test_tool_error_goes_back_to_the_model_and_the_run_continues() -> None:
    client = ScriptedClient([tool_call("broken", {}), text_reply("Recovered.")])
    result = run(client, Recorder())

    result_block = tool_results(client.requests[1].messages[-1])[0]
    assert result_block.get("is_error") is True
    assert result.text == "Recovered."


def test_history_is_append_only() -> None:
    client = ScriptedClient([tool_call("calculator", {}), text_reply("ok")])
    run(client, Recorder())

    first, second = client.requests[0].messages, client.requests[1].messages
    assert second[: len(first)] == first


def test_refusal_stops_without_looping() -> None:
    client = ScriptedClient([text_reply("I can't help with that.", stop_reason="refusal")])
    result = run(client, Recorder())  # a second call would exhaust the script and fail

    assert result.stop_reason == "refusal"


def test_turn_limit_is_checked_before_the_call() -> None:
    client = ScriptedClient([tool_call("calculator", {}), text_reply("never reached")])
    rec = Recorder()
    run(client, rec, limits=Limits(max_turns=1))

    assert len(client.requests) == 1
    assert any(e.type is EventType.GUARDRAIL for e in rec.events)


def test_every_event_hangs_off_the_parent() -> None:
    rec = Recorder()
    root = rec.emit(agent="supervisor", type=EventType.HANDOFF, text="to analyst")
    run(ScriptedClient([text_reply("ok")]), rec, parent_id=root.event_id)

    for event in rec.events[1:]:
        assert event.parent_id is not None
