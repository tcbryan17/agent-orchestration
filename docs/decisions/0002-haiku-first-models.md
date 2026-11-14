# 0002. Every agent starts on Claude Haiku 5.5

- **Status:** Accepted
- **Date:** 2026-11-14

## Context
Five agents (supervisor, researcher, analyst, writer, reviewer) each make several calls per run, and a public demo multiplies that. Cost per completed task is a headline metric for this project.

Prices per million tokens at decision time:

| Model | Input | Output |
|---|---|---|
| Claude Haiku 5.5 | $0.10 ($0.50 above 100K prompt tokens) | $0.50 ($2.50 above 100K) |
| Claude Sonnet 5.5 | $2.00 | $10.00 |
| Claude Opus 5.5 | $4.00 | $20.00 |

## Options considered
- **Opus everywhere, tuned down by effort level**: highest quality ceiling; about 40× Haiku's per-token price.
- **Opus supervisor, cheaper workers**: the common pattern; it assumes the supervisor needs the strongest model before we have measured that.
- **Haiku everywhere, upgrade on evidence**: cheapest baseline. Each upgrade must be justified by an eval result.

## Decision
Every agent defaults to `claude-haiku-5-5`. The model is set per agent in config, so one agent can be upgraded with a one-line change. An upgrade happens only when the eval (Phase 7) shows that agent is the bottleneck, and each upgrade gets its own record with before/after numbers.

## Why
It turns model choice into a measured result rather than a guess, and keeps the public demo cheap to run. We accept that early runs may fail in ways a stronger model wouldn't. Those failures are useful: they show where capability actually matters in a multi-agent system.

## Consequences
- The cost calculator must handle Haiku 5.5's two price tiers (the 100K-token threshold).
- Some server tools and API features support only certain models. Check each against Haiku 5.5 before using it (web search version first, in Phase 3).
- Haiku 5.5 has no server-side refusal fallback, so the loop has to handle `stop_reason: "refusal"` itself.
- The supervisor is the most likely first upgrade. Watch for planning and handoff errors in the eval.
