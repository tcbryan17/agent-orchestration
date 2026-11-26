"""Tamper-evident audit log (C11): each event is chained to the one before it.

The idea: every entry stores a hash that covers the event AND the previous entry's hash. Edit
or delete any past event and every later hash stops matching, so tampering is detectable by
anyone who re-computes the chain. It proves integrity, not truth: a chain over false events
is still false.

Boilerplate here: `AuditEntry` and `AuditChainSink`, which plugs into the recorder like any
other sink. The three functions that decide what is hashed and how are C11 and are yours.
"""

from collections.abc import Sequence
from dataclasses import dataclass

from agent_orchestration.events import Event

# The "previous hash" of the first entry. Any fixed value works; what matters is that it is
# a constant everyone agrees on, so a verifier knows where the chain starts.
GENESIS = "0" * 64


@dataclass(frozen=True)
class AuditEntry:
    """One link: the event, the hash before it, and the hash covering both."""

    event: Event
    prev_hash: str
    hash: str


class AuditChainSink:
    """An `EventSink` (recorder.py) that appends a hash-chained entry per event."""

    def __init__(self) -> None:
        self.entries: list[AuditEntry] = []

    def write(self, event: Event) -> None:
        prev = self.entries[-1].hash if self.entries else GENESIS
        self.entries.append(AuditEntry(event, prev, chain_hash(prev, event)))


def canonical_bytes(event: Event) -> bytes:
    """TODO(human) C11: turn an event into bytes that are always identical for the same event.

    Hashing needs one exact byte sequence per event. JSON can write the same data many ways
    (key order, spacing, how a Decimal or datetime is printed), and any difference changes
    the hash.

      A. Canonical JSON: sorted keys, no extra whitespace, Decimal written as text (never
         float), timestamps in one fixed format. Readable, easy to verify in another
         language; you must define each type's text form.
      B. A custom binary or length-prefixed encoding: unambiguous; harder to read and to
         verify by hand.

    Also decide which fields are covered. GDPR Art. 17 (erasure) collides with immutability:
    if the chain covers personal data, deleting it breaks the chain. Options: keep personal
    data out of chained fields (hash a pointer; the data sits in a deletable table);
    crypto-shredding (encrypt it, destroy the key); or redact before hashing (the chain
    proves the redacted record, not the original).

    Guide: docs/concepts/c11-audit-provenance.md
    Governance: EU AI Act Art. 12-style logs; ISO/IEC 42001 event logging; GDPR Art. 17.
    """
    raise NotImplementedError("C11: see docs/concepts/c11-audit-provenance.md")


def chain_hash(prev_hash: str, event: Event) -> str:
    """TODO(human) C11: the hash that links `event` to everything before it.

    Combine `prev_hash` and `canonical_bytes(event)` with a cryptographic hash (SHA-256 is
    in the standard library). Decide how they are joined so two different (prev, event) pairs
    can never produce the same input bytes (for example a separator or length prefix).

    Which structure?

      A. A hash chain: simple, one pass to verify; proving one entry exists means sending
         the whole chain.
      B. A Merkle tree: a short proof for any single entry; more code, more moving parts.
      C. Signed entries (a key signs each hash): proves WHO wrote it, not just that it is
         unchanged; needs key storage and rotation.

    Guide: docs/concepts/c11-audit-provenance.md
    Governance: EU AI Act Art. 12-style logs; ISO/IEC 42001 event logging.
    """
    raise NotImplementedError("C11: see docs/concepts/c11-audit-provenance.md")


def verify_chain(entries: Sequence[AuditEntry]) -> bool:
    """TODO(human) C11: return True only if the chain is intact from GENESIS to the end.

    Recompute every hash from the entries' events (never trust the stored `hash`), and check
    that each entry's `prev_hash` is the one before it. Decide what an empty chain returns,
    and whether to report WHERE it broke (more useful) or only that it broke.

    Guide: docs/concepts/c11-audit-provenance.md
    Governance: EU AI Act Art. 12-style logs; ISO/IEC 42001 event logging.
    """
    raise NotImplementedError("C11: see docs/concepts/c11-audit-provenance.md")
