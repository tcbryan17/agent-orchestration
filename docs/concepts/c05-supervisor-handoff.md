# C05. Supervisor handoff

- **Stub:** `src/agent_orchestration/supervisor.py: delegate` (Phase 4)
- **Status:** not started
- **You type this.** Claude does not write it.

## The question

The supervisor hands a sub-task to a worker, which starts a fresh loop. What does the worker get to see, and what comes back? This is the context boundary: it decides cost, quality, and how much untrusted text can travel between agents.

## Where it sits

```
Supervisor messages[]  --brief-->  Worker (fresh messages[])
                       <--result--  (transcript | summary | structured result + source event IDs)
```

## Options

These are the options Claude has found. The list is not exhaustive and none is recommended: you choose, then you must be able to say why.

| Option | How it works | Pros | Cons | When you'd pick it |
|---|---|---|---|---|
| In: brief only | The worker gets only a written task | Cheapest; strongest isolation | The brief must be complete or the worker guesses | Independent sub-tasks |
| In: brief + artifacts | The brief plus named outputs of earlier workers, passed by value | Workers can build on each other without the whole history | Supervisor must pick the right artifacts | Pipelines such as researcher -> analyst -> writer |
| In: full history | Copy the supervisor's whole conversation | Nothing is missed | Expensive; leaks injected text from earlier tool output; breaks isolation | Almost never |
| Out: full transcript | Return everything the worker did | Complete | Fills the supervisor's context; carries untrusted text upward | Debugging only |
| Out: summary | Return the worker's own short summary | Small | Sources and numbers can be lost or changed | Tasks where provenance does not matter |
| Out: structured result with source event IDs | Return typed fields plus the IDs of the events that produced each fact | Supports provenance (C11); easy to check | More schema to design | A finance deliverable where each figure needs a source |

## What the tests check

`tests/concepts/test_c05_supervisor_handoff.py`. These tests check invariants that any option must keep. They do not care which option you pick. They are skipped for now. When you have written the code, delete the `pytestmark` line at the top of the file to switch them on.

`tests/concepts/test_c05_supervisor_handoff.py` checks, for any option you pick:

- `test_worker_gets_a_fresh_conversation_containing_the_brief`
- `test_worker_uses_its_own_model_prompt_and_only_its_own_tools`
- `test_handoff_is_recorded_and_worker_events_hang_off_the_run_tree`


Add one test of your own for the choice you made.

## Questions an interviewer might ask

1. What exactly does a worker see? What is deliberately hidden from it?
2. Why not just give every worker the full history?
3. How does the supervisor know where a number in the report came from?
4. What happens when a worker fails or returns something malformed?
5. Handoffs must work with `tool_choice: auto`. How do you make sure the supervisor delegates?

## Governance link

NIST AI RMF: MAP (roles and boundaries of each component) and GOVERN (accountability for each agent). NIST AI 600-1: information integrity, value chain and component integration. OWASP LLM Top 10: excessive agency and prompt injection. ISO/IEC 42001: Annex A areas on responsibilities and data for AI systems (numbers to verify). GDPR: Art. 5(1)(c) minimisation applies to what is passed between agents.

Framework references name the area, not an exact clause, unless sure. Check the exact wording before you quote one.

## Write an ADR if

You choose the handoff contract (what goes in, what comes out). Other agents' prompts and the audit trail depend on it.

Use the template in `docs/decisions/README.md`, include the options you rejected, and never edit an accepted record.
