"""Provenance (C11): can every figure in a deliverable be traced to a tool result?"""

from collections.abc import Sequence
from dataclasses import dataclass

from agent_orchestration.events import Event


@dataclass(frozen=True)
class UnsupportedClaim:
    """A claim in the report with no matching tool result. Change this if you need to."""

    claim: str
    reason: str


def check_claims(report: str, events: Sequence[Event]) -> list[UnsupportedClaim]:
    """TODO(human) C11: list the claims in `report` that no event in `events` supports.

    How do claims get tied to evidence?

      A. Inline markers: the writer tags each figure (for example `[ev:3f2a]` with an event
         id) and you check each tag points at a TOOL_RESULT containing that figure; simple
         to check, relies on the writer using the markers honestly.
      B. A structured claims list: the writer returns text plus a list of
         (figure, event_id) pairs; easiest to verify mechanically; the prose and the list
         can still disagree, and it constrains the writer's output format.

    Decide how a figure matches a result (exact string, or the number after rounding and
    unit conversion), and what the reviewer (C8) does with the list. Note this checks that
    a figure appears in a source, not that the source is correct or the sentence
    interprets it fairly.

    Guide: docs/concepts/c11-audit-provenance.md
    Governance: NIST AI 600-1 information integrity and confabulation; ISO/IEC 42001 data
    provenance.
    """
    raise NotImplementedError("C11: see docs/concepts/c11-audit-provenance.md")
