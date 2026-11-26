# C02. Tool dispatch

- **Stub:** `src/agent_orchestration/tools/dispatch.py: dispatch` (Phase 3)
- **Status:** not started
- **You type this.** Claude does not write it.

## The question

The model names a tool and gives some arguments. Who runs it, what checks happen first, and what does the model see if something fails? The dispatcher is where model output becomes real action, so it is where excessive agency is stopped or allowed.

## Where it sits

```
tool_use block (name, input)
   -> is the name registered?  -> is it on THIS agent's allowlist?
   -> validate input           -> run the tool
   -> ToolOutcome(content, is_error)  -> wrap_result (C4) -> back to the model
```

## Options

These are the options Claude has found. The list is not exhaustive and none is recommended: you choose, then you must be able to say why.

| Option | How it works | Pros | Cons | When you'd pick it |
|---|---|---|---|---|
| Registry dict | A plain `dict[str, Tool]` built in one place | Easy to read and test; everything visible in one file | You must remember to add each tool | Few tools; you want it explicit |
| Decorator registration | `@tool` adds a function to a global registry at import | Tool and registration sit together | Import-order magic; harder to restrict per agent | Many tools, or tools in many files |
| Pydantic validation | Parse input into a model; invalid input becomes an error outcome | Clear error messages; type-safe inside the tool | Duplicates the JSON schema unless generated from it | Tools where a bad value does damage |
| Trust strict schemas | Rely on `strict: true` so the API guarantees the shape | Less code | Does not cover everything (values, ranges, business rules); not every model/feature combination supports it (check Haiku 5.5) | Simple tools, plus a few cheap manual checks |
| Failure as `is_error` outcome | Return an error outcome the loop sends back to the model | The model can correct itself; run continues | Error text may leak internals | Default for expected failures |
| Failure as raise | Let exceptions propagate | Loud | One bad call kills the run | Bugs in your own code |
| Per-agent allowlist | Each agent gets only the tools it needs; dispatch refuses others | Limits damage if an agent is hijacked; matches OWASP's excessive-agency advice | More config to keep in step | Any multi-agent system |
| Global registry only | Any agent may call any registered tool | Simplest | A hijacked agent can use every tool | A single agent with harmless tools |

## What the tests check

`tests/concepts/test_c02_tool_dispatch.py`. These tests check invariants that any option must keep. They do not care which option you pick. They are skipped for now. When you have written the code, delete the `pytestmark` line at the top of the file to switch them on.

Invariants: a valid call returns the tool output; an unknown tool is an error outcome, not a raise; a tool outside the agent's allowlist is an error outcome; a tool that raises becomes an error outcome with a message.

Add one test of your own for the choice you made.

## Questions an interviewer might ask

1. The model asks for a tool that does not exist. What happens, and what does the model see?
2. Why give each agent its own tool allowlist if the schemas are already strict?
3. Where do you validate arguments, and what does strict mode not catch?
4. What should an error message to the model contain, and what must it never contain?
5. How would a prompt-injected researcher try to misuse dispatch, and what stops it?

## Governance link

OWASP LLM Top 10: excessive agency (LLM06 in the 2025 list; check the current numbering). NIST AI RMF: MANAGE (controls that limit what the system can do). NIST AI 600-1: information security. ISO/IEC 42001: Annex A responsible-use controls (number to verify). EU AI Act: Art. 15 robustness and cybersecurity, voluntary here.

Framework references name the area, not an exact clause, unless sure. Check the exact wording before you quote one.

## Write an ADR if

You pick a registration style or an allowlist model that other phases will rely on (for example, workers sharing one registry). Small wiring choices do not need an ADR.

Use the template in `docs/decisions/README.md`, include the options you rejected, and never edit an accepted record.
