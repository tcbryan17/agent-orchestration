"""Tests for agent specs, prompt loading and the run manifest."""

import hashlib
from decimal import Decimal
from pathlib import Path
from uuid import UUID

import pytest

from agent_orchestration.agents.specs import SPECS, AgentSpec
from agent_orchestration.config import settings
from agent_orchestration.guardrails import Limits
from agent_orchestration.manifest import build_manifest
from agent_orchestration.prompts import load_prompt
from agent_orchestration.supervisor import supervisor_tools

DRAFTED = ("researcher", "analyst", "writer")  # supervisor and reviewer prompts are the owner's


def test_five_agents_with_the_readme_tools() -> None:
    assert set(SPECS) == {"supervisor", "researcher", "analyst", "writer", "reviewer"}
    assert SPECS["researcher"].tools == {"edgar_company_facts"}
    assert SPECS["analyst"].tools == {"calculator", "build_table"}
    assert SPECS["writer"].tools == frozenset()
    assert SPECS["reviewer"].tools == frozenset()
    assert "finish" in SPECS["supervisor"].tools


def test_models_default_to_the_configured_default() -> None:
    assert {s.model for s in SPECS.values()} == {settings.default_model}


def test_specs_are_frozen() -> None:
    with pytest.raises(AttributeError):
        SPECS["writer"].model = "other"  # type: ignore[misc]


@pytest.mark.parametrize("name", DRAFTED)
def test_drafted_prompts_exist_and_forbid_betting_tips(name: str) -> None:
    text = load_prompt(SPECS[name].prompt_file).text
    assert "betting tips" in text


@pytest.mark.parametrize("name", ["supervisor", "reviewer"])
def test_owner_prompts_are_templates_with_a_todo(name: str) -> None:
    assert "TODO(human)" in load_prompt(SPECS[name].prompt_file).text


def test_prompt_hash_is_of_the_file_bytes(tmp_path: Path) -> None:
    f = tmp_path / "p.md"
    f.write_bytes(b"hello")
    p = load_prompt(f)
    assert p.text == "hello"
    assert p.sha256 == hashlib.sha256(b"hello").hexdigest()


def test_manifest_records_models_prompts_limits_and_tools() -> None:
    run_id = UUID("00000000-0000-4000-8000-000000000001")
    limits = Limits(max_turns=7, max_usd=Decimal("0.25"), max_revisions=1)
    m = build_manifest(run_id=run_id, specs=SPECS, limits=limits)

    assert m.run_id == run_id and m.created_at.tzinfo is not None
    assert m.models["analyst"] == settings.default_model
    assert m.prompt_sha256["writer"] == load_prompt(SPECS["writer"].prompt_file).sha256
    assert m.tools["analyst"] == ["build_table", "calculator"]
    assert (m.max_turns, m.max_usd, m.max_revisions) == (7, Decimal("0.25"), 1)
    assert m.python_version and (m.git_sha is None or len(m.git_sha) >= 7)


def test_manifest_is_frozen() -> None:
    m = build_manifest(run_id=UUID(int=1), specs=SPECS, limits=Limits())
    with pytest.raises(ValueError):
        m.max_turns = 99


def test_supervisor_tools_are_one_delegate_per_worker_plus_finish() -> None:
    names = [t["name"] for t in supervisor_tools(SPECS)]
    assert names == [
        "delegate_researcher",
        "delegate_analyst",
        "delegate_writer",
        "delegate_reviewer",
        "finish",
    ]
    delegate = supervisor_tools(SPECS)[0]
    assert delegate["input_schema"]["required"] == ["brief"]


def test_supervisor_tools_match_the_supervisor_spec() -> None:
    names = {t["name"] for t in supervisor_tools(SPECS)}
    assert names == SPECS["supervisor"].tools


def test_agentspec_can_be_built_directly() -> None:
    spec = AgentSpec("x", "m", Path("p.md"), frozenset({"t"}), 10)
    assert spec.tools == {"t"}
