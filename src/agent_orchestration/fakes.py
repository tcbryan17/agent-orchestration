"""Test doubles for the model client. Nothing here makes a network call.

`ScriptedClient` returns pre-written responses in order, and records a deep copy of every
request. The copies let tests check the loop's behaviour from the outside: which messages it
sent, whether it appended rather than edited history, and that tool results answered the right
`tool_use` ids.
"""

import copy
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Literal

from anthropic.types import Message, MessageParam, TextBlock, ToolParam, ToolUseBlock, Usage

StopReason = Literal[
    "end_turn",
    "max_tokens",
    "stop_sequence",
    "tool_use",
    "pause_turn",
    "refusal",
    "model_context_window_exceeded",
]


@dataclass(frozen=True)
class RecordedRequest:
    model: str
    max_tokens: int
    system: str
    messages: list[MessageParam]
    tools: list[ToolParam]


class ScriptedClient:
    """Plays back `responses` one per `create()` call; fails loudly if the script runs out."""

    def __init__(self, responses: Sequence[Message]) -> None:
        self._responses = list(responses)
        self.requests: list[RecordedRequest] = []

    def create(
        self,
        *,
        model: str,
        max_tokens: int,
        system: str,
        messages: Sequence[MessageParam],
        tools: Sequence[ToolParam],
    ) -> Message:
        self.requests.append(
            RecordedRequest(
                model=model,
                max_tokens=max_tokens,
                system=system,
                messages=copy.deepcopy(list(messages)),
                tools=copy.deepcopy(list(tools)),
            )
        )
        if len(self.requests) > len(self._responses):
            raise AssertionError(
                f"ScriptedClient ran out of responses at call {len(self.requests)}"
            )
        return self._responses[len(self.requests) - 1]


def make_message(
    content: Sequence[TextBlock | ToolUseBlock],
    *,
    stop_reason: StopReason,
    input_tokens: int = 100,
    output_tokens: int = 20,
    model: str = "claude-haiku-5-5",
) -> Message:
    """Build an API response the way the SDK would parse it."""
    return Message(
        id="msg_fake",
        type="message",
        role="assistant",
        model=model,
        content=list(content),
        stop_reason=stop_reason,
        stop_sequence=None,
        usage=Usage(input_tokens=input_tokens, output_tokens=output_tokens),
    )


def text_reply(text: str, *, stop_reason: StopReason = "end_turn", **kw: Any) -> Message:
    """A response holding one text block (end_turn, max_tokens, refusal, pause_turn...)."""
    return make_message([TextBlock(type="text", text=text)], stop_reason=stop_reason, **kw)


def tool_call(
    name: str, tool_input: dict[str, Any], *, tool_id: str = "toolu_1", **kw: Any
) -> Message:
    """A response asking for one tool call."""
    block = ToolUseBlock(type="tool_use", id=tool_id, name=name, input=tool_input)
    return make_message([block], stop_reason="tool_use", **kw)


def tool_calls(calls: Sequence[tuple[str, str, dict[str, Any]]], **kw: Any) -> Message:
    """A response asking for several tool calls at once: (tool_id, name, input) each."""
    blocks = [ToolUseBlock(type="tool_use", id=i, name=n, input=inp) for i, n, inp in calls]
    return make_message(blocks, stop_reason="tool_use", **kw)
