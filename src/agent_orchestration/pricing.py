"""Dollar cost of a model call, worked out from the `usage` block of its response.

Cost is stored on each `Event` at the moment it happens, at the prices in force then (prices
change; history shouldn't). Money is `Decimal` throughout: costs per call are tiny (around
$0.0001), they get summed thousands of times, and the audit log hashes their text form, so they
must be exact and print the same way every time.

Prices are USD per million tokens, copied from the pricing page on PRICES_AS_OF.
Cache writes use the 5-minute TTL rate: the project doesn't use the 1-hour cache.
"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from agent_orchestration.events import TokenUsage

PRICES_AS_OF = "2026-11-15"
PRICES_SOURCE = "https://platform.claude.com/docs/en/about-claude/pricing"

PER_MILLION = Decimal(1_000_000)


class RateCard(BaseModel):
    """USD per million tokens for each kind of token, at one pricing tier."""

    model_config = ConfigDict(frozen=True)

    input: Decimal
    output: Decimal
    cache_write: Decimal  # 5-minute TTL
    cache_read: Decimal


class LongContextPricing(BaseModel):
    """A second rate card for requests whose prompt is longer than `threshold` tokens."""

    model_config = ConfigDict(frozen=True)

    threshold: int
    rates: RateCard


class ModelPricing(BaseModel):
    """Prices for one model. `long_context` is None for models with one price at any length."""

    model_config = ConfigDict(frozen=True)

    standard: RateCard
    long_context: LongContextPricing | None = None


# Strings, not floats, into Decimal: Decimal(0.1) would carry float's rounding error with it.
PRICING: dict[str, ModelPricing] = {
    "claude-haiku-5-5": ModelPricing(
        standard=RateCard(
            input=Decimal("0.10"),
            output=Decimal("0.50"),
            cache_write=Decimal("0.125"),
            cache_read=Decimal("0.01"),
        ),
        long_context=LongContextPricing(
            threshold=100_000,
            rates=RateCard(
                input=Decimal("0.50"),
                output=Decimal("2.50"),
                cache_write=Decimal("0.625"),
                cache_read=Decimal("0.05"),
            ),
        ),
    ),
}


def cost_from_usage(usage: TokenUsage, model: str) -> Decimal:
    """Return the USD cost of one Messages API call, as an exact Decimal (not rounded)."""
    pricing = PRICING[model]

    prompt_tokens = (
        usage.input_tokens + usage.cache_creation_input_tokens + usage.cache_read_input_tokens
    )

    rates = pricing.standard
    if pricing.long_context is not None and prompt_tokens > pricing.long_context.threshold:
        rates = pricing.long_context.rates

    total = (
        usage.input_tokens * rates.input
        + usage.output_tokens * rates.output
        + usage.cache_creation_input_tokens * rates.cache_write
        + usage.cache_read_input_tokens * rates.cache_read
    )
    return total / PER_MILLION
