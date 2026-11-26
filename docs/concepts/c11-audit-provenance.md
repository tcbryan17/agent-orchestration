# C11. Audit trail and provenance

- **Stub:** `src/agent_orchestration/audit.py: chain_hash, canonical_bytes, verify_chain; src/agent_orchestration/provenance.py: check_claims` (Phase 4-6)
- **Status:** not started
- **You type this.** Claude does not write it.

## The question

How do you make the event log tamper-evident, so that editing a past event is detectable? And how do you link every figure in a report back to the tool call that fetched it? There is a tension: an immutable log must also respect a person's right to have their data erased.

## Where it sits

```
event N-1 --hash--> event N  (prev_hash + canonical_bytes(event) -> hash)
verify_chain: recompute from the start; first mismatch = tampering
report claim "revenue 4.2bn" --source event ID--> TOOL_RESULT event --> SEC filing
```

## Options

These are the options Claude has found. The list is not exhaustive and none is recommended: you choose, then you must be able to say why.

| Option | How it works | Pros | Cons | When you'd pick it |
|---|---|---|---|---|
| Canonical JSON: sorted keys, Decimal as text | Serialise events the same way every time before hashing | Same hash on any machine; money does not lose precision | Rules to follow exactly; datetimes and floats need a policy | The default way to build hashable bytes |
| Canonical form: custom format | Your own byte layout | Full control | More to get wrong; harder to explain | Rarely |
| Hash chain | Each entry hashes the previous hash plus its own bytes | Simple; detects edits, deletion and reordering | Verifying means reading the whole chain; no proof for one entry alone | A single-writer log |
| Merkle tree | Entries are leaves; a root hash covers all | Short proof that one entry is included | More complex | Auditors check single entries without the full log |
| Signed entries | Each entry is signed with a key | Proves who wrote it | Key management; a stolen key forges history | When more than one party writes |
| Erasure: personal data out of chained fields | Keep names out of hashed fields; hash only a pointer to a separate store | Delete the store, the chain stays valid | Needs discipline about what goes in events | Design-time choice |
| Erasure: crypto-shredding | Encrypt personal data per subject and delete the key | Data becomes unreadable but hashes still verify | Key management; whether this counts as erasure needs checking | Data that must stay in events |
| Erasure: redact before hashing | Remove personal data before the event is chained | Nothing to erase later | The log loses detail | When the data is not needed for audit |
| Provenance: inline markers | Claims in the text carry markers like [src:evt-42] | Easy to read and render | Parsing fragile; the model may drop or invent markers | Simple reports |
| Provenance: structured claims list | A separate list of {claim, value, source_event_id} | Machine-checkable; reviewer can reject unsourced claims | More schema; the report text and list can diverge | When `check_claims` must be strict |

## What the tests check

`tests/concepts/test_c11_audit_provenance.py`. These tests check invariants that any option must keep. They do not care which option you pick. They are skipped for now. When you have written the code, delete the `pytestmark` line at the top of the file to switch them on.

`tests/concepts/test_c11_audit_provenance.py` checks, for any option you pick:

- `test_same_event_hashes_identically_twice`
- `test_decimal_cost_is_stable_and_exact`
- `test_payload_key_order_does_not_change_the_bytes`
- `test_hash_depends_on_the_previous_hash`
- `test_intact_chain_verifies`
- `test_chain_detects_a_tampered_event`
- `test_chain_detects_a_removed_event`
- `test_check_claims_flags_a_figure_with_no_source`
- `test_check_claims_accepts_a_sourced_figure`


Add one test of your own for the choice you made.

## Questions an interviewer might ask

1. How would you prove to an auditor that this log was not edited after the fact?
2. What exactly goes into the hash, and why must it be the same on every machine?
3. A director asks for their name to be erased. What do you do about a hash chain?
4. What does a hash chain not protect against? (Hint: someone who rewrites the whole chain.)
5. How does the reviewer know a figure came from a tool and not from the model's memory?

## Governance link

NIST AI RMF: MEASURE (traceable records) and GOVERN (accountability). NIST AI 600-1: information integrity and confabulation (provenance). EU AI Act: Art. 12-style logging (voluntary here). ISO/IEC 42001: data provenance and event logging (Annex A numbers to verify). GDPR: Art. 17 erasure and Art. 5(1)(e) storage limitation against an immutable log; Art. 5(1)(c) minimisation. See `docs/governance/gdpr.md`.

Framework references name the area, not an exact clause, unless sure. Check the exact wording before you quote one.

## Write an ADR if

You choose the erasure approach, the chain design, or the provenance format. The data model, the API and the legal position all rest on these.

Use the template in `docs/decisions/README.md`, include the options you rejected, and never edit an accepted record.
