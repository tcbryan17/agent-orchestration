# C01. The agent loop

- **Stub:** `src/agent_orchestration/loop.py: run_agent` (Phase 2)
- **Status:** not started
- **You type this.** Claude does not write it.

## The question

One agent has a task and some tools. How does it keep calling the model until the work is done, and what does it do when the model stops for a reason other than "I'm finished"? Every `stop_reason` is a branch you must handle on purpose. Unknown ones must fail loudly. A loop that only handles `end_turn` and `tool_use` will hang, loop forever or lose data the first time the API returns something else.

## Where it sits

```
task -> messages[] -> check_budget -> model call -> record MODEL_CALL -> append assistant turn
                                                         |
          +---------+-----------+-----------+------------+----------------+
       end_turn   tool_use   max_tokens  pause_turn   refusal   context window exceeded
        return    run tools   (decide)     resend     (decide)      (decide)
                  send ALL results back
                  in ONE user message ----> loop
```

## Options

These are the options Claude has found. The list is not exhaustive and none is recommended: you choose, then you must be able to say why.

| Option | How it works | Pros | Cons | When you'd pick it |
|---|---|---|---|---|
| `max_tokens`: continue the turn | Append the partial answer and ask the model to carry on | Often finishes the answer | Spends more; a cut-off `tool_use` block cannot be run | Long prose where a partial answer is useful |
| `max_tokens`: fail loudly | Stop, record an ERROR event, return what you have | Safe and predictable; the cost stays bounded | Wastes the partial output | A demo with a cost cap where truncation means a bad prompt |
| `max_tokens`: retry with a larger cap | Redo the call once with a higher `max_tokens` | Fixes a cap that was set too low | Pays for the call twice; needs a ceiling to stop it repeating | The cap was a guess and you have a hard dollar limit elsewhere |
| `pause_turn`: resend unchanged | Send the conversation back as it is so a server-tool turn can continue | Matches how the API expects it to work | Needs its own loop bound, or it can run for ever | Whenever you use server tools such as web search |
| `refusal`: stop and record ERROR | Treat it as a final state and log it | Honest and simple; keeps the trace truthful | The task fails with no second chance | Default for a public demo |
| `refusal`: rephrase and retry | Reword the request and call again | Might rescue a false refusal | Looks like jailbreaking; hides a safety signal; hard to defend | Rarely. Be ready to justify it |
| `model_context_window_exceeded` | Error out, or end the turn with what exists | Error: nothing is silently dropped. End: partial result saved | Error: wasted work. End: caller may not notice the cut | Decide per agent. The researcher is the likeliest to hit it |
| Parallel tool calls: sequential | Run each `tool_use` block in order | Simple, deterministic event order | Slower when tools are slow | Fast tools, or when you want replayable traces |
| Parallel tool calls: concurrent | Run blocks together (threads or asyncio) | Lower latency | You need a rule for event order; harder to test | Slow network tools such as EDGAR fetches |
| Tool errors: `is_error` result | Send the failure back as a `tool_result` with `is_error: true` | The model can recover; the run continues | The model may retry a doomed call; needs a turn cap | Almost always |
| Tool errors: raise | Let the exception end the run | Failures are impossible to miss | One bad tool call kills the whole task | Programming errors, not tool failures |

## What the tests check

`tests/concepts/test_c01_agent_loop.py`. These tests check invariants that any option must keep. They do not care which option you pick. They are skipped for now. When you have written the code, delete the `pytestmark` line at the top of the file to switch them on.

Invariants: `end_turn` returns the text after one call; a `tool_use` result goes back with the matching `tool_use_id`; parallel calls are answered in one user message; a tool error goes back to the model and the run continues; history is append-only; a refusal stops without looping; the turn limit is checked before the call; every event hangs off the parent event.

Add one test of your own for the choice you made.

## Questions an interviewer might ask

1. What are the possible values of `stop_reason` and what does your loop do for each?
2. Why must all parallel tool results go back in a single user message?
3. What stops the loop from running for ever? Where exactly is that checked?
4. A tool raises an exception. Does the run die? Why did you choose that?
5. Why is the message history append-only? What would break if you edited an earlier turn?

## Governance link

NIST AI RMF: MEASURE (every step is traced, so the system can be assessed) and MANAGE (a defined response when the model refuses or is cut off). NIST AI 600-1: confabulation (a truncated answer can read as a complete one). EU AI Act: record-keeping in the style of Art. 12 (automatic logging), which is voluntary here. ISO/IEC 42001: AI system lifecycle and event logging (Annex A control number to verify against the standard).

Framework references name the area, not an exact clause, unless sure. Check the exact wording before you quote one.

## Write an ADR if

You choose a non-default policy for `max_tokens` or `refusal` (for example retry with a rephrase), or you move to concurrent tool execution. The `stop_reason` policy is a behaviour the whole system depends on.

Use the template in `docs/decisions/README.md`, include the options you rejected, and never edit an accepted record.
