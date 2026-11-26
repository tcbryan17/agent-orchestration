"""The model client seam: the slice of the `anthropic` SDK the agent loop uses.

The loop depends on `MessagesClient` (a Protocol), never on `anthropic.Anthropic` directly.
That one indirection is what lets CI run the loop against `fakes.ScriptedClient` with no key
and no spend (CLAUDE.md: CI must never need an API key).
"""

from collections.abc import Sequence
from typing import Protocol

import anthropic
from anthropic.types import Message, MessageParam, ToolParam

from agent_orchestration.config import settings


class MessagesClient(Protocol):
    """One Messages API request. Mirrors `client.messages.create` for the arguments we use."""

    def create(
        self,
        *,
        model: str,
        max_tokens: int,
        system: str,
        messages: Sequence[MessageParam],
        tools: Sequence[ToolParam],
    ) -> Message: ...


class AnthropicMessages:
    """The real client. Fails fast without a key (config.py makes the key optional for CI)."""

    def __init__(self, client: anthropic.Anthropic | None = None) -> None:
        if client is None:
            if settings.anthropic_api_key is None:
                raise RuntimeError("ANTHROPIC_API_KEY is not set; live calls need it in .env")
            client = anthropic.Anthropic(api_key=settings.anthropic_api_key.get_secret_value())
        self._client = client

    def create(
        self,
        *,
        model: str,
        max_tokens: int,
        system: str,
        messages: Sequence[MessageParam],
        tools: Sequence[ToolParam],
    ) -> Message:
        return self._client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system,
            messages=list(messages),
            tools=list(tools),
        )
