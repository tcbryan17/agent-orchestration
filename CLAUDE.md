# CLAUDE.md

Guidance for Claude Code, and context for anyone (human or AI) working in this repo.

## What this is
A supervisor agent breaks a business task into steps and delegates to specialist agents (researcher, analyst, writer, reviewer). Every step is traced: which agent ran, which tools it called, tokens, latency and cost. The portfolio site (`../portfolio-site`) replays one recorded run. See `README.md` and `docs/PLAN.md`.

**This is a learning-first portfolio project.** The owner must be able to explain every important piece in an interview or to a customer. Building it is only half the goal.

## How we work together
- **The owner types the core concepts.** That means the agent loop and `stop_reason` handling, tool schemas and dispatch, supervisor handoff and the context boundary, the reviewer loop and how it terminates, turn and dollar guardrails, cost from `usage`, the event schema, and the eval rubric. For these, Claude sets up the surrounding code, leaves a single `TODO(human)`, explains the trade-offs, and waits. Claude does not write them.
- **Claude writes boilerplate**: project config, CI, FastAPI/SSE plumbing, DB models, Docker, fakes for tests, export scripts.
- **Small choices: just decide** and mention the choice in one line. **Architectural choices: ask** with options and a recommendation, then record the decision in `docs/decisions/` (never edit an accepted record; supersede it).
- Explain *why* something works, not just *what* it does.
- **Subagents (owner's standing preference):** use them where appropriate, such as parallel research, broad searches and independent lookups. Pick the model by difficulty: **Sonnet** for moderately complex work, **Haiku** for simple lookups. Core concepts the owner types are never delegated.

## Branching and CI/CD
- Never commit to `main`. Work on `<type>/<slug>` branches (`feat/`, `fix/`, `chore/`, `docs/`), open a PR, let CI pass, squash-merge. A GitHub ruleset enforces this (ADR 0003); a pre-commit hook catches local mistakes.
- The owner merges PRs. Claude opens them.
- CI must never need an API key: tests use a fake client. Live tests are marked `live` and run only with `-m live`.
- **Never check out a PR from an outside contributor locally.** Its `pyproject.toml`, `uv.lock`, pre-commit config, `.claude/settings.json` and `CLAUDE.md` would run or load on the owner's machine. Review outside PRs on GitHub only.
- Commits use the owner's GitHub no-reply address (set in this repo's local git config), never a personal email.

## Secrets
- **Claude must never read, print, edit or source `.env` files** (`.env`, `.env.local`, `.env.*`) anywhere in this repo. This is enforced, not just requested: `permissions.deny` rules in `.claude/settings.json`, plus the owner's user-level Bash hook (`~/.claude/hooks/block-env-bash.sh`). `.env.example` is allowed and must stay up to date when config is added.
- When a config value is needed, ask the owner or read it through `settings` in code. Secrets are `SecretStr`.

## Commands
```bash
cp .env.example .env            # first time only, then the owner fills in the key
uv sync                         # install deps into .venv
uv run pre-commit install       # one-time: lint/format/mypy + no-commit-to-main before each commit
uv run pytest                   # tests (live tests skipped)
uv run pytest -m live           # real API calls; costs money, owner runs explicitly
uv run mypy src tests           # type check (strict)
uv run ruff check .             # lint
uv run ruff format .            # format
```
Before calling work done, run pytest, mypy and ruff check.

Under Claude Code's Bash sandbox, `uv` can't write its usual cache, so prefix commands (including `git commit`, whose hooks call `uv run`) with `UV_CACHE_DIR="$TMPDIR/uvcache"`.

## Conventions
- Python 3.12, managed by `uv`, src layout: `src/agent_orchestration/`.
- Model calls use the official `anthropic` SDK directly with a hand-rolled loop (ADR 0001). No agent frameworks.
- Every agent defaults to `claude-haiku-5-5` (ADR 0002). Models are set per agent; upgrades need eval evidence and an ADR.
- The event schema is a contract with the portfolio site's replay. Change both together.

## Current status (updated 2026-11-15)
**Done:**
- Phase 0: repo setup (PR #1).
- Data-source spike (`docs/spikes/0001-data-sources.md`) and ADR 0004 (accepted) (PR #2): a "football finance analyst". Stage 1 uses live SEC XBRL for DraftKings, Flutter, Rush Street and Man Utd. Stage 2 adds a human-verified Premier League club dataset extracted from scanned Companies House accounts.
- Phase 1: event schema and cost tracking (PR #3, ready for the owner to merge).
  - `events.py` (owner-designed): a frozen `Event` with `run_id`/`event_id`/`parent_id` (a tree, for provenance), a recorder-assigned `seq` for order plus a UTC-aware `ts`, `agent`/`type`/`text`/`payload`, and model-call fields (`model`, `usage`, `Decimal` `cost_usd`, `latency_ms`).
  - `pricing.py`: `cost_from_usage()` (owner-implemented). Haiku 5.5 rates were checked against the pricing page on 2026-11-15. A prompt over 100K tokens (input + cache writes + cache reads) reprices the whole request. Unknown models raise `KeyError`.
  - `replay.py`: `to_site_events()` exports to the site's `{t, who, text}` format, with real elapsed time, hidden model calls and tool results, and run totals on the last line. There's no CLI script yet; it waits for the recorder's file format in Phase 2.
  - 28 tests, including the `Event` guarantees and the pricing edge cases.
- Security review (2026-11-15): no secrets in files or history, no known dependency vulnerabilities, CI can't reach secrets from PRs. Dependabot is on.

**Next: Phase 2, the agent loop** (`feat/agent-loop`). The owner types the loop and `stop_reason` handling. Claude scaffolds the fake client for tests and the recorder that assigns `seq`. Tool results from SEC/Companies House are untrusted text going into a model that can call tools, so design the dispatch with prompt injection in mind.

**Owner to-dos:**
- Add `COMPANIES_HOUSE_API_KEY` and `SEC_USER_AGENT` (a project alias) to `.env`.
- Create an Anthropic API key with a spend limit before Phase 2.
- GitHub account: turn on "Keep my email addresses private" and "Block command line pushes that expose my email"; check `gh auth status` scopes, 2FA, PATs, OAuth apps, SSH keys and webhooks. Decide whether to remove the personal email from older commits.
- Optional: a `chore/` PR pinning the pre-commit hooks and GitHub Actions to commit SHAs.

**Governance thread:** see `docs/PLAN.md` (NIST AI RMF, ISO 42001). The hash-chained audit log builds on the Event schema.
