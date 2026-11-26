"""Tool dispatch: turning a model's tool call into a safe function call (C2).

The stub `dispatch()` is yours. `bind()` is plumbing: it fixes the registry and the allowlist
so the loop sees the narrow `ToolDispatcher` signature from base.py.
"""

from collections.abc import Callable, Mapping
from functools import partial
from typing import Any

from agent_orchestration.tools.base import ToolDispatcher, ToolOutcome

ToolFn = Callable[[dict[str, Any]], ToolOutcome]


def dispatch(
    name: str,
    tool_input: dict[str, Any],
    *,
    registry: Mapping[str, ToolFn],
    allowed: frozenset[str],
) -> ToolOutcome:
    """TODO(human) C2: run the tool the model asked for, safely, and never raise.

    The model's tool call is untrusted input: the name may not exist, may not be one this
    agent is allowed, and the arguments may be wrong. Decide how each case is handled.

      A. Registry dict vs decorator registration: a plain dict is explicit and easy to
         test; decorators keep a tool next to its definition but add import-time magic.
      B. Validate input with Pydantic vs trust the strict JSON schema (C3): validation
         catches bad arguments with good messages, at the cost of a model per tool.
      C. Bad call becomes an `is_error` outcome (the model can read it and retry) vs raise
         (the run stops; simple, but one typo kills a whole run). base.ToolDispatcher
         requires that this function never raises.
      D. Per-agent allowlist (`allowed`) vs one global registry: the allowlist limits what a
         hijacked agent can do (least privilege).

    Guide: docs/concepts/c02-tool-dispatch.md
    Governance: NIST AI RMF MANAGE; OWASP LLM excessive agency; GDPR data minimisation.
    """
    raise NotImplementedError("C2: see docs/concepts/c02-tool-dispatch.md")


def bind(registry: Mapping[str, ToolFn], allowed: frozenset[str]) -> ToolDispatcher:
    """Fix `registry` and `allowed` so the result matches the loop's `ToolDispatcher`."""
    return partial(dispatch, registry=registry, allowed=allowed)
