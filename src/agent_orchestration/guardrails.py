"""Run limits: turns, dollars and reviewer revisions, checked BEFORE each model call.

Boilerplate here: the limit values, a running total built from the event log, and the
description of the call about to be made. The decision itself, `check_budget()`, is C7 and
is yours. If your design needs different fields on these types, change them; they exist so
the loop and the tests have something to call.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal

from anthropic.types import MessageParam, ToolParam

from agent_orchestration.events import Event, EventType


@dataclass(frozen=True)
class Limits:
    """Hard caps for one run. The README promises a cap on turns and dollars."""

    max_turns: int = 20
    max_usd: Decimal = Decimal("0.50")
    max_revisions: int = 2


@dataclass(frozen=True)
class Spend:
    """What a run has used so far, derived from its events (the log is the source of truth)."""

    turns: int
    cost_usd: Decimal
    revisions: int

    @classmethod
    def from_events(cls, events: Sequence[Event]) -> "Spend":
        """Count model calls, sum their exact cost, and count reviewer "revise" verdicts."""
        return cls(
            turns=sum(1 for e in events if e.type is EventType.MODEL_CALL),
            cost_usd=sum((e.cost_usd for e in events if e.cost_usd is not None), Decimal(0)),
            revisions=sum(
                1
                for e in events
                if e.type is EventType.REVIEW and e.payload.get("verdict") == "revise"
            ),
        )


@dataclass(frozen=True)
class PlannedCall:
    """The request about to be sent. Holds everything any estimation option could need."""

    model: str
    max_tokens: int
    system: str
    messages: Sequence[MessageParam]
    tools: Sequence[ToolParam]


@dataclass(frozen=True)
class GuardrailResult:
    """`allowed=False` stops the run; `reason` goes into a GUARDRAIL event."""

    allowed: bool
    reason: str = ""


def check_budget(spent: Spend, next_call: PlannedCall, limits: Limits) -> GuardrailResult:
    """TODO(human) C7: decide whether the next model call may run.

    Called by run_agent() BEFORE every API call (PLAN.md: "checked before each API call").
    The turn cap is easy. The dollar cap is the real question: how do you know what the
    next call will cost before you make it?

      A. Worst case: price the prompt as if it were all input, plus `max_tokens` of output.
         Never overshoots the cap; ends runs a little early.
      B. Count the prompt with the count_tokens endpoint, plus an output guess.
         Close to the real cost; one extra (free, rate-limited) API call per turn.
      C. Check only what's already spent (`spent.cost_usd`), not the next call.
         Simplest; can overshoot by one call's cost.

    Also decide: does a cap breach stop the run or hand it to a human (C9)? Do workers share
    the run's budget or get their own slice? Remember Haiku's price jumps above 100K prompt
    tokens (pricing.py), so option A must use the right tier.

    Guide: docs/concepts/c07-budget-guardrails.md
    Governance: NIST AI RMF MANAGE (risk treatment); GOVERN (stated risk tolerance).
    """
    raise NotImplementedError("C7: see docs/concepts/c07-budget-guardrails.md")
