"""The eval rubric (C12): how a system's output becomes pass or fail. This is yours.

`runner.run_suite()` calls `score()` by default for every task.
"""

from agent_orchestration.evals.types import EvalTask, Score, SystemOutput


def score(task: EvalTask, output: SystemOutput) -> Score:
    """TODO(human) C12: decide whether `output` is a correct answer to `task`.

    What counts as success is the most important number in the project, so decide it
    deliberately:

      A. Exact numbers within a tolerance: compare figures in the text with
         `task.expected` (objective, repeatable; needs ground truth from XBRL and a rule
         for parsing numbers like "$1.2bn" from prose).
      B. LLM judge: another model grades against a rubric (handles wording, can check
         "cited a source"; costs money and must be calibrated against your own grades).
      C. Both: numbers as a hard gate, the judge for quality and citation.

    Also decide the reported metrics (success rate, $/task, turns/task) and how a failed or
    cap-stopped run is counted: as a fail, or excluded? Excluding hides failures. The same
    rubric must score the multi-agent system and the single-agent baseline, or the
    comparison means nothing.

    Guide: docs/concepts/c12-eval-rubric.md
    Governance: NIST AI RMF MEASURE; EU AI Act Art. 15-style accuracy testing.
    """
    raise NotImplementedError("C12: see docs/concepts/c12-eval-rubric.md")
