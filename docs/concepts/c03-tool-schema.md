# C03. Tool schema design

- **Stub:** `src/agent_orchestration/tools/schemas.py: edgar_schema` (Phase 3)
- **Status:** not started
- **You type this.** Claude does not write it.

## The question

The schema and description are the only instructions the model has for a tool. How do you write them so the model calls the tool correctly, with arguments you can trust, and knows when not to call it? This is prompt design for tools.

## Where it sits

```
name + description (when to use, when NOT to use)
input_schema: properties, enums, required, additionalProperties: false
   -> strict: true (optional) -> the model's arguments are shaped by it
```

## Options

These are the options Claude has found. The list is not exhaustive and none is recommended: you choose, then you must be able to say why.

| Option | How it works | Pros | Cons | When you'd pick it |
|---|---|---|---|---|
| Enums | Closed list of allowed values (e.g. company keys, metric names) | The model cannot invent values; easy to validate | Must be updated when you add companies | Small, known sets such as the four SEC companies |
| Free strings | Any string is accepted | Flexible; no schema changes | Typos and invented values; need validation after | Open-ended input such as a search query |
| `strict: true` | The API constrains output to the schema | Guaranteed shape and types | Limits which JSON Schema features you can use; check support on Haiku 5.5 | Whenever the model supports it |
| Loose schema | No strict mode, rely on the model | Any schema feature allowed | Wrong types and extra fields can appear | Fallback when strict is unavailable; add validation in C2 |
| Terse description | One line saying what the tool does | Cheap in tokens | Model picks it at the wrong time | Tools with one obvious use |
| Description as a prompt | What it does, when to use it, when not to, units, examples | Better tool choice; fewer wasted calls | More tokens on every request; can go stale | Tools that look alike (EDGAR vs club data) |

## What the tests check

`tests/concepts/test_c03_tool_schema.py`. These tests check invariants that any option must keep. They do not care which option you pick. They are skipped for now. When you have written the code, delete the `pytestmark` line at the top of the file to switch them on.

Invariants: the schema is well formed (name, description, object `input_schema`); the schema requires the company argument.

Add one test of your own for the choice you made.

## Questions an interviewer might ask

1. Why use an enum for the company instead of a string?
2. What does `strict: true` guarantee, and what does it not?
3. How did you write the description to stop the model calling the tool for a club that is not on EDGAR?
4. What breaks if the description and the code disagree?
5. How do you keep descriptions short enough to be affordable on every call?

## Governance link

NIST AI RMF: MAP (documenting intended use and limits of each component). NIST AI 600-1: confabulation (a clear schema reduces invented arguments). OWASP LLM Top 10: excessive agency. ISO/IEC 42001: documentation of system components (control number to verify).

Framework references name the area, not an exact clause, unless sure. Check the exact wording before you quote one.

## Write an ADR if

Rarely. Write one if you adopt a convention all tools follow, such as strict mode everywhere, or you give up strict mode because Haiku 5.5 does not support it.

Use the template in `docs/decisions/README.md`, include the options you rejected, and never edit an accepted record.
