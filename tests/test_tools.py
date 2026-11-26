import json
from decimal import Decimal
from pathlib import Path

import httpx2
import pytest

from agent_orchestration.tools.calculator import calculate
from agent_orchestration.tools.edgar import COMPANIES, EdgarClient, annual_values
from agent_orchestration.tools.table import build_table

FIXTURE = Path(__file__).parent / "fixtures" / "edgar" / "CIK0001883685.json"


def make_client(tmp_path: Path, seen: list[httpx2.Request]) -> EdgarClient:
    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return httpx2.Response(200, json=json.loads(FIXTURE.read_text()))

    http = httpx2.Client(transport=httpx2.MockTransport(handler))
    return EdgarClient("test-alias a@example.com", tmp_path, http)


def test_edgar_sends_user_agent_and_padded_cik(tmp_path: Path) -> None:
    seen: list[httpx2.Request] = []
    make_client(tmp_path, seen).company_facts(COMPANIES["DraftKings"])
    assert seen[0].headers["User-Agent"] == "test-alias a@example.com"
    assert seen[0].url.path.endswith("/CIK0001883685.json")


def test_edgar_cache_avoids_second_request(tmp_path: Path) -> None:
    seen: list[httpx2.Request] = []
    client = make_client(tmp_path, seen)
    first = client.company_facts(1883685)
    second = client.company_facts(1883685)
    assert len(seen) == 1 and first == second


@pytest.mark.parametrize("agent", [None, "", "   "])
def test_edgar_requires_user_agent(tmp_path: Path, agent: str | None) -> None:
    with pytest.raises(RuntimeError, match="SEC_USER_AGENT"):
        EdgarClient(agent, tmp_path)


def test_annual_values_keeps_only_annual_with_provenance() -> None:
    facts = json.loads(FIXTURE.read_text())
    values = annual_values(facts, "us-gaap", "Revenues", "USD")
    assert [v["value"] for v in values] == [1000, 1500]
    assert values[0]["accn"] == "0000000000-24-000001"
    assert {"form", "filed", "end"} <= values[0].keys()
    assert annual_values(facts, "us-gaap", "Nope", "USD") == []


def test_calculator_valid() -> None:
    assert calculate("(1500 - 1000) / 1000") == Decimal("0.5")
    assert calculate("-2 * 3") == Decimal(-6)
    assert calculate("0.1 + 0.2") == Decimal("0.3")


@pytest.mark.parametrize(
    "expr", ["__import__('os')", "x + 1", "abs(-1)", "2 ** 3", "1 / 0", "True", "'a'", ""]
)
def test_calculator_rejects(expr: str) -> None:
    with pytest.raises(ValueError):
        calculate(expr)


def test_table() -> None:
    out = build_table(["Club", "Ratio"], [["A", "0.7"], ["B", "0.8"]])
    assert out.splitlines() == ["| Club | Ratio |", "| --- | --- |", "| A | 0.7 |", "| B | 0.8 |"]


def test_table_rejects_ragged_rows() -> None:
    with pytest.raises(ValueError, match="row 1"):
        build_table(["a", "b"], [["1", "2"], ["3"]])
