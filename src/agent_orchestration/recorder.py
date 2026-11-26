"""The recorder: the one place events are created, numbered and handed on.

Agents never build an `Event` themselves. They call `Recorder.emit()`, which fills in the
`run_id` and the next `seq`, so ordering can't drift between agents, and passes the event to
every sink. A sink is anything that wants to see events as they happen: an in-memory list
for tests, Postgres and the SSE stream later (Phase 6), and the hash-chained audit log (C11).

Why a separate class rather than a global list: one recorder per run keeps runs isolated, and
making `seq` the recorder's job (not the caller's) is what lets `seq` be trusted as the order.
"""

from collections.abc import Iterable
from decimal import Decimal
from typing import Any, Protocol
from uuid import UUID, uuid4

from agent_orchestration.events import Event, EventType, TokenUsage


class EventSink(Protocol):
    """Receives every event of a run, in `seq` order, as soon as it is emitted."""

    def write(self, event: Event) -> None: ...


class MemorySink:
    """Keeps events in a list. Used by tests and by the replay export."""

    def __init__(self) -> None:
        self.events: list[Event] = []

    def write(self, event: Event) -> None:
        self.events.append(event)


class Recorder:
    """Numbers and distributes the events of one run."""

    def __init__(self, run_id: UUID | None = None, sinks: Iterable[EventSink] = ()) -> None:
        self.run_id = run_id or uuid4()
        self._sinks = list(sinks)
        self._memory = MemorySink()
        self._sinks.append(self._memory)
        self._next_seq = 0

    @property
    def events(self) -> list[Event]:
        """Every event emitted so far, in order. A copy: the log itself is append-only."""
        return list(self._memory.events)

    def emit(
        self,
        *,
        agent: str,
        type: EventType,
        text: str,
        parent_id: UUID | None = None,
        payload: dict[str, Any] | None = None,
        model: str | None = None,
        usage: TokenUsage | None = None,
        cost_usd: Decimal | None = None,
        latency_ms: int | None = None,
    ) -> Event:
        """Create the next event, send it to every sink, and return it.

        The returned event's `event_id` is what a child step passes as its `parent_id`.
        """
        event = Event(
            run_id=self.run_id,
            seq=self._next_seq,
            parent_id=parent_id,
            agent=agent,
            type=type,
            text=text,
            payload=payload or {},
            model=model,
            usage=usage,
            cost_usd=cost_usd,
            latency_ms=latency_ms,
        )
        self._next_seq += 1
        for sink in self._sinks:
            sink.write(event)
        return event
