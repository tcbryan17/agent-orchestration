# Architecture Decision Records

One short file per significant decision, numbered in order (`0001-short-title.md`). Write a record when the decision changes the system's shape or would be costly to reverse. Skip small choices.

A record is never edited after the fact. If a decision changes, write a new record that supersedes it, and update the old record's status.

| # | Decision | Status |
|---|----------|--------|
| [0001](0001-hand-rolled-agent-loop.md) | Hand-rolled agent loop on the `anthropic` SDK | Accepted |
| [0002](0002-haiku-first-models.md) | Every agent starts on Claude Haiku 5.5; upgrade per agent only on eval evidence | Accepted |
| [0003](0003-public-repo-and-branch-rules.md) | Public repo, PR-only `main` enforced by a GitHub ruleset | Accepted |
| [0004](0004-demo-task-and-data-sources.md) | Football finance analyst: SEC XBRL live + human-verified club dataset | Proposed |

## Template

```markdown
# NNNN. Title

- **Status:** Proposed | Accepted | Superseded by NNNN
- **Date:** YYYY-MM-DD

## Context
The problem and the constraints that matter here.

## Options considered
- **Option A**: pros / cons
- **Option B**: pros / cons

## Decision
What we chose.

## Why
The reasoning, including what we're trading away.

## Consequences
What this makes easier or harder later, and what would make us revisit it.
```
