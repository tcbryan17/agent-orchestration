# C12. Eval rubric

- **Stub:** `src/agent_orchestration/evals/rubric.py: score` (Phase 7)
- **Status:** not started
- **You type this.** Claude does not write it.

## The question

How do you decide, with numbers, whether the system did a task correctly, and whether the multi-agent design is worth its cost compared with one agent? The rubric is what turns "it seems to work" into evidence.

## Where it sits

```
task + ground truth (SEC XBRL values) --> run --> score(output, truth) --> success, $ / task, turns / task
same tasks --> single-agent baseline --> compare
```

## Options

These are the options Claude has found. The list is not exhaustive and none is recommended: you choose, then you must be able to say why.

| Option | How it works | Pros | Cons | When you'd pick it |
|---|---|---|---|---|
| Numeric tolerance | Compare extracted numbers to known values within a tolerance | Objective, free, repeatable; Stage 1 has exact ground truth | Only checks numbers, not reasoning or wording | Fact and calculation tasks |
| LLM judge | A model grades the report against a rubric | Covers narrative and structure | Costs money; has bias; needs calibration | Qualitative criteria such as caveats stated |
| Both | Numeric check plus a judge for the rest | Wide coverage | More to build and explain | The full eval |
| Metrics: success rate, $/task, turns/task | Per-task and aggregate | Matches what the README promises | Averages hide bad tails; report distribution too | Always |
| Single-agent baseline | Same tasks, one agent with all the tools | Shows whether the supervisor design is justified | Needs another harness | Always, if you claim multi-agent helps |
| Judge calibration | Compare the judge's grades to your own on a sample | Tells you if you can trust it | Costs your time | Whenever a judge is used |

## What the tests check

`tests/concepts/test_c12_eval_rubric.py`. These tests check invariants that any option must keep. They do not care which option you pick. They are skipped for now. When you have written the code, delete the `pytestmark` line at the top of the file to switch them on.

`tests/concepts/test_c12_eval_rubric.py` checks, for any option you pick:

- `test_empty_answer_does_not_pass`
- `test_same_input_same_score`
- `test_score_ignores_cost_and_turns`
- `test_a_clearly_wrong_number_does_not_pass`


Add one test of your own for the choice you made.

## Questions an interviewer might ask

1. How do you know the multi-agent version is better than one agent? Show the numbers.
2. What tolerance did you pick for numbers and why?
3. How do you stop the judge model from favouring its own style?
4. How many tasks do you have, and is that enough to say anything? What is the uncertainty?
5. What would you do if the cheaper single agent scored the same?

## Governance link

NIST AI RMF: MEASURE (metrics, test sets, comparing with a baseline). NIST AI 600-1: confabulation (measured error rate). EU AI Act: Art. 15 accuracy and robustness (voluntary here). ISO/IEC 42001: monitoring and measurement, verification and validation (clause numbers to verify).

Framework references name the area, not an exact clause, unless sure. Check the exact wording before you quote one.

## Write an ADR if

You change the success definition, or upgrade an agent's model on eval evidence (ADR 0002 already requires that).

Use the template in `docs/decisions/README.md`, include the options you rejected, and never edit an accepted record.
