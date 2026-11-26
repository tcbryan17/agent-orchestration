# Risk register

*One row per risk. Likelihood and impact use Low / Medium / High, set by you after thinking about this deployment. Controls are concept IDs (C1 to C12) and must match `controls-map.md`. Review after each phase and after the evals. Rows below are seeds with ratings left blank on purpose: rate them yourself.*

NIST AI 600-1 category names used here: Confabulation, Information Integrity, Information Security, Data Privacy, Value Chain and Component Integration, Intellectual Property, Harmful content areas. Check the exact names against the document.

| ID | Risk | NIST AI 600-1 category | Likelihood | Impact | Controls (concept IDs) | Owner | Status |
|---|---|---|---|---|---|---|---|
| R-001 | Fabricated figures: the report states a number no tool returned, or a wrong one | Confabulation | to rate | to rate | C8, C11, C12 | Toby | open |
| R-002 | Prompt injection via filings: text in a filing or web page tries to steer an agent | Information Security | to rate | to rate | C2, C4, C10 | Toby | open |
| R-003 | Runaway cost: a loop or a public visitor burns the API budget | Information Security (abuse); Value Chain | to rate | to rate | C1, C7, C9 | Toby | open |
| R-004 | Betting-tip content: the report reads as tips, inducements or investment advice | Information Integrity; harmful content | to rate | to rate | C8, C10 | Toby | open |
| R-005 | Personal data in traces: director names and pay end up in logs or model prompts | Data Privacy | to rate | to rate | C4, C5, C11 | Toby | open |
| R-006 | Third-party model change: the provider updates or retires a model and behaviour or price shifts | Value Chain and Component Integration | to rate | to rate | C12 | Toby | open |
| R-007 | Copyrighted report text: outputs reproduce text from copyrighted reports (e.g. industry reports) | Intellectual Property | to rate | to rate | C10 | Toby | open |
| R-008 (example) | Unaligned fiscal years or accounting standards produce a misleading comparison | Confabulation; Information Integrity | to rate | to rate | C8 | Toby | open |

## Rating guide
- **Likelihood:** Low = unlikely in the demo's life; Medium = could happen; High = expect it.
- **Impact:** Low = a wrong demo answer; Medium = misleading output reaches a visitor; High = financial loss, legal exposure or a leak.
- Write the reason beside each rating in the notes below, so you can defend it.

## Notes
*One short paragraph per risk: what you decided and why.*
