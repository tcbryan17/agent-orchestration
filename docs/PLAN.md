# Build plan

Each phase is one branch and one PR. In the **You type** column are the concepts the owner writes by hand, with guidance. Claude scaffolds everything else.

## Architecture

```
POST /runs {task}
   │
   ▼
Supervisor (manual loop, ADR 0001)
   tools: delegate_researcher · delegate_analyst · delegate_writer · delegate_reviewer · finish
   │   each delegate_* call starts a FRESH worker loop with its own messages[]
   ├─▶ Researcher  (web search) ───────────────┐
   ├─▶ Analyst     (calculator, build_table)   ├─ result returns as the supervisor's tool_result
   ├─▶ Writer                                  │
   └─▶ Reviewer ── approve | revise(notes) ────┘
   │
   every step ──▶ Event(run_id, seq, ts, parent_id, agent, type, text, usage, cost_usd, …)
                    ├─▶ Postgres (run history)
                    └─▶ SSE  GET /runs/{id}/events ──▶ live timeline
                                       └─▶ export ──▶ replay/sample-run.json ──▶ portfolio site
```

The backend emits the full event format. An export script converts it to the site's replay format (`{t, who, text}`), the same approach as `multimodal-doc-rag`'s `export_site_replay.py`.

## Phases

| # | Branch | Goal | You type |
|---|---|---|---|
| 0 ✅ | `chore/repo-setup` | CLAUDE.md, settings, CI, secret scan, ADRs 0001–0003 | — (decided branch rules) |
| 1 ✅ | `feat/event-schema` | Event model and cost tracking | Event schema; `cost_from_usage()` including Haiku's 100K price tier |
| 2 | `feat/agent-loop` | One agent completes a task with tools | **The loop**: `stop_reason` handling, tool results, error results |
| 3 | `feat/tools` | Researcher and Analyst tools | One `strict` tool schema plus the dispatcher |
| 4 | `feat/supervisor` | Delegation to workers | **The handoff and the context boundary** |
| 5 | `feat/review-guardrails` | Reviewer loop and limits | Termination: max turns, max $, max revisions |
| 6 | `feat/api-sse` | `POST /runs`, SSE stream, Postgres | How a running agent feeds the SSE stream |
| 7 | `feat/evals` | 10–15 tasks: success rate, $/task, turns/task, compared with a single-agent baseline | The grading rubric |
| 8 | `feat/deploy-replay` | Rate-limited deploy, recorded run, site update | — (review) |

## Constraints to design around
- **Models (ADR 0002):** every agent starts on Haiku 5.5 and is upgraded per agent only on eval evidence.
- **Handoffs:** the supervisor's delegation must work with `tool_choice: auto`, strict tool schemas and prompt steering. Forced tool choice isn't available on every model, so don't depend on it.
- **Append-only history:** workers get a fresh `messages` list and never an edited copy of the supervisor's.
- **The loop must handle** `end_turn`, `tool_use`, `max_tokens`, `refusal` and `pause_turn`.
- **Guardrails:** a hard cap on turns and dollars per run, checked *before* each API call.

## CI/CD
- **PR → CI:** ruff, format check, mypy (strict), pytest with a fake client (no key, no spend), and a gitleaks secret scan.
- **Evals:** a manually triggered workflow with the API key stored as a GitHub secret and a hard cost cap. Never runs automatically.
- **Merge to `main`:** deploy, with secrets stored on the hosting platform only.

## Governance and auditability (cross-cutting, scope expansion)
Governance runs through every phase rather than being added at the end. The owner wants it to line up with **NIST AI RMF 1.0** (Govern / Map / Measure / Manage), its **Generative AI Profile (NIST AI 600-1)**, and **ISO/IEC 42001** (AI management system). Candidate pieces, to be confirmed at scoping:
- **Tamper-evident audit trail:** the event log is append-only and hash-chained, so any edit to past events is detectable. *(owner types)*
- **Provenance:** every figure in a deliverable links to the source document and the tool call that fetched it. The Reviewer rejects claims without a source. *(owner types)*
- **Policy guardrails:** for example, no betting tips or inducements in a betting-domain deliverable. Red-team prompts go into the eval set. *(owner types)*
- **Reproducibility record per run:** model IDs, prompt versions, tool versions, settings.
- **Human approval gate** before a deliverable counts as "published".
- **Governance documents:** a risk register, a system card, and a controls map from NIST AI RMF subcategories and ISO 42001 requirements to concrete repo artifacts (ADRs, tests, logs, CI). *(owner writes, with guidance)*

Mapping practices to a framework shows an approach. It is not certification or a compliance claim.

## Open decisions
- ~~Demo task~~: **decided** in ADR 0004. It's a football finance analyst: live SEC XBRL for betting operators and Man Utd (Stage 1), then a human-verified club dataset (Stage 2).
- **Hosting:** Render or Fly, decided at Phase 8.
- **OpenTelemetry:** stretch goal. Our own event log is the trace; OTel export is optional.
