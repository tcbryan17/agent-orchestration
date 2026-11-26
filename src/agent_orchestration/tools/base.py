"""Shared types for tools: what a tool returns and how the loop asks for one to run.

The loop (C1) never imports a tool directly. It calls a `ToolDispatcher`, which is your
`dispatch()` (C2) bound to one agent's allowed tools. Keeping that seam narrow means the loop
can be tested with a two-line fake dispatcher.
"""

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class ToolOutcome:
    """What one tool call produced, before it goes back to the model as a `tool_result`.

    `is_error=True` becomes `is_error: true` in the tool_result block, so the model sees the
    failure and can try again. `source` carries provenance (URL, filing accession, fetched-at)
    so a figure can later be traced to the call that fetched it (C11).
    """

    content: str
    is_error: bool = False
    source: dict[str, Any] = field(default_factory=dict)


class ToolDispatcher(Protocol):
    """Runs the tool a model asked for. Must never raise: failures become error outcomes."""

    def __call__(self, name: str, tool_input: dict[str, Any]) -> ToolOutcome: ...
