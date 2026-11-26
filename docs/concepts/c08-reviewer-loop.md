# C08. Reviewer loop

- **Stub:** `src/agent_orchestration/reviewer.py: review, next_step` (Phase 5)
- **Status:** not started
- **You type this.** Claude does not write it.

## The question

The reviewer reads the draft and either approves it or sends it back. What form does its verdict take, and how does the loop end when the reviewer keeps saying no? A loop with no exit is a cost and quality risk.

## Where it sits

```
writer -> reviewer -> approve ------------------> done
              |
              +-> revise(notes) -> writer -> reviewer ...   (max_revisions)
                         on the cap: ship with caveat | fail | escalate to a human (C9)
```

## Options

These are the options Claude has found. The list is not exhaustive and none is recommended: you choose, then you must be able to say why.

| Option | How it works | Pros | Cons | When you'd pick it |
|---|---|---|---|---|
| Approve / revise + notes | Reviewer returns a verdict and free-text notes | Simple; easy to log | Vague notes; no measure of quality | First version |
| Scored rubric | Reviewer scores fixed criteria (sources present, periods aligned, standards noted) | Specific feedback; measurable; can feed evals | More prompt design; scores can be inconsistent | When the reviewer's checks are the governance control |
| On max revisions: ship with caveat | Publish the last draft with a visible warning | User gets something | Unreviewed content reaches the user | Low-stakes drafts |
| On max revisions: fail | Stop and report failure | Nothing bad is published | Wasted spend; poor demo | When correctness matters more than output |
| On max revisions: escalate | Hand to a human (C9) | Human decides | Needs a UI and someone to answer | Deliverables that count as published |

## What the tests check

`tests/concepts/test_c08_reviewer_loop.py`. These tests check invariants that any option must keep. They do not care which option you pick. They are skipped for now. When you have written the code, delete the `pytestmark` line at the top of the file to switch them on.

`tests/concepts/test_c08_reviewer_loop.py` checks, for any option you pick:

- `test_approved_ships`
- `test_revise_under_the_cap_asks_for_a_revision`
- `test_revise_at_the_cap_never_asks_for_another_revision`
- `test_next_step_is_deterministic`


Add one test of your own for the choice you made.

## Questions an interviewer might ask

1. How does your loop terminate? Prove it cannot run for ever.
2. Why use a different model or prompt for the reviewer than the writer?
3. What does the reviewer check that the writer cannot check itself?
4. What happens at the revision cap and why did you choose that?
5. How do you know the reviewer is any good? How would you measure it?

## Governance link

NIST AI RMF: MEASURE (testing outputs against criteria) and MANAGE. NIST AI 600-1: confabulation and information integrity (rejecting claims without a source). EU AI Act: Art. 14 human oversight (if escalating), Art. 15 accuracy, both voluntary here. ISO/IEC 42001: verification and validation (Annex A number to verify).

Framework references name the area, not an exact clause, unless sure. Check the exact wording before you quote one.

## Write an ADR if

You decide what happens at the revision cap, or you adopt a rubric the evals depend on.

Use the template in `docs/decisions/README.md`, include the options you rejected, and never edit an accepted record.
