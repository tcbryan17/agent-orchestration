"""The eval runner: run tasks through a system, score them, stop at a dollar cap, report.

Why this is separate from the rubric: the runner is plumbing (loading tasks, looping,
adding up cost, writing a report). The rubric (`rubric.py`, C12) is the judgement. A
`system` is any function `prompt -> SystemOutput`, so the same runner measures the
multi-agent system and a single-agent baseline, which is the comparison the README promises
(success rate, $/task, turns/task).

The cost cap is checked before each task, so a suite can overshoot by at most one task.
Tasks skipped because of the cap are listed in the report, never silently dropped: a success
rate over fewer tasks than planned must say so (NIST AI RMF MEASURE).
"""

import tomllib
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

from agent_orchestration.evals.rubric import score as default_score
from agent_orchestration.evals.types import EvalTask, Score, SystemOutput

System = Callable[[str], SystemOutput]
Scorer = Callable[[EvalTask, SystemOutput], Score]


@dataclass(frozen=True)
class TaskResult:
    task: EvalTask
    output: SystemOutput
    score: Score


@dataclass(frozen=True)
class SuiteReport:
    system_name: str
    results: list[TaskResult] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)  # task ids not run because of the cap
    max_usd: Decimal = Decimal(0)

    @property
    def n(self) -> int:
        return len(self.results)

    @property
    def total_cost(self) -> Decimal:
        return sum((r.output.cost_usd for r in self.results), Decimal(0))

    @property
    def success_rate(self) -> float:
        return sum(1 for r in self.results if r.score.passed) / self.n if self.n else 0.0

    @property
    def cost_per_task(self) -> Decimal:
        return self.total_cost / self.n if self.n else Decimal(0)

    @property
    def turns_per_task(self) -> float:
        return sum(r.output.turns for r in self.results) / self.n if self.n else 0.0


def load_tasks(directory: Path) -> list[EvalTask]:
    """Load every `*.toml` file in `directory`, sorted by file name (stable order)."""
    tasks: list[EvalTask] = []
    for path in sorted(directory.glob("*.toml")):
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        tasks.append(
            EvalTask(
                id=str(data["id"]),
                prompt=str(data["prompt"]),
                expected={str(k): str(v) for k, v in data.get("expected", {}).items()},
                tier=str(data.get("tier", "untiered")),
            )
        )
    return tasks


def run_suite(
    tasks: Iterable[EvalTask],
    system: System,
    scorer: Scorer | None = None,
    *,
    max_usd: Decimal,
    system_name: str = "system",
) -> SuiteReport:
    """Run tasks in order until done or the dollar cap is reached."""
    score_fn = scorer or default_score
    results: list[TaskResult] = []
    skipped: list[str] = []
    spent = Decimal(0)
    for task in tasks:
        if spent >= max_usd:
            skipped.append(task.id)
            continue
        output = system(task.prompt)
        spent += output.cost_usd
        results.append(TaskResult(task, output, score_fn(task, output)))
    return SuiteReport(system_name, results, skipped, max_usd)


def render_report(reports: Sequence[SuiteReport]) -> str:
    """Markdown: a summary table (one row per system), then per-task rows for each system."""
    lines = [
        "# Eval report",
        "",
        "| System | Tasks run | Success rate | $/task | Turns/task | Total $ | Skipped (cap) |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in reports:
        lines.append(
            f"| {r.system_name} | {r.n} | {r.success_rate:.0%} | ${r.cost_per_task:.4f} "
            f"| {r.turns_per_task:.1f} | ${r.total_cost:.4f} | {len(r.skipped)} |"
        )
    for r in reports:
        lines += ["", f"## {r.system_name}", "", "| Task | Tier | Result | $ | Turns | Detail |"]
        lines.append("|---|---|---|---|---|---|")
        for t in r.results:
            verdict = "pass" if t.score.passed else "fail"
            detail = t.score.detail.replace("|", "/").replace("\n", " ")
            lines.append(
                f"| {t.task.id} | {t.task.tier} | {verdict} | ${t.output.cost_usd:.4f} "
                f"| {t.output.turns} | {detail} |"
            )
        if r.skipped:
            lines += [
                "",
                f"Skipped because the ${r.max_usd} cap was reached: " + ", ".join(r.skipped),
            ]
    return "\n".join(lines) + "\n"


def write_report(report: SuiteReport, path: Path, baseline: SuiteReport | None = None) -> None:
    """Write the markdown report. Pass `baseline` to compare two systems side by side."""
    reports = [report] if baseline is None else [report, baseline]
    path.write_text(render_report(reports), encoding="utf-8")
