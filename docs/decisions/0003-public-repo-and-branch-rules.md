# 0003. Public repo, PR-only `main`

- **Status:** Accepted
- **Date:** 2026-11-14

## Context
All code must reach `main` through a feature branch, a pull request and green CI. On GitHub's free plan, branch protection and rulesets are enforced only on public repositories. The API returned 403 for this repo while it was private.

## Options considered
- **Make the repo public**: rules are enforced for free, and it's a portfolio piece anyway. The cost is that work in progress is visible.
- **GitHub Pro**: keeps the repo private with rules enforced; costs money for a repo that will be public eventually.
- **Convention only** (local hooks, no server enforcement): free, but nothing stops a mistaken push to `main`.

## Decision
Make the repo public. A ruleset on `main` requires a pull request, the `check` and `secrets` CI jobs to pass, and blocks force pushes and branch deletion. A local pre-commit hook (`no-commit-to-branch`) also catches commits made on `main` before they're pushed.

## Why
Enforcement on the server is the only kind that can't be skipped by accident. Being public also suits the project's purpose. Because the repo is public, the `gitleaks` scan runs on every PR.

## Consequences
- Branch names follow `<type>/<slug>` (`feat/`, `fix/`, `chore/`, `docs/`); PRs are squash-merged.
- As a solo developer, PRs need 0 approvals: the CI checks are the gate.
- No secret may ever be committed. Keys live in `.env` locally and as GitHub or hosting-platform secrets.
