from __future__ import annotations


# ==================================================
# COST FOLLOW-UP KEYWORDS
# ==================================================

_COST_KEYWORDS = {
    "cost",
    "costs",
    "price",
    "pricing",
    "expense",
    "expenses",
    "rate",
    "rates",
    "amount",
    "budget",
    "charge",
    "charges",
    "how much",
    "what would it cost",
    "what will it cost",
    "how much would",
    "how much will",
}


def is_cost_question(
    question: str,
) -> bool:
    """
    Determine whether the user's current question
    is asking about cost or pricing.

    This is intentionally deterministic.

    We do not use the LLM for intent detection because
    cost retrieval needs predictable behaviour.
    """

    normalized = (
        question
        .strip()
        .lower()
    )

    if not normalized:
        return False

    for keyword in _COST_KEYWORDS:

        if keyword in normalized:
            return True

    return False