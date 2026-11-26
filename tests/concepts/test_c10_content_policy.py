"""Acceptance tests for C10, policy.check_policy. Delete `pytestmark` to switch them on.

Whatever detection method you pick: ordinary financial prose passes, an obvious betting tip
does not, and a result that changes the text must say what it found.
"""

import pytest

from agent_orchestration.policy import check_policy

pytestmark = [
    pytest.mark.human_todo,
    pytest.mark.skip(reason="C10 not written yet: docs/concepts/c10-content-policy.md"),
]

CLEAN = "DraftKings reported revenue of $4.0bn for fiscal 2025 (10-K, revenue)."
TIP = "Bet on Arsenal to win this weekend, the odds are great. Place your bet now!"


def test_ordinary_financial_prose_is_allowed_unchanged() -> None:
    result = check_policy(CLEAN)
    assert result.action == "allow" and result.text == CLEAN and not result.findings


def test_an_obvious_betting_tip_is_not_allowed() -> None:
    result = check_policy(TIP)
    assert result.action != "allow" and result.findings


def test_redaction_never_leaves_the_tip_in_the_text() -> None:
    result = check_policy(TIP)
    if result.action == "redact":
        assert "Place your bet now" not in result.text


def test_same_input_gives_the_same_result() -> None:
    assert check_policy(TIP) == check_policy(TIP)
