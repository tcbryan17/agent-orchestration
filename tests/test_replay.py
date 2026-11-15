"""to_site_events: Event list -> the portfolio site's {t, who, text} timeline."""

import json
from collections.abc import Callable

from agent_orchestration.events import Event, EventType, TokenUsage
from agent_orchestration.pricing import cost_from_usage
from agent_orchestration.replay import to_site_events

MakeEvent = Callable[..., Event]
HAIKU = "claude-haiku-5-5"


def model_call(make_event: MakeEvent, seq: int, after_ms: int, usage: TokenUsage) -> Event:
    return make_event(
        seq,
        after_ms=after_ms,
        agent="researcher",
        type=EventType.MODEL_CALL,
        model=HAIKU,
        usage=usage,
        cost_usd=cost_from_usage(usage, HAIKU),
    )


def test_no_events_gives_empty_timeline() -> None:
    assert to_site_events([]) == []


def test_entries_have_exactly_the_site_fields_and_are_json(make_event: MakeEvent) -> None:
    out = to_site_events([make_event(0)])
    assert out == [{"t": 0, "who": "supervisor", "text": "step 0"}]
    json.dumps(out)  # what gets pasted into the site's projects.js


def test_run_started_is_shown_as_the_user(make_event: MakeEvent) -> None:
    out = to_site_events([make_event(0, type=EventType.RUN_STARTED, text="Compare DKNG and RSI")])
    assert out[0]["who"] == "user"


def test_model_calls_and_tool_results_are_hidden(make_event: MakeEvent) -> None:
    events = [
        make_event(0, type=EventType.HANDOFF),
        make_event(1, type=EventType.MODEL_CALL),
        make_event(2, type=EventType.TOOL_CALL),
        make_event(3, type=EventType.TOOL_RESULT),
    ]
    assert [e["text"] for e in to_site_events(events)] == ["step 0", "step 2"]


def test_t_is_milliseconds_since_the_first_event(make_event: MakeEvent) -> None:
    events = [make_event(0, after_ms=5_000), make_event(1, after_ms=8_100)]
    assert [e["t"] for e in to_site_events(events)] == [0, 3_100]


def test_order_comes_from_seq_not_list_position(make_event: MakeEvent) -> None:
    events = [make_event(2, after_ms=200), make_event(0), make_event(1, after_ms=100)]
    assert [e["text"] for e in to_site_events(events)] == ["step 0", "step 1", "step 2"]


def test_clock_skew_never_makes_time_run_backwards(make_event: MakeEvent) -> None:
    # seq 1 was recorded with a timestamp before seq 0's: t holds steady instead of going < 0.
    events = [make_event(0, after_ms=1_000), make_event(1, after_ms=900)]
    assert [e["t"] for e in to_site_events(events)] == [0, 0]


def test_run_finished_line_totals_hidden_model_calls(make_event: MakeEvent) -> None:
    # Costs: 1,000 x 0.10 + 500 x 0.50 = $0.00035; 1,200 x 0.10 + 300 x 0.50 = $0.00027
    # Total $0.00062 -> "$0.0006" for display. Tokens 1,500 + 1,500 = 3.0k. 41s end to end.
    events = [
        make_event(0, type=EventType.RUN_STARTED, text="Compare DKNG and RSI"),
        model_call(make_event, 1, 2_000, TokenUsage(input_tokens=1_000, output_tokens=500)),
        model_call(make_event, 2, 9_000, TokenUsage(input_tokens=1_200, output_tokens=300)),
        make_event(3, after_ms=41_000, type=EventType.RUN_FINISHED, text="Done"),
    ]
    last = to_site_events(events)[-1]
    assert last == {
        "t": 41_000,
        "who": "supervisor",
        "text": "Done · 2 model calls · 3.0k tokens · $0.0006 · 41s",
    }
