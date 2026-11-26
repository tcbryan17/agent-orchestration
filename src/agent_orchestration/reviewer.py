"""The reviewer loop (C8): critique a deliverable, then decide what happens next.

Two stubs: `review()` asks the reviewer agent for a verdict, and `next_step()` decides what
the run does with it. Splitting them keeps the termination rule a plain function you can
test without any model.
"""

from dataclasses import dataclass, field
from typing import Literal
from uuid import UUID

from agent_orchestration.agents.specs import AgentSpec
from agent_orchestration.guardrails import Limits, Spend
from agent_orchestration.llm import MessagesClient
from agent_orchestration.recorder import Recorder

NextStep = Literal["ship", "revise", "ship_with_caveat", "fail", "escalate"]


@dataclass(frozen=True)
class Verdict:
    """The reviewer's judgement. Minimal; change this if your design needs it.

    `scores` is empty for a plain approve/revise design and holds one entry per criterion
    for a rubric design.
    """

    approved: bool
    notes: str = ""
    scores: dict[str, int] = field(default_factory=dict)


def review(
    *,
    client: MessagesClient,
    recorder: Recorder,
    reviewer: AgentSpec,
    deliverable: str,
    parent_id: UUID | None,
) -> Verdict:
    """TODO(human) C8: have the reviewer judge `deliverable` and return a Verdict.

    What does a verdict look like?

      A. Approve or revise, with notes: simple, easy to act on; coarse, and "approve" can
         hide how close the call was.
      B. A scored rubric (for example 1-5 per criterion, approve above a threshold): more
         signal and tunable; harder to calibrate, and a small model's scores can be noisy.

    Also decide how the verdict is parsed (strict JSON, or a tool call with a strict
    schema, which is more reliable) and what happens when it cannot be parsed. Record a
    REVIEW event with `payload["verdict"]` set to "approve" or "revise": `Spend.from_events`
    counts revisions from it.

    Guide: docs/concepts/c08-reviewer-loop.md
    Governance: NIST AI RMF MEASURE (testing before release), MANAGE; ISO/IEC 42001
    verification of outputs.
    """
    raise NotImplementedError("C8: see docs/concepts/c08-reviewer-loop.md")


def next_step(verdict: Verdict, spent: Spend, limits: Limits) -> NextStep:
    """TODO(human) C8: decide what the run does after this verdict. Must terminate.

    An approved verdict ships. The real question is a "revise" verdict when
    `spent.revisions` has reached `limits.max_revisions`:

      A. Ship with a visible caveat ("not approved by the reviewer; open notes: ..."):
         the user gets something, honestly labelled; a weak draft goes out.
      B. Fail: nothing unreviewed is ever published; the spend so far is wasted.
      C. Escalate to a human (C9): best judgement call; needs the approval mechanism and
         a person available.

    Also decide: does running out of dollars or turns (C7) change the answer? Whatever you
    choose, the loop must always end: revisions are bounded by `limits.max_revisions`.

    Guide: docs/concepts/c08-reviewer-loop.md
    Governance: NIST AI RMF MANAGE (risk response); ISO/IEC 42001 human oversight.
    """
    raise NotImplementedError("C8: see docs/concepts/c08-reviewer-loop.md")
