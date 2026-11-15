"""Shared test helpers."""

from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

import pytest

from agent_orchestration.events import Event, EventType

T0 = datetime(2026, 11, 15, 12, 0, tzinfo=UTC)
RUN_ID = UUID("00000000-0000-4000-8000-000000000001")


@pytest.fixture
def make_event() -> Callable[..., Event]:
    """Build an Event with sensible defaults; override any field by keyword.

    `after_ms` sets the timestamp relative to a fixed start time, so tests are deterministic.
    """

    def _make(seq: int = 0, *, after_ms: int = 0, **overrides: Any) -> Event:
        fields: dict[str, Any] = {
            "run_id": RUN_ID,
            "seq": seq,
            "ts": T0 + timedelta(milliseconds=after_ms),
            "agent": "supervisor",
            "type": EventType.MESSAGE,
            "text": f"step {seq}",
        }
        fields.update(overrides)
        return Event(**fields)

    return _make
