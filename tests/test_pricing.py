"""cost_from_usage: Haiku 5.5 prices as of 2026-11-15 (see pricing.PRICES_AS_OF).

Expected values are worked by hand in the comments, so a failure shows which rule broke.
"""

from decimal import Decimal

import pytest

from agent_orchestration.events import TokenUsage
from agent_orchestration.pricing import cost_from_usage

HAIKU = "claude-haiku-5-5"


def test_no_tokens_costs_nothing() -> None:
    assert cost_from_usage(TokenUsage(), HAIKU) == Decimal(0)


def test_returns_decimal_not_float() -> None:
    cost = cost_from_usage(TokenUsage(input_tokens=1), HAIKU)
    assert isinstance(cost, Decimal)


def test_input_and_output_at_standard_rates() -> None:
    # 1,000 x $0.10 + 500 x $0.50 = $350 per million tokens -> $0.00035
    usage = TokenUsage(input_tokens=1_000, output_tokens=500)
    assert cost_from_usage(usage, HAIKU) == Decimal("0.00035")


def test_cache_writes_and_reads_have_their_own_rates() -> None:
    # 2,000 x 0.10 + 10,000 x 0.125 + 50,000 x 0.01 + 1,000 x 0.50
    # = 200 + 1,250 + 500 + 500 = 2,450 per million -> $0.00245
    usage = TokenUsage(
        input_tokens=2_000,
        cache_creation_input_tokens=10_000,
        cache_read_input_tokens=50_000,
        output_tokens=1_000,
    )
    assert cost_from_usage(usage, HAIKU) == Decimal("0.00245")


def test_prompt_of_exactly_100k_stays_on_standard_rates() -> None:
    # "Over 100,000" means 100,000 itself is standard: 100,000 x 0.10 -> $0.01
    usage = TokenUsage(input_tokens=100_000)
    assert cost_from_usage(usage, HAIKU) == Decimal("0.01")


def test_prompt_over_100k_reprices_the_whole_request() -> None:
    # 100,001 > 100,000, so every token (not just the excess) is at $0.50 -> $0.0500005
    usage = TokenUsage(input_tokens=100_001)
    assert cost_from_usage(usage, HAIKU) == Decimal("0.0500005")


def test_cache_reads_count_toward_the_threshold() -> None:
    # Prompt = 1,000 input + 99,001 cache reads = 100,001 -> long-context card, output included:
    # 1,000 x 0.50 + 99,001 x 0.05 + 1,000 x 2.50 = 500 + 4,950.05 + 2,500 -> $0.00795005
    usage = TokenUsage(input_tokens=1_000, cache_read_input_tokens=99_001, output_tokens=1_000)
    assert cost_from_usage(usage, HAIKU) == Decimal("0.00795005")


def test_output_tokens_do_not_count_toward_the_threshold() -> None:
    # Prompt is 1,000 tokens; 200,000 output tokens don't make it "long context".
    # 1,000 x 0.10 + 200,000 x 0.50 = 100 + 100,000 -> $0.1001
    usage = TokenUsage(input_tokens=1_000, output_tokens=200_000)
    assert cost_from_usage(usage, HAIKU) == Decimal("0.1001")


def test_unknown_model_raises_instead_of_costing_zero() -> None:
    # A silent $0 would let the dollar guardrail under-count. KeyError is what a dict lookup
    # raises; change this if you choose a different exception.
    with pytest.raises(KeyError):
        cost_from_usage(TokenUsage(input_tokens=1), "claude-imaginary-1")
