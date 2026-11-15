"""Export a run's events to the portfolio site's replay format: `{t, who, text}`.

The site (../portfolio-site) plays a recorded run as a timeline: each entry appears `t`
milliseconds after the start, labelled `who`, with one line of `text`, and is shown as
"+3.1 s". The site renders text with `textContent`, so event text (which may quote SEC or
Companies House data) is never interpreted as HTML.

Only the steps a reader cares about are shown. Model calls and raw tool results are hidden
(a run can have dozens), but they still count: the final line totals their tokens, cost and
time, which is the "every step is traced" claim in one sentence.
"""

from collections.abc import Iterable, Sequence
from datetime import timedelta
from decimal import Decimal
from typing import TypedDict

from agent_orchestration.events import Event, EventType, TokenUsage

HIDDEN = frozenset({EventType.MODEL_CALL, EventType.TOOL_RESULT})


class SiteEvent(TypedDict):
    t: int  # milliseconds after the run started, real time (the site shows it as "+X s")
    who: str
    text: str


def to_site_events(events: Iterable[Event]) -> list[SiteEvent]:
    """Convert one run's events to the site's timeline entries, in run order."""
    ordered = sorted(events, key=lambda e: e.seq)  # seq is the order; ts only says when
    if not ordered:
        return []

    start = ordered[0].ts
    t = 0
    out: list[SiteEvent] = []
    for event in ordered:
        # Clock skew could put a later event at an earlier time; never let the timeline
        # run backwards.
        t = max(t, (event.ts - start) // timedelta(milliseconds=1))
        if event.type in HIDDEN:
            continue
        who = "user" if event.type is EventType.RUN_STARTED else event.agent
        text = event.text
        if event.type is EventType.RUN_FINISHED:
            text = f"{event.text} · {run_summary(ordered)}"
        out.append(SiteEvent(t=t, who=who, text=text))
    return out


def run_summary(events: Sequence[Event]) -> str:
    """One line of run totals, e.g. "6 model calls · 18.4k tokens · $0.0900 · 41s"."""
    calls = sum(1 for e in events if e.type is EventType.MODEL_CALL)
    tokens = sum(_total_tokens(e.usage) for e in events if e.usage is not None)
    cost = sum((e.cost_usd for e in events if e.cost_usd is not None), Decimal(0))
    seconds = (max(e.ts for e in events) - min(e.ts for e in events)).total_seconds()
    # Rounded here, for display only; the events keep the exact Decimal.
    return f"{calls} model calls · {tokens / 1000:.1f}k tokens · ${cost:.4f} · {seconds:.0f}s"


def _total_tokens(usage: TokenUsage) -> int:
    return (
        usage.input_tokens
        + usage.output_tokens
        + usage.cache_creation_input_tokens
        + usage.cache_read_input_tokens
    )
