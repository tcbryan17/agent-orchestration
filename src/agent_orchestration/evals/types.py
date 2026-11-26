"""Plain data types shared by the eval runner and the rubric.

They live in their own module so `runner.py` can use `rubric.score` as its default scorer
without a circular import.
"""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class EvalTask:
    """One graded task. `expected` maps a name to the ground-truth value the rubric checks."""

    id: str
    prompt: str
    expected: dict[str, str]
    tier: str  # for example "easy", "multi_company", "adversarial"; free text, used in reports


@dataclass(frozen=True)
class SystemOutput:
    """What a system under test produced for one task."""

    text: str
    cost_usd: Decimal
    turns: int


@dataclass(frozen=True)
class Score:
    """The rubric's verdict on one output. Change this if your rubric needs more fields."""

    passed: bool
    detail: str = ""
