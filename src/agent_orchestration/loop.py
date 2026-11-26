"""The agent loop: one agent works on one task, calling tools until it is done.

Everything around the loop is boilerplate (client, recorder, dispatcher, limits). The loop
body is C1 and is yours: it is the single most-asked question in agent interviews.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from uuid import UUID

from anthropic.types import MessageParam, ToolParam

from agent_orchestration.guardrails import Limits
from agent_orchestration.llm import MessagesClient
from agent_orchestration.recorder import Recorder
from agent_orchestration.tools.base import ToolDispatcher


@dataclass(frozen=True)
class AgentResult:
    """How one agent's run ended."""

    text: str  # the agent's final answer (or what it had when it stopped)
    stop_reason: str  # the last stop_reason, or "guardrail" if a limit stopped it
    turns: int  # model calls made
    messages: list[MessageParam]  # the full, append-only conversation


def run_agent(
    *,
    client: MessagesClient,
    recorder: Recorder,
    agent: str,
    model: str,
    system: str,
    task: str,
    tools: Sequence[ToolParam],
    dispatch: ToolDispatcher,
    limits: Limits,
    parent_id: UUID | None = None,
    max_tokens: int = 2048,
) -> AgentResult:
    """TODO(human) C1: run one agent until it finishes, fails, or hits a limit.

    The shape: start `messages` with the task, then loop: check the budget
    (guardrails.check_budget), call the model, record a MODEL_CALL event with
    `cost_from_usage()`, append the assistant turn, then branch on `stop_reason`:

      end_turn      Done. Return the text.
      tool_use      Run every tool_use block through `dispatch`, record TOOL_CALL and
                    TOOL_RESULT events, send ALL results back in ONE user message
                    (each tool_result's `tool_use_id` must match its call).
                    Parallel calls: run in order (simple, deterministic trace) or
                    concurrently (faster, but the event order needs a rule).
      max_tokens    The answer was cut off. Options: continue the turn (spends more, may
                    finish), fail loudly (safe, wastes the partial), or retry once with a
                    larger cap. A cut-off tool_use block can't be run.
      pause_turn    The server paused a long turn (server tools). Send the conversation
                    back unchanged to let it continue.
      refusal       The model declined. Options: stop and record an ERROR event (honest,
                    simplest), or retry with a rephrase (risky: looks like jailbreaking).
                    Haiku 5.5 has no server-side fallback (ADR 0002).
      model_context_window_exceeded / stop_sequence / anything new
                    Decide: treat as an error, or as end_turn? Unknown values should
                    fail loudly rather than loop forever.

    Rules to keep: `messages` is append-only (never edit earlier turns); tool errors go back
    to the model as `is_error` results rather than crashing the run; every event of this
    agent hangs off `parent_id` so the run forms a tree.

    Guide: docs/concepts/c01-agent-loop.md
    Governance: NIST AI RMF MEASURE (every step traced); EU AI Act Art. 12-style logging.
    """
    raise NotImplementedError("C1: see docs/concepts/c01-agent-loop.md")
