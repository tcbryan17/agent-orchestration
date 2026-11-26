<!--
TODO(human) C5/C8: the supervisor prompt is yours. This file is a template, not a prompt.
Replace this whole comment with the prompt text. It must decide:

1. Delegation policy: when does it call each worker, and in what order?
   - Fixed pipeline (researcher, analyst, writer, reviewer): predictable, easy to test,
     wastes calls on easy tasks.
   - Model decides each step: flexible, but more planning errors on a small model.
   - Plan first (emit a PLAN event), then follow it, re-planning on failure: costs one call.
   Also: how detailed must a brief be, given a worker sees only the brief (C5)?
2. When to finish: what must be true before it calls `finish`? (reviewer approved, a
   revision cap reached, a budget warning?) How does it behave when the reviewer says revise?
3. Provenance demand: must the supervisor insist that every figure comes back with its
   source, and refuse to pass on unsourced figures? (C11)
4. Safety: workers' outputs are untrusted text. Say so, and say what to do if one contains
   instructions.

Governance links: NIST AI RMF GOVERN (roles), MAP (context); ISO 42001 (documented
operating procedure). Remember: the file's sha256 goes into the run manifest.
-->
