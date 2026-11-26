# GDPR notes

*This covers both EU GDPR and UK GDPR with the Data Protection Act 2018, because you work in Europe and London. The rules are close but not identical; mark where they differ once you have checked. This is a working template, not legal advice. Everything marked "to confirm" or "to verify" needs checking against the law or a qualified adviser.*

## Record of processing
*Art. 30 asks for a record like this. A small project may be exempt from some duties; confirm whether that applies.*

| Data category | Purpose | Lawful basis | Retention | Where stored |
|---|---|---|---|---|
| Director data from filings (names, pay) | Financial analysis of public companies | Art. 6(1)(f) legitimate interests (to confirm) | to decide | EDGAR fixtures in repo (example); model prompts at the provider |
| Visitor task text | Run the task the visitor asked for | Art. 6(1)(f) (to confirm) | to decide | Run events in Postgres |
| IP addresses for rate limiting | Prevent abuse and cost overruns | Art. 6(1)(f) (to confirm) | to decide (short) | Rate limiter memory or host logs |
| Run events and audit log | Trace and audit runs | Art. 6(1)(f) (to confirm) | to decide | Postgres |
| Eval reports | Measure quality | Art. 6(1)(f) (to confirm) | to decide | Repo / CI artifacts |

## Legitimate interests assessment
*Three parts. Write full sentences.*

**Purpose.** What is the interest? *(Example: demonstrating an AI engineering system using public filings.)*

**Necessity.** Could the purpose be met with less personal data? *(Link to the minimisation notes below.)*

**Balancing.** What would a person reasonably expect? What is the effect on them? What safeguards reduce it?

## Data minimisation notes
- **C2:** which tools return personal data, and can they return less?
- **C4:** should director names and pay reach the model at all? Extract only the figures needed.
- **C5:** what is passed between agents, and does it include personal data?
- **C11:** keep personal data out of chained fields (see the erasure tension below).

## Retention
| Data | Retention period | Reason | Deletion method |
|---|---|---|---|
| (example) Run events for public demo | to decide | | |

## Data subject rights procedure
*Write the steps you would follow if someone asks. Include who answers, the deadline (one month under both regimes; confirm), and how you verify identity.*

| Right | Steps |
|---|---|
| Access (Art. 15) | to fill |
| Rectification (Art. 16) | to fill |
| Erasure (Art. 17) | to fill; see below |
| Objection (Art. 21), because legitimate interests is the basis | to fill |

**Erasure and the audit chain.** The audit log is hash-chained so edits are detectable. Deleting an event breaks the chain. Options in guide C11: keep personal data out of chained fields (hash a pointer), crypto-shredding, or redact before hashing. Record your choice here and in an ADR. Whether crypto-shredding counts as erasure: to verify.

## DPIA screening (Art. 35)
*A data protection impact assessment is needed for processing likely to be high risk (for example large-scale processing, profiling, special category data). Likely not mandatory here: the data is public, small in scale, and nobody is profiled. Write down why, date it, and revisit if scope changes. To confirm against the regulator's guidance (EDPB or ICO lists).*

| Screening question | Answer | Date |
|---|---|---|
| Large-scale processing of personal data? | to fill | |
| Special category data? | to fill | |
| Automated decisions with legal effect on people? | to fill | |

## International transfers
Prompts go to Anthropic, a US provider. Record the transfer mechanism and the provider's data processing terms: whether a data processing agreement applies, which standard contractual clauses or adequacy decision (for example the EU-US Data Privacy Framework) covers the transfer, and whether the UK addendum applies. All to verify against the provider's current terms. Also record where Postgres and the host run.

## Not legal advice
This document is a learning aid. Before running a public service that handles visitors' data, check these points with a qualified adviser or the ICO and your EU regulator's guidance.
