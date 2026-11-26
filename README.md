# 02 · Agent Orchestration Console

> Part of my AI projects portfolio → **https://tcbryan17.github.io** · See the other projects there.

A supervisor agent breaks a business task into steps and delegates to specialist agents. Every step is visible: which agent ran, which tools it called, and the tokens, latency, and cost.

## Agents (initial set)
| Agent | Job | Tools |
|-------|-----|-------|
| Supervisor | Plan, delegate, decide when it's done | delegate_* (one per worker), finish |
| Researcher | Gather facts | edgar_company_facts (SEC XBRL); club_financials in Stage 2 ([ADR 0004](docs/decisions/0004-demo-task-and-data-sources.md)) |
| Analyst | Structure and compare | build_table, calculator |
| Writer | Produce the deliverable | — |
| Reviewer | Critique, send back or approve | — |

## Stack
Python 3.12 · a hand-rolled agent loop on the `anthropic` SDK ([ADR 0001](docs/decisions/0001-hand-rolled-agent-loop.md)) · Claude Haiku 5.5 by default, upgraded per agent only on eval evidence ([ADR 0002](docs/decisions/0002-haiku-first-models.md)) · FastAPI with Server-Sent Events · Postgres for run history

## Event stream (used by the site)
```
GET /runs/{id}/events   (text/event-stream)
```
Every step emits one frozen `Event` ([`events.py`](src/agent_orchestration/events.py)): which run and which parent step it belongs to, its order (`seq`) and time, the agent, the kind of step, and for model calls the model, token usage, exact `Decimal` cost and latency. The UI renders events as a live timeline. One run's events are saved to `replay/`, and [`replay.py`](src/agent_orchestration/replay.py) converts them to the `{t, who, text}` format the portfolio site's replay player reads.

## Development
```bash
uv sync && uv run pre-commit install
uv run pytest && uv run mypy src tests && uv run ruff check .
```
All changes go through a branch, a PR and green CI ([ADR 0003](docs/decisions/0003-public-repo-and-branch-rules.md)). Decisions are recorded in [`docs/decisions/`](docs/decisions/).

## Guardrails
- A hard cap on agent turns and dollars per run
- A rate-limited public demo, plus a "bring your own task" option only for allowlisted visitors

## Status
Phase 1 (event schema and cost tracking) is complete. Phases 2 to 7 are scaffolded: the plumbing is built and each core concept is a stub I write by hand, with a guide in [docs/concepts/](docs/concepts/) and acceptance tests in `tests/concepts/`. Next is C1, the agent loop. The demo task is a **football finance analyst** comparing Premier League clubs and sports-betting operators from their public filings ([ADR 0004](docs/decisions/0004-demo-task-and-data-sources.md)). Plan: [docs/PLAN.md](docs/PLAN.md). Governance: [docs/governance/](docs/governance/).
