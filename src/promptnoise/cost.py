from __future__ import annotations


def estimate_cost_usd(
    input_tokens: int | None,
    output_tokens: int | None,
    input_usd_per_million: float | None,
    output_usd_per_million: float | None,
) -> float | None:
    """Estimate request cost using a frozen, user-supplied pricing snapshot.

    Reasoning tokens are not billed separately here because provider accounting
    differs. If a provider reports reasoning inside output tokens, the output
    rate already captures it. Store reasoning tokens separately for analysis.
    """

    if (
        input_tokens is None
        or output_tokens is None
        or input_usd_per_million is None
        or output_usd_per_million is None
    ):
        return None

    return (
        input_tokens / 1_000_000 * input_usd_per_million
        + output_tokens / 1_000_000 * output_usd_per_million
    )
