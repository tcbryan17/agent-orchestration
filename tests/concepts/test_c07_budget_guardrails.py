"""Acceptance tests for C7, guardrails.check_budget. Delete `pytestmark` to switch them on.

These hold for every estimation option. Add a test for your option's edge case: for example,
with option A, a call that would cross the dollar cap is refused even though the run hasn't
crossed it yet.
"""

from decimal import Decimal

import pytest

from agent_orchestration.guardrails import Limits, PlannedCall, Spend, check_budget

pytestmark = [
    pytest.mark.human_todo,
    pytest.mark.skip(reason="C7 not written yet: docs/concepts/c07-budget-guardrails.md"),
]

LIMITS = Limits(max_turns=5, max_usd=Decimal("0.10"), max_revisions=2)
CALL = PlannedCall(
    model="claude-haiku-5-5",
    max_tokens=1000,
    system="s",
    messages=[{"role": "user", "content": "hi"}],
    tools=[],
)


def test_fresh_run_is_allowed() -> None:
    assert check_budget(Spend(0, Decimal(0), 0), CALL, LIMITS).allowed


def test_turn_cap_blocks_with_a_reason() -> None:
    result = check_budget(Spend(5, Decimal(0), 0), CALL, LIMITS)
    assert not result.allowed and result.reason


def test_dollar_cap_blocks_once_reached() -> None:
    result = check_budget(Spend(1, Decimal("0.10"), 0), CALL, LIMITS)
    assert not result.allowed and result.reason
