# C09. Human approval gate

- **Stub:** `src/agent_orchestration/approval.py` (Phase 5)
- **Status:** not started
- **You type this.** Claude does not write it.

## The question

When must a person say yes before a result counts as final? And how does a run pause for that decision and carry on afterwards, given the run is a process that normally goes straight through?

## Where it sits

```
writer/reviewer done --> [gate] --pause--> awaiting_approval --API: approve/reject--> resume | stop
```

## Options

These are the options Claude has found. The list is not exhaustive and none is recommended: you choose, then you must be able to say why.

| Option | How it works | Pros | Cons | When you'd pick it |
|---|---|---|---|---|
| Gate only before publish | One approval before the deliverable is marked published | Light; matches the plan | Intermediate mistakes are not caught | Public demo with a single output |
| Also on guardrail trips | A human is asked when a cap or policy check fires | Human judges the edge cases | Needs someone to respond | Runs where stopping loses a lot of work |
| Every handoff | Approve each delegation | Maximum control | Not automation any more; slow | Training or high-risk settings |
| Pause and resume via API | Run state is saved; `POST /runs/{id}/approve` resumes it | Fits the SSE and Postgres design | Needs saved state (C6) and timeouts | Anything beyond a simple script |

## What the tests check

`tests/concepts/test_c09_human_approval.py`. These tests check invariants that any option must keep. They do not care which option you pick. They are skipped for now. When you have written the code, delete the `pytestmark` line at the top of the file to switch them on.

`tests/concepts/test_c09_human_approval.py` checks, for any option you pick:

- `test_request_is_recorded_in_the_log`
- `test_decision_records_who_decided`
- `test_a_request_cannot_be_resolved_twice`


Add one test of your own for the choice you made.

## Questions an interviewer might ask

1. What does a human approval add that the reviewer agent does not?
2. What does the approver actually see? Can they spot a hidden problem?
3. What happens if nobody answers?
4. How does the run pause and resume without losing state?
5. Could an approver be overwhelmed into rubber-stamping? What do you do about it?

## Governance link

EU AI Act: Art. 14 human oversight (voluntary here; it applies to high-risk systems). NIST AI RMF: GOVERN (accountability) and MANAGE. NIST AI 600-1: human-AI configuration (automation bias). ISO/IEC 42001: human oversight and responsible use (Annex A number to verify). GDPR Art. 22 is not engaged: no decisions about people.

Framework references name the area, not an exact clause, unless sure. Check the exact wording before you quote one.

## Write an ADR if

You make approval part of the run's lifecycle (pause and resume), because Phase 6's API and the data model depend on it.

Use the template in `docs/decisions/README.md`, include the options you rejected, and never edit an accepted record.
