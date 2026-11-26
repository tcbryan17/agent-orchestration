# C10. Content policy

- **Stub:** `src/agent_orchestration/policy.py: check_policy` (Phase 5)
- **Status:** not started
- **You type this.** Claude does not write it.

## The question

The domain is sports betting. The report must not contain tips, odds advice or inducements, and it is not investment advice. Where do you check the text, how, and what do you do when it fails?

## Where it sits

```
draft --> check_policy --> pass -> reviewer / publish
                       --> fail -> block | redact | flag (record a GUARDRAIL event)
```

## Options

These are the options Claude has found. The list is not exhaustive and none is recommended: you choose, then you must be able to say why.

| Option | How it works | Pros | Cons | When you'd pick it |
|---|---|---|---|---|
| Regex / keyword rules | Match patterns such as "guaranteed", "bet on", "you should buy" | Free, fast, predictable, easy to test | Misses paraphrase; false positives | A first filter with red-team prompts as tests |
| LLM classifier | A model decides whether the text breaks policy | Catches wording a regex misses | Costs money; can be wrong or be injected; harder to test | As a second layer on top of rules |
| Reviewer rubric item | The reviewer checks policy as one of its criteria | No new component | Policy depends on the reviewer's mood; not a hard stop | As an extra layer |
| Block | Reject the output and stop or retry | Strongest | The user gets nothing | Clear breaches |
| Redact | Remove the offending part | User still gets a report | May leave a misleading gap | Small, local breaches |
| Flag | Keep the text and mark it | Transparent | Bad content still reaches the reader | Borderline cases with human review |

## What the tests check

`tests/concepts/test_c10_content_policy.py`. These tests check invariants that any option must keep. They do not care which option you pick. They are skipped for now. When you have written the code, delete the `pytestmark` line at the top of the file to switch them on.

`tests/concepts/test_c10_content_policy.py` checks, for any option you pick:

- `test_ordinary_financial_prose_is_allowed_unchanged`
- `test_an_obvious_betting_tip_is_not_allowed`
- `test_redaction_never_leaves_the_tip_in_the_text`
- `test_same_input_gives_the_same_result`


Add one test of your own for the choice you made.

## Questions an interviewer might ask

1. Why is a keyword filter alone not enough? Why is an LLM filter alone not enough?
2. Is "Team A is a strong buy" investment advice? Where do you draw the line, and who decides?
3. What happens to a draft that fails? Who sees why?
4. How do you test the policy? What are your red-team prompts?
5. Which regulations apply to betting-related content in the UK, and is this a regulated promotion? (Check; do not guess.)

## Governance link

NIST AI RMF: MANAGE (risk treatment) and MEASURE (red-team tests). NIST AI 600-1: information integrity and harmful content risks. EU AI Act: Art. 50 transparency applies to AI-generated content; policy limits are your own choice. Betting advertising rules (UK Gambling Commission, ASA) are a separate area: to verify before any public claim.

Framework references name the area, not an exact clause, unless sure. Check the exact wording before you quote one.

## Write an ADR if

You adopt an LLM classifier or a block/redact/flag policy that changes what users can receive.

Use the template in `docs/decisions/README.md`, include the options you rejected, and never edit an accepted record.
