"""Acceptance tests for C5, supervisor.delegate. Delete `pytestmark` to switch them on.

These hold whichever handoff design you pick. Add tests for your own choices (what exactly
the worker sees, what shape the result has).
"""

import pytest

from agent_orchestration.agents.specs import SPECS
from agent_orchestration.events import EventType
from agent_orchestration.fakes import ScriptedClient, text_reply
from agent_orchestration.guardrails import Limits
from agent_orchestration.recorder import Recorder
from agent_orchestration.supervisor import delegate

pytestmark = [
    pytest.mark.human_todo,
    pytest.mark.skip(reason="C5 not written yet: docs/concepts/c05-supervisor-handoff.md"),
]


def run_delegate(client: ScriptedClient, rec: Recorder, brief: str = "Get FY revenue.") -> None:
    root = rec.emit(agent="supervisor", type=EventType.PLAN, text="plan")
    result = delegate(
        client=client,
        recorder=rec,
        worker=SPECS["researcher"],
        brief=brief,
        artifacts=[],
        limits=Limits(),
        parent_id=root.event_id,
    )
    assert result.text == "Revenue was 100."


def test_worker_gets_a_fresh_conversation_containing_the_brief() -> None:
    client = ScriptedClient([text_reply("Revenue was 100.")])
    run_delegate(client, Recorder(), brief="Get FY revenue.")

    messages = client.requests[0].messages
    assert messages[0]["role"] == "user"
    assert "Get FY revenue." in str(messages[0]["content"])


def test_worker_uses_its_own_model_prompt_and_only_its_own_tools() -> None:
    client = ScriptedClient([text_reply("Revenue was 100.")])
    run_delegate(client, Recorder())

    request = client.requests[0]
    assert request.model == SPECS["researcher"].model
    assert {t["name"] for t in request.tools} <= SPECS["researcher"].tools


def test_handoff_is_recorded_and_worker_events_hang_off_the_run_tree() -> None:
    rec = Recorder()
    run_delegate(ScriptedClient([text_reply("Revenue was 100.")]), rec)

    assert any(e.type is EventType.HANDOFF for e in rec.events)
    assert all(e.parent_id is not None for e in rec.events[1:])
