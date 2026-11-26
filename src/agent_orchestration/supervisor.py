"""Supervisor handoff (C5): the boundary between the supervisor and a worker.

Boilerplate here: the `delegate_<worker>` and `finish` tool definitions the supervisor sees.
The handoff itself, `delegate()`, is C5 and is yours. It is where "what does a worker know?"
and "what does the supervisor get back?" are decided, which are the two most important
design questions in a multi-agent system.
"""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from uuid import UUID

from anthropic.types import ToolParam

from agent_orchestration.agents.specs import AgentSpec
from agent_orchestration.guardrails import Limits
from agent_orchestration.llm import MessagesClient
from agent_orchestration.recorder import Recorder


@dataclass(frozen=True)
class Artifact:
    """A named piece of earlier work (for example the researcher's facts) passed to a worker.

    Minimal on purpose; change this if your design needs it. `source_event_ids` keeps the
    link back to the events that produced it (provenance, C11).
    """

    name: str
    content: str
    source_event_ids: tuple[UUID, ...] = ()


@dataclass(frozen=True)
class WorkerResult:
    """What comes back from a worker. Change this if your design needs it."""

    text: str
    source_event_ids: tuple[UUID, ...] = field(default_factory=tuple)
    stop_reason: str = "end_turn"


def supervisor_tools(specs: Mapping[str, AgentSpec] | Sequence[AgentSpec]) -> list[ToolParam]:
    """Build the supervisor's tools: one `delegate_<name>` per worker, plus `finish`.

    Each delegate tool takes a single `brief` string. Keeping the input to one string is
    deliberate: whatever the supervisor writes there is everything the worker can know
    (unless you choose to pass artifacts too, in `delegate()`).
    """
    items = specs.values() if isinstance(specs, Mapping) else specs
    tools: list[ToolParam] = [
        {
            "name": f"delegate_{spec.name}",
            "description": (
                f"Hand a sub-task to the {spec.name}. The {spec.name} sees only the brief "
                "you write, so include everything it needs."
            ),
            "input_schema": {
                "type": "object",
                "properties": {"brief": {"type": "string", "description": "The sub-task."}},
                "required": ["brief"],
                "additionalProperties": False,
            },
        }
        for spec in items
        if spec.name != "supervisor"
    ]
    tools.append(
        {
            "name": "finish",
            "description": "End the run with the final deliverable.",
            "input_schema": {
                "type": "object",
                "properties": {"report": {"type": "string", "description": "The deliverable."}},
                "required": ["report"],
                "additionalProperties": False,
            },
        }
    )
    return tools


def delegate(
    *,
    client: MessagesClient,
    recorder: Recorder,
    worker: AgentSpec,
    brief: str,
    artifacts: Sequence[Artifact],
    limits: Limits,
    parent_id: UUID | None,
) -> WorkerResult:
    """TODO(human) C5: run `worker` on a sub-task and decide what crosses the boundary.

    Two questions. What does the worker SEE?

      A. The brief only: smallest context and cost, strongest isolation; the supervisor must
         write complete briefs or the worker flounders.
      B. The brief plus selected artifacts (earlier results, by value): the worker has what
         it needs without the supervisor's chatter; you choose what to include.
      C. The supervisor's full history: easiest for the worker, but it breaks the
         append-only rule (PLAN.md: workers get a fresh messages list, never an edited copy)
         and leaks the whole context, costing tokens and widening what an injected
         instruction can reach.

    And what comes BACK?

      A. The full transcript: complete, but costly and noisy for the supervisor's context.
      B. A free-text summary: cheap and readable; facts can be dropped or distorted, and
         the source of each figure is lost.
      C. A structured result with source event IDs (text plus the tool-result events behind
         each figure): best for provenance (C11) and the audit trail; more code.

    Also decide: record a HANDOFF event (what, with which parent_id) before running the
    worker, and whether workers share the run's budget (C7) or get a slice.

    Guide: docs/concepts/c05-supervisor-handoff.md
    Governance: NIST AI RMF MAP (context and boundaries); GDPR data minimisation (what
    personal data, such as directors' names in filings, crosses the boundary).
    """
    raise NotImplementedError("C5: see docs/concepts/c05-supervisor-handoff.md")
