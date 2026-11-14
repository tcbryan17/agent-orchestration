# 0004. Demo task and data sources: football finance analyst

- **Status:** Proposed
- **Date:** 2026-11-14

## Context
The demo task has to be gradeable without an LLM judge, replayable from saved data, actually in need of several specialist agents, safe for public use, and workable on Haiku (ADR 0002). The owner chose peer comparison from public financial filings, focused on the Premier League and sports betting, because it combines their finance background with their interests. Spike 0001 (`docs/spikes/0001-data-sources.md`) checked what data exists.

## Options considered
- **Betting operators only** (DraftKings, Flutter, Rush Street, via SEC XBRL): clean structured data and exact grading, but little Premier League content.
- **Clubs only** (via Companies House): the most engaging, but every club's accounts are image-only scanned PDFs, so the whole project would depend on OCR quality.
- **Both, staged: a "football finance analyst"**: operators and Manchester United through live structured tools first; other clubs added from a human-verified dataset extracted from the scanned accounts.

## Decision
The staged "football finance analyst":
1. **Stage 1:** a live `edgar_company_facts` tool for DraftKings, Flutter, Rush Street and Manchester United (US GAAP and IFRS). The engine, the evals and the governance controls are built against this data.
2. **Stage 2:** a club financials dataset for about six Premier League clubs. It's extracted once from the Companies House PDFs by a vision model, checked line by line by the owner, and stored in the repo with source page references. Agents read it through a `club_financials` tool and never OCR at run time.
3. **Default demo:** "A squad-cost-ratio and revenue-mix comparison of Manchester United and two other clubs under the 2026/27 rules". The fallback, if Stage 2 slips, is an operators-only comparison.
4. **Hardest eval tier:** the 2026/27 ban on gambling sponsors on the front of shirts: club exposure against operators' marketing response.

## Why
- Stage 1 gives us exact ground truth early, so evals and guardrails don't wait on data wrangling.
- Stage 2 turns the scanned-PDF problem into a governed data pipeline with lineage, human verification and a measured extraction-accuracy rate. That's a better governance story than live OCR, and it costs less to run.
- Three accounting standards and fiscal years that don't line up give the Analyst and Reviewer real finance controls to apply.

We trade away live club data and accept a curated dataset that lags by up to about 10 months, because club accounts are filed late anyway.

## Consequences
- Settings need `SEC_USER_AGENT` (a project alias) and `COMPANIES_HOUSE_API_KEY`.
- Stage 2 needs its own decision record: which model extracts the figures, the verification workflow, and the dataset format.
- The scanned PDFs aren't committed; only extracted figures with source references are. The Deloitte and UEFA reports are cited and never copied.
- Revisit Stage 2 if clubs start filing iXBRL accounts (then the bulk Accounts Data Product could replace extraction).
