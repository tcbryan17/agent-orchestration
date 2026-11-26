"""Agent specs: one frozen record per agent saying who it is and what it may do.

Why a spec object rather than constants scattered through the code: the model, the prompt
and the tool allowlist are the three things that decide an agent's behaviour, so they live
together, are immutable, and can be written into the run manifest (manifest.py) as-is.

Models default to `settings.default_model` (ADR 0002: Haiku first). To upgrade one agent
after an eval shows it is the bottleneck, add one line to `MODEL_OVERRIDES`, for example
`{"supervisor": "claude-sonnet-5-5"}`, and write the ADR with before/after numbers.

The tool lists are least privilege (OWASP LLM "excessive agency"): the researcher can fetch
filings but not calculate, the analyst can calculate but not fetch, and the writer and
reviewer have no tools at all. The supervisor's tools are the `delegate_*` tools plus
`finish`, built by `supervisor.supervisor_tools()`.
"""

from dataclasses import dataclass
from pathlib import Path

from agent_orchestration.config import settings

PROMPTS_DIR = Path(__file__).resolve().parents[3] / "prompts"

# The one-line upgrade point from ADR 0002. Empty means everyone uses the default model.
MODEL_OVERRIDES: dict[str, str] = {}


@dataclass(frozen=True)
class AgentSpec:
    """Everything that defines one agent, fixed for the life of a run."""

    name: str
    model: str
    prompt_file: Path
    tools: frozenset[str]
    max_tokens: int


def _spec(name: str, tools: frozenset[str], max_tokens: int = 2048) -> AgentSpec:
    return AgentSpec(
        name=name,
        model=MODEL_OVERRIDES.get(name, settings.default_model),
        prompt_file=PROMPTS_DIR / f"{name}.md",
        tools=tools,
        max_tokens=max_tokens,
    )


def delegate_tool_names() -> frozenset[str]:
    """The supervisor's tools: one `delegate_<worker>` per worker, plus `finish`."""
    workers = ("researcher", "analyst", "writer", "reviewer")
    return frozenset({f"delegate_{w}" for w in workers} | {"finish"})


SPECS: dict[str, AgentSpec] = {
    spec.name: spec
    for spec in (
        _spec("supervisor", delegate_tool_names()),
        _spec("researcher", frozenset({"edgar_company_facts"})),
        _spec("analyst", frozenset({"calculator", "build_table"})),
        _spec("writer", frozenset(), max_tokens=4096),
        _spec("reviewer", frozenset()),
    )
}
