"""Human approval (C9): a person signs off before a deliverable counts as published.

The two stubs are the request (the run pauses) and the resolution (a person answers, and
the run resumes, later via the API in Phase 6).

Owner adds `EventType.APPROVAL` to `events.py` when you write these: until then there is no
event type for "approval requested / granted / denied". Do not use `GUARDRAIL` for it, since
a person's decision is not a limit firing.
"""

from dataclasses import dataclass
from typing import Literal
from uuid import UUID

from agent_orchestration.recorder import Recorder

ApprovalStatus = Literal["awaiting_approval", "approved", "denied"]


@dataclass(frozen=True)
class ApprovalRequest:
    """A deliverable waiting for a person. Minimal; change this if your design needs it."""

    request_id: UUID
    run_id: UUID
    deliverable: str
    reason: str  # why a person is needed: "publish", "guardrail tripped", ...


@dataclass(frozen=True)
class ApprovalDecision:
    """A person's answer. Minimal; change this if your design needs it."""

    request_id: UUID
    approved: bool
    approver: str  # who decided; never a model
    note: str = ""


def request_approval(
    *, recorder: Recorder, deliverable: str, reason: str, parent_id: UUID | None
) -> ApprovalRequest:
    """TODO(human) C9: pause the run and ask a person to approve `deliverable`.

    Where does a person sign off?

      A. Only before "published": minimal friction, one gate; mistakes between agents go
         unseen until the end.
      B. Also when a guardrail trips (C7 cap, C10 policy flag, C8 max revisions): a person
         handles the exceptions; more interruptions, needs someone on call.
      C. Before every handoff: strongest oversight; the run is slow and a person becomes
         the bottleneck, which defeats the point of agents.

    Mechanism: the run records an approval-requested event, stops with status
    `awaiting_approval`, and is resumed through the API when a person answers
    (`resolve_approval`). Decide what is stored while it waits (the event log is enough if
    state can be rebuilt from it, C6) and what happens if nobody answers (timeout, then fail?).

    Guide: docs/concepts/c09-human-approval.md
    Governance: EU AI Act Art. 14-style human oversight; NIST AI RMF MANAGE; ISO/IEC 42001
    human oversight.
    """
    raise NotImplementedError("C9: see docs/concepts/c09-human-approval.md")


def resolve_approval(
    *, recorder: Recorder, request: ApprovalRequest, approver: str, approved: bool, note: str
) -> ApprovalDecision:
    """TODO(human) C9: record a person's decision so the run can resume or stop.

    Decide: is `approver` verified (the API's job in Phase 6) or only recorded? Can one
    request be resolved twice (it should not be)? Does a denial end the run, or send it
    back to revise (C8)?

    Guide: docs/concepts/c09-human-approval.md
    Governance: EU AI Act Art. 14-style human oversight; NIST AI RMF MANAGE; ISO/IEC 42001
    human oversight.
    """
    raise NotImplementedError("C9: see docs/concepts/c09-human-approval.md")
