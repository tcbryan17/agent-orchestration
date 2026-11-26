# Governance documents

These are templates for you to fill in as the project grows. Nothing here claims a control exists. A row only moves to "implemented" when you can point at a file, a test or a log that proves it.

| File | What it is | Fill it in when |
|---|---|---|
| `controls-map.md` | Maps framework requirements to concept IDs (C1 to C12) and to evidence in the repo | Each phase lands; update the status then |
| `risk-register.md` | The risks of this system, how likely and how bad, and which controls treat them | Review after every phase and after the evals |
| `system-card.md` | A plain description of what the system is for, its limits and its oversight | Draft now, finish after Phase 7 |
| `data-card.md` | Where the data comes from, its licences, known gaps and personal data | When Stage 1 tools and the Stage 2 dataset exist |
| `gdpr.md` | EU and UK GDPR notes: record of processing, legitimate interests, rights, transfers | Before the demo is public |
| `suppliers.md` | The outside services the system uses and what each one receives | When you add or change a service |

Concept guides are in `docs/concepts/`. Decisions are in `docs/decisions/`.

## What this is and is not
Mapping practices to NIST AI RMF, NIST AI 600-1, the EU AI Act, ISO/IEC 42001, OWASP and GDPR shows an approach. It is not certification, an audit or legal advice. Do not say the project "complies with" anything. Say "maps to" or "is informed by", and point at the evidence.

Where a document says "to verify", the fact was not checked against a primary source. Check it before you rely on it or repeat it in an interview.

## How to fill a row
1. Write the requirement in your own words.
2. Name the repo evidence: a file path, a test name, or a log field.
3. Set the status honestly: planned (nothing yet), partial (some of it), implemented (evidence exists and you have run it).
