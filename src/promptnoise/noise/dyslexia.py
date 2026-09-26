from __future__ import annotations

import random
import re

HOMOPHONES = {
    "their": "there",
    "there": "their",
    "to": "too",
    "too": "to",
    "your": "you're",
    "you're": "your",
}

REAL_WORD_CONFUSIONS = {
    "from": "form",
    "form": "from",
    "then": "than",
    "than": "then",
    "quiet": "quite",
    "quite": "quiet",
}


def dyslexia_noise(text: str, rng: random.Random, mode: str) -> tuple[str, list[dict]]:
    """Literature-informed synthetic perturbations.

    These are *dyslexia-associated writing phenomena*, not diagnostic markers
    and not a simulation of any individual person's dyslexia.
    """

    result = text
    edits: list[dict] = []

    if mode == "homophone":
        mapping = HOMOPHONES
    elif mode == "real_word_confusion":
        mapping = REAL_WORD_CONFUSIONS
    elif mode == "letter_order":
        words = list(re.finditer(r"\b[A-Za-z]{5,}\b", result))
        if not words:
            return result, edits
        match = rng.choice(words)
        word = match.group(0)
        i = rng.randint(1, len(word) - 2)
        chars = list(word)
        chars[i], chars[i + 1] = chars[i + 1], chars[i]
        changed = "".join(chars)
        result = result[:match.start()] + changed + result[match.end():]
        edits.append({"operation": "letter_order", "before": word, "after": changed})
        return result, edits
    elif mode == "nonword":
        words = list(re.finditer(r"\b[A-Za-z]{5,}\b", result))
        if not words:
            return result, edits
        match = rng.choice(words)
        word = match.group(0)
        i = rng.randint(1, len(word) - 2)
        changed = word[:i] + word[i + 1:]
        result = result[:match.start()] + changed + result[match.end():]
        edits.append({"operation": "letter_deletion", "before": word, "after": changed})
        return result, edits
    else:
        raise ValueError(f"Unsupported dyslexia noise mode: {mode}")

    candidates = []
    for before, after in mapping.items():
        match = re.search(rf"\b{re.escape(before)}\b", result, flags=re.IGNORECASE)
        if match:
            candidates.append((match, before, after))

    if candidates:
        match, before, after = rng.choice(candidates)
        result = result[:match.start()] + after + result[match.end():]
        edits.append({"operation": mode, "before": before, "after": after})

    return result, edits
