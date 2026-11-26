"""Acceptance tests for C2, tools.dispatch.dispatch. Delete `pytestmark` to switch them on."""

from typing import Any

import pytest

from agent_orchestration.tools.base import ToolOutcome
from agent_orchestration.tools.dispatch import ToolFn, dispatch

pytestmark = [
    pytest.mark.human_todo,
    pytest.mark.skip(reason="C2 not written yet: docs/concepts/c02-tool-dispatch.md"),
]


def _ok(tool_input: dict[str, Any]) -> ToolOutcome:
    return ToolOutcome(content=f"got {tool_input}")


def _boom(tool_input: dict[str, Any]) -> ToolOutcome:
    raise RuntimeError("disk on fire")


REGISTRY: dict[str, ToolFn] = {"ok": _ok, "boom": _boom, "secret": _ok}
ALLOWED = frozenset({"ok", "boom"})


def call(name: str, tool_input: dict[str, Any] | None = None) -> ToolOutcome:
    return dispatch(name, tool_input or {}, registry=REGISTRY, allowed=ALLOWED)


def test_valid_call_returns_the_tool_output() -> None:
    result = call("ok", {"a": 1})
    assert not result.is_error and "a" in result.content


def test_unknown_tool_is_an_error_outcome_not_a_raise() -> None:
    assert call("nope").is_error


def test_tool_outside_allowlist_is_an_error_outcome() -> None:
    assert call("secret").is_error


def test_tool_that_raises_becomes_an_error_with_a_message() -> None:
    result = call("boom")
    assert result.is_error and result.content
