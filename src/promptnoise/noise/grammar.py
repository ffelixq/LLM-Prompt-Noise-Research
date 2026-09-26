from __future__ import annotations

import random
import re


def grammar_noise(text: str, rng: random.Random) -> tuple[str, list[dict]]:
    """Create mild, intent-preserving grammatical compression.

    This is deliberately conservative. Final grammar conditions should be
    human-reviewed before the final benchmark is frozen.
    """

    result = text
    edits: list[dict] = []

    rules = [
        (r"\bCan you\b", "Can"),
        (r"\bCould you\b", "Can"),
        (r"\bWhat is\b", "What"),
        (r"\bWhich is\b", "Which"),
        (r"\bthe final\b", "final"),
        (r"\bthe resulting\b", "resulting"),
        (r"\bthe person's\b", "person's"),
    ]

    rng.shuffle(rules)
    for pattern, replacement in rules[:3]:
        if re.search(pattern, result, flags=re.IGNORECASE):
            result, count = re.subn(pattern, replacement, result, count=1, flags=re.IGNORECASE)
            if count:
                edits.append({"operation": "grammar_compression", "before": pattern, "after": replacement})

    # Remove one non-essential article where possible.
    article_matches = list(re.finditer(r"\b(a|an|the)\b\s*", result, flags=re.IGNORECASE))
    if article_matches and rng.random() < 0.7:
        match = rng.choice(article_matches)
        before = result[match.start():match.end()]
        result = result[:match.start()] + result[match.end():]
        edits.append({"operation": "article_omission", "before": before, "after": ""})

    return result, edits
