"""Acceptance tests for C11: audit-chain functions and provenance.check_claims.

Delete `pytestmark` to switch them on. Invariants for any encoding or chain structure: the
same event hashes identically twice, Decimal values are stable, changing any covered field
changes the hash, and a tampered or removed event makes verification fail.
"""

from collections.abc import Callable
from decimal import Decimal

import pytest

from agent_orchestration.audit import (
    GENESIS,
    AuditChainSink,
    AuditEntry,
    canonical_bytes,
    chain_hash,
    verify_chain,
)
from agent_orchestration.events import Event, EventType
from agent_orchestration.provenance import check_claims

pytestmark = [
    pytest.mark.human_todo,
    pytest.mark.skip(reason="C11 not written yet: docs/concepts/c11-audit-provenance.md"),
]

MakeEvent = Callable[..., Event]


def build_chain(events: list[Event]) -> list[AuditEntry]:
    sink = AuditChainSink()
    for e in events:
        sink.write(e)
    return sink.entries


def test_same_event_hashes_identically_twice(make_event: MakeEvent) -> None:
    e = make_event(0)
    assert canonical_bytes(e) == canonical_bytes(e)
    assert chain_hash(GENESIS, e) == chain_hash(GENESIS, e)


def test_decimal_cost_is_stable_and_exact(make_event: MakeEvent) -> None:
    a = make_event(0, cost_usd=Decimal("0.0010"))
    b = make_event(0, cost_usd=Decimal("0.0010"))
    assert canonical_bytes(a) == canonical_bytes(b)
    assert canonical_bytes(a) != canonical_bytes(make_event(0, cost_usd=Decimal("0.0011")))


def test_payload_key_order_does_not_change_the_bytes(make_event: MakeEvent) -> None:
    a = make_event(0, payload={"x": 1, "y": 2})
    b = make_event(0, payload={"y": 2, "x": 1})
    assert canonical_bytes(a) == canonical_bytes(b)


def test_hash_depends_on_the_previous_hash(make_event: MakeEvent) -> None:
    e = make_event(0)
    assert chain_hash(GENESIS, e) != chain_hash("f" * 64, e)


def test_intact_chain_verifies(make_event: MakeEvent) -> None:
    assert verify_chain(build_chain([make_event(i) for i in range(4)]))


def test_chain_detects_a_tampered_event(make_event: MakeEvent) -> None:
    entries = build_chain([make_event(i) for i in range(4)])
    forged = AuditEntry(make_event(1, text="edited"), entries[1].prev_hash, entries[1].hash)
    assert not verify_chain([entries[0], forged, *entries[2:]])


def test_chain_detects_a_removed_event(make_event: MakeEvent) -> None:
    entries = build_chain([make_event(i) for i in range(4)])
    assert not verify_chain([entries[0], *entries[2:]])


def test_check_claims_flags_a_figure_with_no_source(make_event: MakeEvent) -> None:
    events = [make_event(0, type=EventType.TOOL_RESULT, text="Revenues: 4,000,000,000 USD")]
    unsupported = check_claims("Revenue was $9.9bn.", events)
    assert unsupported


def test_check_claims_accepts_a_sourced_figure(make_event: MakeEvent) -> None:
    events = [make_event(0, type=EventType.TOOL_RESULT, text="Revenues: 4,000,000,000 USD")]
    assert check_claims("Revenue was 4,000,000,000 USD.", events) == []
