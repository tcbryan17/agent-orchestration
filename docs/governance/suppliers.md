# Suppliers

*Every outside service the system sends data to or receives data from. For each: what it receives, what it returns, the terms that matter, and what you checked. Items marked "to verify" were not checked against the supplier's current terms.*

| Supplier | Role | What it receives | What it returns | Key terms | Status of checks |
|---|---|---|---|---|---|
| Anthropic | Model provider (Claude Haiku 5.5, ADR 0002) | Prompts: system text, task, tool results (may include filing text and director names), tool definitions | Model responses and token usage | Data retention and training terms for API use; data processing terms; region of processing. All to verify | to verify |
| SEC EDGAR | Source of XBRL financial data | HTTP requests with a `User-Agent` (name and contact) | `companyfacts` JSON | Requests need a descriptive User-Agent; limit 10 requests per second; fair-access policy to verify | to verify |
| Companies House | Source of club accounts (Stage 2) | HTTP requests with the API key | Filing history and document content | Free API key sent as the Basic auth username; limit 600 requests per 5 minutes | to verify |
| GitHub | Hosts the public repo and CI | All code and docs; secrets stored as GitHub secrets | CI results, Dependabot alerts | Repo is public (ADR 0003); never commit secrets; gitleaks scan on PRs | to verify |
| (example) Hosting provider | Runs the demo (Phase 8) | Requests from visitors, the app and its logs | | Render or Fly, undecided | not chosen |

## Change watch
*Record how you notice a supplier change (a model retirement, a price change, new terms). See risk R-006 in `risk-register.md`.*

| Date | Supplier | Change | Action |
|---|---|---|---|
| (example) | | | |
