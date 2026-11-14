"""Trace events: the single record of everything that happens in a run.

Every step of every agent emits one `Event`. Four consumers read the same events, so the
schema has to serve all of them at once:

1. **Timeline and replay** (Phase 6, portfolio site): who did what, when, in what order.
2. **Cost tracking** (Phase 1, ADR 0002): tokens and dollars per step, summed per agent/run.
3. **Audit trail** (governance): an append-only, tamper-evident log of the run.
4. **Provenance** (governance): tracing a figure in the final report back to the tool call
   that fetched it, inside the worker the supervisor delegated to.

Whatever isn't captured here at the moment it happens can't be reconstructed later.
"""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class EventType(StrEnum):
    """What kind of step an event records. Adjust freely while designing `Event`."""

    RUN_STARTED = "run_started"
    PLAN = "plan"  # the supervisor's plan or re-plan
    HANDOFF = "handoff"  # the supervisor delegates a sub-task to a worker
    MODEL_CALL = "model_call"  # one Messages API request/response; carries token usage
    TOOL_CALL = "tool_call"  # an agent asked to run a tool (name + input)
    TOOL_RESULT = "tool_result"  # what the tool returned (or its error)
    MESSAGE = "message"  # an agent's text output
    REVIEW = "review"  # the reviewer's verdict: approve or revise
    GUARDRAIL = "guardrail"  # a limit or policy check fired (turns, dollars, content policy)
    ERROR = "error"
    RUN_FINISHED = "run_finished"


class TokenUsage(BaseModel):
    """Token counts as reported in an API response's `usage` block.

    Cache reads and writes are billed at different rates from plain input, so they're kept
    separate rather than summed into input_tokens.
    """

    model_config = ConfigDict(frozen=True)

    input_tokens: int = 0
    output_tokens: int = 0
    cache_creation_input_tokens: int = 0
    cache_read_input_tokens: int = 0


class Event(BaseModel):
    """One step in a run. See the module docstring for the four consumers it must serve."""

    # TODO(human): define the fields of an Event (aim for about 8-10 lines).
    #
    # Questions to answer with your field choices:
    #   - Identity and ordering: how do you identify a run and an event, and how do you
    #     order events reliably (a timestamp, a sequence number, or both)?
    #   - Who and what: which agent, which EventType, and what's shown on the timeline?
    #   - Nesting: a worker's tool call happens inside a supervisor handoff. How does an
    #     event point at the step that caused it?
    #   - Cost: where do TokenUsage and the dollar cost live, and which type holds money?
    #   - Reproducibility: what tells an auditor which model produced this step?
    #   - Mutability: should an Event be changeable after it's created (model_config)?
