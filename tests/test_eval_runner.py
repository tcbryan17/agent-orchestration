"""Tests for the eval runner, with a fake system and a fake scorer (no API, no rubric)."""

from decimal import Decimal
from pathlib import Path

from agent_orchestration.evals.runner import (
    SuiteReport,
    load_tasks,
    render_report,
    run_suite,
    write_report,
)
from agent_orchestration.evals.types import EvalTask, Score, SystemOutput


def tasks(n: int) -> list[EvalTask]:
    return [EvalTask(f"t{i}", f"prompt {i}", {"x": "1"}, "easy") for i in range(n)]


def fake_system(prompt: str) -> SystemOutput:
    return SystemOutput(text=f"answer to {prompt}", cost_usd=Decimal("0.10"), turns=4)


def fake_scorer(task: EvalTask, output: SystemOutput) -> Score:
    return Score(passed=task.id != "t1", detail="stub")


def test_runs_every_task_and_computes_metrics() -> None:
    report = run_suite(tasks(4), fake_system, fake_scorer, max_usd=Decimal("10"))
    assert report.n == 4 and report.skipped == []
    assert report.success_rate == 0.75
    assert report.cost_per_task == Decimal("0.10")
    assert report.turns_per_task == 4.0


def test_cost_cap_stops_the_suite_and_lists_skipped_tasks() -> None:
    report = run_suite(tasks(5), fake_system, fake_scorer, max_usd=Decimal("0.25"))
    # cap checked before each task: after 3 tasks $0.30 >= $0.25, so the last two are skipped
    assert report.n == 3
    assert report.skipped == ["t3", "t4"]


def test_empty_suite_has_zero_metrics() -> None:
    report = run_suite([], fake_system, fake_scorer, max_usd=Decimal("1"))
    assert report.success_rate == 0.0 and report.cost_per_task == 0


def test_report_contains_metrics_and_rows(tmp_path: Path) -> None:
    report = run_suite(
        tasks(2), fake_system, fake_scorer, max_usd=Decimal("10"), system_name="multi"
    )
    out = tmp_path / "report.md"
    write_report(report, out)
    text = out.read_text()
    assert "multi" in text and "50%" in text and "$0.1000" in text and "4.0" in text
    assert "| t0 | easy | pass |" in text and "| t1 | easy | fail |" in text


def test_report_compares_two_systems() -> None:
    multi = run_suite(tasks(2), fake_system, fake_scorer, max_usd=Decimal("9"), system_name="multi")
    single = SuiteReport("single-agent baseline", multi.results[:1], [], Decimal(9))
    text = render_report([multi, single])
    assert "| multi |" in text and "| single-agent baseline |" in text


def test_load_tasks_from_toml(tmp_path: Path) -> None:
    (tmp_path / "b.toml").write_text('id = "b"\nprompt = "pb"\n[expected]\nv = "2"\n')
    (tmp_path / "a.toml").write_text('id = "a"\nprompt = "pa"\ntier = "hard"\n')
    loaded = load_tasks(tmp_path)
    assert [t.id for t in loaded] == ["a", "b"]
    assert loaded[0].tier == "hard" and loaded[1].tier == "untiered"
    assert loaded[1].expected == {"v": "2"}


def test_example_tasks_in_the_repo_load() -> None:
    repo_tasks = load_tasks(Path(__file__).resolve().parents[1] / "evals" / "tasks")
    assert {"example-01", "example-02"} <= {t.id for t in repo_tasks}
