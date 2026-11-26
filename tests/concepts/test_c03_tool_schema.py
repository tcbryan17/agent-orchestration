"""Acceptance tests for C3, tools.schemas.edgar_schema. Delete `pytestmark` to switch on."""

from typing import Any, cast

import pytest

from agent_orchestration.tools.schemas import edgar_schema

pytestmark = [
    pytest.mark.human_todo,
    pytest.mark.skip(reason="C3 not written yet: docs/concepts/c03-tool-schema.md"),
]


def test_schema_is_well_formed() -> None:
    schema = edgar_schema()
    assert schema["name"]
    assert schema["input_schema"]["type"] == "object"
    assert str(schema.get("description", "")).strip()


def test_schema_requires_the_company() -> None:
    input_schema = cast(dict[str, Any], edgar_schema()["input_schema"])
    required = input_schema.get("required", [])
    assert any("company" in str(r).lower() or "cik" in str(r).lower() for r in required)
