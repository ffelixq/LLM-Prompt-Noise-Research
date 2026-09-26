from __future__ import annotations

import random
import re

REPLACEMENTS = {
    "you": "u",
    "your": "ur",
    "are": "r",
    "please": "pls",
    "because": "bc",
    "something": "smth",
    "should": "shld",
    "could": "cld",
    "would": "wld",
    "with": "w",
    "without": "w/o",
    "before": "b4",
    "people": "ppl",
    "message": "msg",
}


def textese_noise(text: str, rng: random.Random, probability: float = 0.65) -> tuple[str, list[dict]]:
    result = text
    edits: list[dict] = []

    phrase_rules = [
        (r"\bright now\b", "rn"),
        (r"\bi do not know\b", "idk"),
        (r"\bi don't know\b", "idk"),
        (r"\bgoing to\b", "gna"),
        (r"\bwant to\b", "wna"),
    ]

    for pattern, replacement in phrase_rules:
        if rng.random() <= probability and re.search(pattern, result, flags=re.IGNORECASE):
            result, count = re.subn(pattern, replacement, result, count=1, flags=re.IGNORECASE)
            if count:
                edits.append({"operation": "textese", "before": pattern, "after": replacement})

    for word, replacement in REPLACEMENTS.items():
        if rng.random() > probability:
            continue
        pattern = rf"\b{re.escape(word)}\b"
        if re.search(pattern, result, flags=re.IGNORECASE):
            result, count = re.subn(pattern, replacement, result, count=1, flags=re.IGNORECASE)
            if count:
                edits.append({"operation": "textese", "before": word, "after": replacement})

    return result, edits
