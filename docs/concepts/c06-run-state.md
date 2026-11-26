# C06. Run state

- **Stub:** `src/agent_orchestration/state.py: RunState` (Phase 4)
- **Status:** not started
- **You type this.** Claude does not write it.

## The question

Where does the truth about a run live while it is going on: in an event log you replay, or in an object you update? And do agents share a scratchpad or pass results by value? This decides how easy replay, audit and debugging are.

## Where it sits

```
events (append-only)  --fold-->  RunState (derived view)      [event sourcing]
RunState (mutated in place) + events written on the side       [mutable state]
```

## Options

These are the options Claude has found. The list is not exhaustive and none is recommended: you choose, then you must be able to say why.

| Option | How it works | Pros | Cons | When you'd pick it |
|---|---|---|---|---|
| Event sourcing | State is computed from the event log | Replay and audit come free; one source of truth; matches `Spend.from_events` | Recomputing can be slow on long runs; needs care in design | When the log already has to be trusted (C11) |
| Mutable state | An object updated in place, with events logged separately | Simple to write and read | State and log can disagree; replay is not guaranteed | Short runs where the log is only for display |
| Shared scratchpad | All agents read and write one workspace | Easy collaboration | Any agent can alter another's data; untrusted text spreads; hard to attribute | Single-agent runs or trusted agents |
| Artifacts by value | Each agent returns an immutable result; the supervisor passes copies on | Clear provenance; matches the append-only rule | Copies cost tokens; no live sharing | Multi-agent runs that need an audit trail |

## What the tests check

`tests/concepts/test_c06_run_state.py`. These tests check invariants that any option must keep. They do not care which option you pick. They are skipped for now. When you have written the code, delete the `pytestmark` line at the top of the file to switch them on.

`tests/concepts/test_c06_run_state.py` checks, for any option you pick:

- `test_empty_log_is_a_valid_fresh_state`
- `test_rebuilding_twice_gives_the_same_state`
- `test_state_does_not_depend_on_input_order`
- `test_more_events_never_remove_information`


Add one test of your own for the choice you made.

## Questions an interviewer might ask

1. If the process crashes mid-run, what can you recover and from where?
2. Can you rebuild the totals shown in the UI from the event log alone? Show me.
3. Why not let agents share a scratchpad? What would go wrong with an injected worker?
4. How do you avoid the state and the log disagreeing?
5. What is the cost of replaying a long run?

## Governance link

NIST AI RMF: MEASURE (reliable records for assessment) and MANAGE (the ability to reproduce and investigate incidents). EU AI Act: Art. 12-style record-keeping, voluntary here. ISO/IEC 42001: lifecycle and event logging (Annex A number to verify). NIST AI 600-1: information integrity.

Framework references name the area, not an exact clause, unless sure. Check the exact wording before you quote one.

## Write an ADR if

You pick event sourcing or mutable state, because the API (Phase 6), replay and the audit chain all depend on it.

Use the template in `docs/decisions/README.md`, include the options you rejected, and never edit an accepted record.
