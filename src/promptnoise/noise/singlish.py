from __future__ import annotations

import random
import re


def singlish_pilot(text: str, rng: random.Random) -> tuple[str, list[dict]]:
    """Generate a *pilot-only* Singlish-like variant.

    This is not a substitute for native-speaker-authored/validated Singlish.
    Final Singlish benchmark items must be reviewed for naturalness and
    semantic equivalence by Singaporean annotators.
    """

    result = text
    edits: list[dict] = []

    transformations = [
        (r"\bCan you\b", "Can"),
        (r"\bCould you\b", "Can"),
        (r"\bIs it\b", "Issit"),
        (r"\bWhy is\b", "Why"),
        (r"\bWhich one is\b", "Which one"),
    ]

    for pattern, replacement in transformations:
        if rng.random() < 0.6 and re.search(pattern, result, flags=re.IGNORECASE):
            result, count = re.subn(pattern, replacement, result, count=1, flags=re.IGNORECASE)
            if count:
                edits.append({"operation": "singlish_syntax_pilot", "before": pattern, "after": replacement})

    if "?" in result and rng.random() < 0.75:
        particle = rng.choice(["ah", "leh"])
        result = result.replace("?", f" {particle}?", 1)
        edits.append({"operation": "singlish_particle_pilot", "after": particle})

    return result, edits
