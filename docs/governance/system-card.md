# System card

*A plain description of the system for a reader who has not seen the code. Fill in after Phase 7, when there are evaluation results. Keep claims small and checkable. Do not describe anything that is not built.*

## Intended use
Analysis of public company filings, for example comparing the finances of Premier League clubs and sports-betting operators. It produces a written comparison with sources. It is **not** investment advice and **not** betting advice or tips.

## Users
*Who will use it: portfolio visitors, allowlisted visitors with their own task, the owner. Describe how each is limited (rate limits, allowlist).*

## Out-of-scope uses
- Investment, trading or betting decisions.
- Any use that needs figures to be guaranteed correct.
- Analysis of private individuals.
- *Add others as you find them.*

## Models
Claude Haiku 5.5 (`claude-haiku-5-5`) for every agent, per ADR 0002. Any upgrade is per agent, on eval evidence, with its own ADR.

| Agent | Model | Prompt version | Notes |
|---|---|---|---|
| Supervisor (example) | claude-haiku-5-5 | to fill | |

## Data sources
SEC EDGAR XBRL (live) and a human-verified club dataset from Companies House accounts. See `data-card.md` and ADR 0004.

## Evaluation
*To fill after Phase 7: number of tasks, success rate, cost per task, turns per task, baseline comparison, known failure cases. Link the report.*

## Limitations
*Start with: accounting standards differ (US GAAP, IFRS, probably FRS 102; to verify); fiscal years differ; club data can lag by up to about 10 months; Haiku 5.5 may make planning errors; extraction accuracy of the club dataset is measured, not perfect.*

## Human oversight
*Describe the approval gate (C9), what the approver sees, and what happens with no response. Describe the budget and turn limits (C7). Do not describe a gate that does not exist yet.*

## AI disclosure
Users must be told they are interacting with an AI system, and the report must be marked as AI-generated (EU AI Act Art. 50 transparency; owner to verify the exact obligations against the Act's text). *Record where in the UI and the report this appears.*

## Risk tier
The likely EU AI Act tier is limited risk (transparency duties only). Financial analysis of company filings does not appear to be an Annex III use. The Annex III creditworthiness item concerns natural persons, not companies. **Owner to verify against the Act's text.** This is not legal advice.

## Change log
| Date | Change | Link |
|---|---|---|
| (example) | Card drafted | |
