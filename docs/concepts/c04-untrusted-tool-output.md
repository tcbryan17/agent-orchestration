# C04. Untrusted tool output

- **Stub:** `src/agent_orchestration/tools/untrusted.py: wrap_result` (Phase 3)
- **Status:** not started
- **You type this.** Claude does not write it.

## The question

Filings and web pages are text written by other people. A model reading them may treat instructions inside them as your instructions. How do you pass tool output to the model so that data stays data? No option is a complete fix, so think in layers.

## Where it sits

```
SEC / Companies House / web  --text-->  wrap_result  --> tool_result in messages
                                            |
                      delimit / extract numbers only / quarantine reader model
```

## Options

These are the options Claude has found. The list is not exhaustive and none is recommended: you choose, then you must be able to say why.

| Option | How it works | Pros | Cons | When you'd pick it |
|---|---|---|---|---|
| Spotlighting / delimiting | Wrap the output in clear markers and tell the model it is data, not instructions | Cheap; keeps all the content | The model can still be fooled; markers can be spoofed unless escaped | Free-text sources such as filings and web pages |
| Parsed numbers only | Extract the fields you need (e.g. XBRL values) and drop the prose | Almost no room for injection; small context | Loses narrative and context; only works for structured sources | `edgar_company_facts` and the club dataset |
| Quarantined reader model | A separate model with no tools reads the text and returns a short structured answer | Hijacking the reader gains nothing; the privileged agent never sees raw text | Extra cost and latency; the reader's output can still be wrong | High-risk free text, such as web search results |
| Layering | Combine the above with least-privilege tools (C2), output checks (C10) and review (C8) | Failure of one layer is not fatal | More parts to test | Anything public-facing |

## What the tests check

`tests/concepts/test_c04_untrusted_tool_output.py`. These tests check invariants that any option must keep. They do not care which option you pick. They are skipped for now. When you have written the code, delete the `pytestmark` line at the top of the file to switch them on.

Invariants: the output still contains the original content; injected text is not returned bare; error outcomes stay recognisable.

Add one test of your own for the choice you made.

## Questions an interviewer might ask

1. What is indirect prompt injection and where could it enter this system?
2. Why is delimiting not enough on its own?
3. Why is a structured numeric source safer than a web page, and what do you lose?
4. Filings name directors and their pay. Should that text reach the model at all? What would data minimisation say?
5. If an injection succeeded, what is the worst the agent could do? Which controls limit that?

## Governance link

OWASP LLM Top 10: LLM01 prompt injection (verify numbering). NIST AI 600-1: information security, information integrity. NIST AI RMF: MANAGE (risk treatment) and MEASURE (test with adversarial inputs). GDPR: Art. 5(1)(c) data minimisation, since filings contain director names and remuneration. EU AI Act: Art. 15 robustness and cybersecurity, voluntary here.

Framework references name the area, not an exact clause, unless sure. Check the exact wording before you quote one.

## Write an ADR if

You adopt a quarantined reader model, or drop a source from the model's view altogether. Both change cost, architecture and what the agents can see.

Use the template in `docs/decisions/README.md`, include the options you rejected, and never edit an accepted record.
