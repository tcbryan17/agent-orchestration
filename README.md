# 02 · Agent Orchestration Console

> Part of my AI projects portfolio → **https://tcbryan17.github.io** · See the other projects there.

A supervisor agent breaks a business task into steps and delegates to specialist agents. Every step is visible: which agent ran, which tools it called, and the tokens, latency, and cost.

## Agents (initial set)
| Agent | Job | Tools |
|-------|-----|-------|
| Supervisor | Plan, delegate, decide when it's done | handoff |
| Researcher | Gather facts | web_search, fetch_url |
| Analyst | Structure and compare | build_table, calculator |
| Writer | Produce the deliverable | — |
| Reviewer | Critique, send back or approve | — |

## Planned stack
Python · Claude Agent SDK (or a hand-rolled loop) · FastAPI with Server-Sent Events · Postgres for run history · OpenTelemetry traces

## Event stream (used by the site)
```
GET /runs/{id}/events   (text/event-stream)
data: { "t": ms, "agent": str, "type": "plan|tool_call|tool_result|message|handoff|done",
        "text": str, "tokens": int, "cost_usd": float }
```
The UI renders these as a live timeline. Save one run's events to `replay/sample-run.json`. The portfolio site plays it as this project's demo.

## Guardrails
- A hard cap on agent turns and dollars per run
- A rate-limited public demo, plus a "bring your own task" option only for allowlisted visitors

## Status
Planned
