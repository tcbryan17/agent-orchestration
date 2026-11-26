"""Acceptance tests for C8, reviewer.review and reviewer.next_step. Delete `pytestmark`.

They hold for every option: approval ships, the loop always terminates, and a revise verdict
under the revision cap sends the work back. Add a test for your max-revisions choice.
"""

from decimal import Decimal

import pytest

from agent_orchestration.guardrails import Limits, Spend
from agent_orchestration.reviewer import Verdict, next_step

pytestmark = [
    pytest.mark.human_todo,
    pytest.mark.skip(reason="C8 not written yet: docs/concepts/c08-reviewer-loop.md"),
]

LIMITS = Limits(max_turns=20, max_usd=Decimal("1"), max_revisions=2)
APPROVE = Verdict(approved=True)
REVISE = Verdict(approved=False, notes="cite the source for revenue")


def test_approved_ships() -> None:
    assert next_step(APPROVE, Spend(5, Decimal("0.1"), 0), LIMITS) == "ship"


def test_revise_under_the_cap_asks_for_a_revision() -> None:
    assert next_step(REVISE, Spend(5, Decimal("0.1"), 0), LIMITS) == "revise"


def test_revise_at_the_cap_never_asks_for_another_revision() -> None:
    result = next_step(REVISE, Spend(9, Decimal("0.3"), LIMITS.max_revisions), LIMITS)
    assert result != "revise"
    assert result in {"ship_with_caveat", "fail", "escalate"}


def test_next_step_is_deterministic() -> None:
    spent = Spend(5, Decimal("0.1"), 1)
    assert next_step(REVISE, spent, LIMITS) == next_step(REVISE, spent, LIMITS)
