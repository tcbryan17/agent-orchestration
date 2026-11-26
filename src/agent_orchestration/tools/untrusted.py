"""Handling untrusted tool output (C4): filing text is data, never instructions."""

from agent_orchestration.tools.base import ToolOutcome


def wrap_result(outcome: ToolOutcome, *, tool_name: str) -> str:
    """TODO(human) C4: turn a tool outcome into the text the model will read.

    SEC and Companies House text enters a model that can call tools, so a filing could
    contain "ignore previous instructions". Decide how to blunt that.

      A. Delimit and label as data ("spotlighting"): cheap, keeps all context, only partial
         protection since the model can still be persuaded.
      B. Return only parsed numbers, never free text: strong, but loses useful context.
      C. A quarantined model reads the text and returns structured facts: strongest, costs
         an extra call and has its own failure modes.
      Usually you layer these. Error outcomes should stay recognisable as errors.

    Also GDPR: filings name directors and officers, so minimise what personal data is passed
    on.

    Guide: docs/concepts/c04-untrusted-tool-output.md
    Governance: NIST AI 600-1 information security; OWASP LLM01 prompt injection.
    """
    raise NotImplementedError("C4: see docs/concepts/c04-untrusted-tool-output.md")
