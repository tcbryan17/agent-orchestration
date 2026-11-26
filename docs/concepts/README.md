# Concept guides

You type these twelve concepts yourself. Claude sets up the code around them and leaves a stub with a `TODO(human)`. Each guide lays out the options, what the tests check, and the questions an interviewer is likely to ask. The guides do not pick an option. You pick, then you write the code.

| Concept | Title | Stub location | Phase | Status |
|---|---|---|---|---|
| [C01](c01-agent-loop.md) | The agent loop | `src/agent_orchestration/loop.py: run_agent` | 2 | not started |
| [C02](c02-tool-dispatch.md) | Tool dispatch | `src/agent_orchestration/tools/dispatch.py: dispatch` | 3 | not started |
| [C03](c03-tool-schema.md) | Tool schema design | `src/agent_orchestration/tools/schemas.py: edgar_schema` | 3 | not started |
| [C04](c04-untrusted-tool-output.md) | Untrusted tool output | `src/agent_orchestration/tools/untrusted.py: wrap_result` | 3 | not started |
| [C05](c05-supervisor-handoff.md) | Supervisor handoff | `src/agent_orchestration/supervisor.py: delegate` | 4 | not started |
| [C06](c06-run-state.md) | Run state | `src/agent_orchestration/state.py: RunState` | 4 | not started |
| [C07](c07-budget-guardrails.md) | Budget guardrails | `src/agent_orchestration/guardrails.py: check_budget` | 5 | not started |
| [C08](c08-reviewer-loop.md) | Reviewer loop | `src/agent_orchestration/reviewer.py: review, next_step` | 5 | not started |
| [C09](c09-human-approval.md) | Human approval gate | `src/agent_orchestration/approval.py` | 5 | not started |
| [C10](c10-content-policy.md) | Content policy | `src/agent_orchestration/policy.py: check_policy` | 5 | not started |
| [C11](c11-audit-provenance.md) | Audit trail and provenance | `src/agent_orchestration/audit.py: chain_hash, canonical_bytes, verify_chain; src/agent_orchestration/provenance.py: check_claims` | 4-6 | not started |
| [C12](c12-eval-rubric.md) | Eval rubric | `src/agent_orchestration/evals/rubric.py: score` | 7 | not started |

## How to use a guide
1. Read the guide before you open the stub. Make sure you can explain each option in your own words.
2. Choose an option. If the guide says the choice is architectural, write an ADR first (see `docs/decisions/README.md`).
3. Type the code in the stub. Ask Claude to explain anything you do not follow.
4. Open the matching `tests/concepts/test_cNN_*.py` and delete the `pytestmark` line. Run `uv run pytest tests/concepts`. The tests check invariants only, so passing does not prove your choice is a good one.
5. Update the status in the table above and the stub's docstring.
6. Fill in the matching rows in `docs/governance/controls-map.md` with real evidence, and only then change a status from planned.

Every concept has its acceptance tests in `tests/concepts/`, skipped until you switch them on.
