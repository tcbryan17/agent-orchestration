"""Content policy (C10): rules a deliverable must obey whatever the model wrote."""

from dataclasses import dataclass
from typing import Literal

PolicyAction = Literal["allow", "flag", "redact", "block"]


@dataclass(frozen=True)
class PolicyResult:
    """The outcome of a policy check. Minimal; change this if your design needs it.

    `text` is the text to use going forward: the input unchanged unless you redact.
    """

    action: PolicyAction
    findings: tuple[str, ...]
    text: str


def check_policy(text: str) -> PolicyResult:
    """TODO(human) C10: check `text` against the content policy.

    The policy: a betting-domain report must contain no betting tips, predictions to bet
    on, or inducements to gamble. (UK gambling advertising rules are relevant context:
    verify the current rules yourself before citing any of them as a requirement.)

    How do you detect a breach?

      A. Keywords and regex: free, instant, deterministic; brittle (misses paraphrase,
         flags "odds" in an innocent sentence).
      B. An LLM classifier: better recall on paraphrase; costs money, is itself a model that
         can be wrong or be injected by the text it reads.
      C. A reviewer rubric item: costs nothing extra; not independent, since the reviewer
         shares the pipeline's failure modes.

    And what happens on a breach?

      A. Block: nothing is published; the safest, and the run fails.
      B. Redact: remove the offending sentences; publishes something, but edits the model's
         text and can leave a broken report.
      C. Flag: publish with a warning or send to a human (C9); relies on a person.

    Record a GUARDRAIL event when it fires. Add red-team prompts to the eval set (C12).

    Guide: docs/concepts/c10-content-policy.md
    Governance: NIST AI RMF MANAGE; NIST AI 600-1 (harmful content); ISO/IEC 42001 controls.
    """
    raise NotImplementedError("C10: see docs/concepts/c10-content-policy.md")
