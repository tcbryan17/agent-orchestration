"""Acceptance tests for C9, approval.request_approval / resolve_approval.

Delete `pytestmark` to switch them on. Invariants: a request is recorded as an event, a
decision names a human approver, and one request cannot be resolved twice.
"""

import pytest

from agent_orchestration.approval import request_approval, resolve_approval
from agent_orchestration.recorder import Recorder

pytestmark = [
    pytest.mark.human_todo,
    pytest.mark.skip(reason="C9 not written yet: docs/concepts/c09-human-approval.md"),
]


def test_request_is_recorded_in_the_log() -> None:
    rec = Recorder()
    request = request_approval(recorder=rec, deliverable="report", reason="publish", parent_id=None)
    assert request.run_id == rec.run_id
    assert len(rec.events) >= 1


def test_decision_records_who_decided() -> None:
    rec = Recorder()
    request = request_approval(recorder=rec, deliverable="r", reason="publish", parent_id=None)
    before = len(rec.events)
    decision = resolve_approval(
        recorder=rec, request=request, approver="owner", approved=True, note="ok"
    )
    assert decision.approver == "owner" and decision.approved
    assert len(rec.events) > before


def test_a_request_cannot_be_resolved_twice() -> None:
    rec = Recorder()
    request = request_approval(recorder=rec, deliverable="r", reason="publish", parent_id=None)
    resolve_approval(recorder=rec, request=request, approver="owner", approved=True, note="")
    with pytest.raises(Exception):  # noqa: B017 - your design picks the exception type
        resolve_approval(recorder=rec, request=request, approver="owner", approved=False, note="")
