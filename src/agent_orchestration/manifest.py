"""The run manifest: a reproducibility record written once at the start of a run.

An event log says what happened; the manifest says under what conditions, so a result can
be reproduced or explained months later: which code (git sha), which software versions,
which model and exact prompt (sha256) each agent used, which limits and tools applied.
This supports NIST AI RMF MEASURE (documented test conditions) and ISO/IEC 42001 lifecycle
records. It is a record, not a guarantee: model outputs are still not deterministic.
"""

import platform
import subprocess
from collections.abc import Mapping
from datetime import UTC, datetime
from decimal import Decimal
from importlib.metadata import PackageNotFoundError, version
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict

from agent_orchestration.agents.specs import AgentSpec
from agent_orchestration.guardrails import Limits
from agent_orchestration.prompts import load_prompt


class RunManifest(BaseModel):
    model_config = ConfigDict(frozen=True)

    run_id: UUID
    created_at: AwareDatetime
    git_sha: str | None  # None when git or the repo is unavailable (for example a container)
    python_version: str
    anthropic_version: str | None
    models: dict[str, str]  # agent name -> model id
    prompt_sha256: dict[str, str]  # agent name -> hash of the prompt file's bytes
    tools: dict[str, list[str]]  # agent name -> allowed tool names, sorted
    max_turns: int
    max_usd: Decimal
    max_revisions: int


def git_sha() -> str | None:
    """The current commit, or None. Never raises: a missing git must not stop a run."""
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, timeout=5, check=True
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() or None


def _anthropic_version() -> str | None:
    try:
        return version("anthropic")
    except PackageNotFoundError:
        return None


def build_manifest(*, run_id: UUID, specs: Mapping[str, AgentSpec], limits: Limits) -> RunManifest:
    """Collect the record. Reads each agent's prompt file, so a missing file fails loudly."""
    return RunManifest(
        run_id=run_id,
        created_at=datetime.now(UTC),
        git_sha=git_sha(),
        python_version=platform.python_version(),
        anthropic_version=_anthropic_version(),
        models={name: s.model for name, s in specs.items()},
        prompt_sha256={name: load_prompt(s.prompt_file).sha256 for name, s in specs.items()},
        tools={name: sorted(s.tools) for name, s in specs.items()},
        max_turns=limits.max_turns,
        max_usd=limits.max_usd,
        max_revisions=limits.max_revisions,
    )
