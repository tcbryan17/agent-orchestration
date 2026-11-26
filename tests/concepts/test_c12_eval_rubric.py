"""Acceptance tests for C12, evals.rubric.score. Delete `pytestmark` to switch them on.

Invariants for any rubric: scoring is deterministic for the same input, an empty answer
never passes, and the score does not depend on cost or turns (so the multi-agent system and
the single-agent baseline are judged by the same standard).
"""

from decimal import Decimal

import pytest

from agent_orchestration.evals.rubric import score
from agent_orchestration.evals.types import EvalTask, SystemOutput

pytestmark = [
    pytest.mark.human_todo,
    pytest.mark.skip(reason="C12 not written yet: docs/concepts/c12-eval-rubric.md"),
]

TASK = EvalTask("t", "Revenue?", {"revenue": "4000000000"}, "easy")


def out(text: str, cost: str = "0.01", turns: int = 3) -> SystemOutput:
    return SystemOutput(text=text, cost_usd=Decimal(cost), turns=turns)


def test_empty_answer_does_not_pass() -> None:
    assert not score(TASK, out("")).passed


def test_same_input_same_score() -> None:
    assert score(TASK, out("Revenue was 4000000000")) == score(TASK, out("Revenue was 4000000000"))


def test_score_ignores_cost_and_turns() -> None:
    cheap, dear = out("Revenue was 4000000000", "0.01", 2), out("Revenue was 4000000000", "9", 30)
    assert score(TASK, cheap).passed == score(TASK, dear).passed


def test_a_clearly_wrong_number_does_not_pass() -> None:
    assert not score(TASK, out("Revenue was 1")).passed
