# Evals

Tasks live in `evals/tasks/*.toml`, one file per task:

```toml
id = "task-id"
tier = "single_company"        # free text; shown in the report
prompt = "The question the system is asked."
[expected]                      # ground truth the rubric checks
revenue_latest = "..."
```

`example-01.toml` and `example-02.toml` are **examples**: their expected values are
placeholders. Real tasks need numbers you have checked against the XBRL data yourself.

## Workflow
1. Write 10-15 tasks (PLAN.md Phase 7), including a few adversarial ones.
2. Write the rubric yourself: `src/agent_orchestration/evals/rubric.py` (concept C12).
3. List the tasks without calling the API: `uv run python scripts/run_eval.py --dry-run`
4. Run for real from GitHub: Actions, "Evals", Run workflow, set `max_usd`. It never runs
   automatically. The run stops once the dollar cap is reached and the report lists any
   tasks it skipped.
5. Compare the multi-agent system with the single-agent baseline: the runner takes any
   function `prompt -> SystemOutput`, so both are scored by the same rubric.

Metrics: success rate, dollars per task, model turns per task.
