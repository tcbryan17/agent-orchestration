"""SEC EDGAR `companyfacts` client: structured XBRL numbers for one company.

WHY a client class: the SEC asks every caller to identify itself with a User-Agent and to stay
under 10 requests/second, and filings never change once filed, so we throttle politely and
cache on disk. That also keeps tests and replays offline and free.
"""

import json
import time
from pathlib import Path
from typing import Any

import httpx2

COMPANIES: dict[str, int] = {
    "DraftKings": 1883685,
    "Flutter": 1635327,
    "Rush Street": 1793659,
    "Manchester United": 1549107,
}
ANNUAL_FORMS = frozenset({"10-K", "20-F"})
_MIN_INTERVAL_S = 0.1  # 10 requests per second at most


class EdgarClient:
    """Fetches `companyfacts` JSON with the required User-Agent, a throttle and a disk cache."""

    def __init__(
        self, user_agent: str | None, cache_dir: Path, http: httpx2.Client | None = None
    ) -> None:
        if not user_agent or not user_agent.strip():
            raise RuntimeError(
                "SEC_USER_AGENT is not set: the SEC rejects requests without a contact "
                "User-Agent. Put a project alias in .env."
            )
        self._user_agent = user_agent
        self._cache_dir = cache_dir
        self._http = http or httpx2.Client(timeout=30)
        self._last_request = 0.0

    def _throttle(self) -> None:
        wait = _MIN_INTERVAL_S - (time.monotonic() - self._last_request)
        if wait > 0:
            time.sleep(wait)
        self._last_request = time.monotonic()

    def company_facts(self, cik: int) -> dict[str, Any]:
        """Return the company's full XBRL facts, from the cache when we already have them."""
        cache_file = self._cache_dir / f"CIK{cik:010d}.json"
        if cache_file.exists():
            cached: dict[str, Any] = json.loads(cache_file.read_text())
            return cached
        self._throttle()
        response = self._http.get(
            f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json",
            headers={"User-Agent": self._user_agent},
        )
        response.raise_for_status()
        data: dict[str, Any] = response.json()
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps(data))
        return data


def annual_values(
    facts: dict[str, Any], taxonomy: str, concept: str, unit: str
) -> list[dict[str, Any]]:
    """Annual (fp == "FY", 10-K or 20-F) data points for one concept, with provenance.

    Each item: value, fy, end, plus accn/form/filed so any figure can be traced to its filing.
    Returns [] when the company doesn't report the concept (the caller decides what that means).
    """
    try:
        points = facts["facts"][taxonomy][concept]["units"][unit]
    except KeyError:
        return []
    return [
        {
            "value": p["val"],
            "fy": p.get("fy"),
            "end": p["end"],
            "accn": p["accn"],
            "form": p["form"],
            "filed": p["filed"],
        }
        for p in points
        if p.get("fp") == "FY" and p.get("form") in ANNUAL_FORMS
    ]
