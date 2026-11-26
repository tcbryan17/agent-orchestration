# C07. Budget guardrails

- **Stub:** `src/agent_orchestration/guardrails.py: check_budget` (Phase 5)
- **Status:** not started
- **You type this.** Claude does not write it.

## The question

Before each model call, can the run afford it? The turn cap is easy. The dollar cap needs you to know what a call will cost before you make it. And what happens when the cap is hit: stop, or ask a human?

## Where it sits

```
Spend.from_events(events) + PlannedCall + Limits --> check_budget --> GuardrailResult(allowed, reason)
     allowed=False -> GUARDRAIL event -> stop run (or hand to a human, C9)
```

## Options

These are the options Claude has found. The list is not exhaustive and none is recommended: you choose, then you must be able to say why.

| Option | How it works | Pros | Cons | When you'd pick it |
|---|---|---|---|---|
| A. Worst case from `max_tokens` | Price the whole prompt as input plus `max_tokens` of output | Never overshoots the cap | Ends runs early; needs a prompt-size estimate; must use the right price tier | Hard dollar guarantee on a public demo |
| B. `count_tokens` estimate | Count the prompt with the API, add an output guess | Close to the real cost | An extra API call per turn; the output guess can be wrong | When early stops cost too much quality |
| C. Post-hoc only | Check what has already been spent | Simplest | Can overshoot by one call | Cheap models where one call costs cents |
| Per-run budget | One cap shared by supervisor and workers | Simple to explain; one number to guarantee | A greedy worker starves the rest | Short runs |
| Per-agent budget | Each agent gets a slice | Contains a runaway agent | More config; unused slices wasted | Runs with one expensive agent |
| Haiku's 100K tier | Prompts over 100K tokens reprice the whole request (`pricing.py`) | Needs handling in any estimate | A worst-case estimate must include the higher rate when near 100K | Always consider it for A and B |

## What the tests check

`tests/concepts/test_c07_budget_guardrails.py`. These tests check invariants that any option must keep. They do not care which option you pick. They are skipped for now. When you have written the code, delete the `pytestmark` line at the top of the file to switch them on.

Invariants: a fresh run is allowed; the turn cap blocks with a reason; the dollar cap blocks once reached.

Add one test of your own for the choice you made.

## Questions an interviewer might ask

1. How do you know what the next call will cost before you make it?
2. What happens when the budget runs out mid-task? Does the user get anything?
3. How does Haiku's 100K price tier change your estimate?
4. Is the budget per run or per agent, and why?
5. A public visitor tries to burn your credit. What are all the layers that stop them?

## Governance link

NIST AI RMF: GOVERN (a stated risk tolerance) and MANAGE (risk treatment). NIST AI 600-1: not a single named risk; closest are information security (abuse of a public endpoint) and value chain (provider pricing changes). EU AI Act Art. 15 robustness, voluntary. ISO/IEC 42001: operational planning and control (clause 8; verify).

Framework references name the area, not an exact clause, unless sure. Check the exact wording before you quote one.

## Write an ADR if

You choose the estimation method or what happens on a breach (stop vs ask a human). That is a stated risk tolerance and public-facing behaviour.

Use the template in `docs/decisions/README.md`, include the options you rejected, and never edit an accepted record.
