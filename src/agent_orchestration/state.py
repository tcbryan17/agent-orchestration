"""Run state (C6): where the truth about "what has happened so far" lives."""

from collections.abc import Sequence
from dataclasses import dataclass

from agent_orchestration.events import Event


@dataclass(frozen=True)
class RunState:
    """What the run knows about itself. Minimal; change this if your design needs it.

    Only the events are stored here. Everything else (spend, which workers have run, the
    latest verdict, whether the run is finished or awaiting approval) is what you decide
    to derive from them, or to keep elsewhere.
    """

    events: tuple[Event, ...]

    @classmethod
    def from_events(cls, events: Sequence[Event]) -> "RunState":
        """TODO(human) C6: rebuild the run's state from its event log.

        Where does a run's truth live?

          A. Event log as the source of truth, state rebuilt from it (event sourcing):
             replayable, auditable, and a crashed run can resume from its events; more
             code, and rebuilding costs time on long runs.
          B. A mutable state object updated as the run goes: simple and fast; harder to
             audit, and it can disagree with the log if one is updated and not the other.

        Related: do agents share a scratchpad (easy, but any agent can overwrite another's
        notes, and it is not append-only) or pass artifacts by value (explicit and
        traceable; the supervisor must carry them, see C5)? `guardrails.Spend.from_events`
        already takes option A for money; follow it or explain why this differs.

        Guide: docs/concepts/c06-run-state.md
        Governance: NIST AI RMF MEASURE (traceability); ISO/IEC 42001 documented records.
        """
        raise NotImplementedError("C6: see docs/concepts/c06-run-state.md")
