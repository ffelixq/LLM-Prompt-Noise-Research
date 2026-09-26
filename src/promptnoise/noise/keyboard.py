from __future__ import annotations

import random
import re
from dataclasses import dataclass

QWERTY_NEIGHBORS = {
    "q": "wa", "w": "qase", "e": "wsdr", "r": "edft", "t": "rfgy",
    "y": "tghu", "u": "yhji", "i": "ujko", "o": "iklp", "p": "ol",
    "a": "qwsz", "s": "awedxz", "d": "serfcx", "f": "drtgvc",
    "g": "ftyhbv", "h": "gyujnb", "j": "huikmn", "k": "jiolm",
    "l": "kop", "z": "asx", "x": "zsdc", "c": "xdfv", "v": "cfgb",
    "b": "vghn", "n": "bhjm", "m": "njk",
}


@dataclass
class KeyboardEdit:
    operation: str
    index: int
    before: str
    after: str


def _protected_spans(text: str, protected_tokens: list[str] | None) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    tokens = [t for t in (protected_tokens or []) if t]
    # Numbers are protected by default because changing them can change ground truth.
    tokens.extend(re.findall(r"\b\d+(?:\.\d+)?\b", text))

    for token in sorted(set(tokens), key=len, reverse=True):
        escaped = re.escape(token)
        # A protected token like "A" should protect answer choice A, not every
        # occurrence of the letter a inside ordinary words.
        pattern = rf"(?<!\w){escaped}(?!\w)" if token.isalnum() else escaped
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            spans.append((match.start(), match.end()))
    return spans


def _is_protected(index: int, spans: list[tuple[int, int]]) -> bool:
    return any(start <= index < end for start, end in spans)


def _adjacent_edit(chars: list[str], idx: int, rng: random.Random) -> KeyboardEdit | None:
    original = chars[idx]
    neighbors = QWERTY_NEIGHBORS.get(original.lower())
    if not neighbors:
        return None
    replacement = rng.choice(neighbors)
    if original.isupper():
        replacement = replacement.upper()
    chars[idx] = replacement
    return KeyboardEdit("adjacent", idx, original, replacement)


def keyboard_noise(
    text: str,
    rate: float,
    rng: random.Random,
    protected_tokens: list[str] | None = None,
) -> tuple[str, list[dict]]:
    """Apply QWERTY-aware character noise.

    The target number of edits is based on eligible alphabetic characters.
    Numbers and supplied protected tokens are not modified. A positive noise
    rate is guaranteed to produce at least one actual edit when an eligible
    alphabetic character exists.
    """

    chars = list(text)
    spans = _protected_spans(text, protected_tokens)
    eligible = [
        i for i, ch in enumerate(chars)
        if ch.isalpha() and not _is_protected(i, spans)
    ]
    if not eligible or rate <= 0:
        return text, []

    target = max(1, round(len(eligible) * rate))
    chosen = sorted(rng.sample(eligible, k=min(target, len(eligible))), reverse=True)
    edits: list[KeyboardEdit] = []

    for idx in chosen:
        if idx >= len(chars) or not chars[idx].isalpha():
            continue

        original = chars[idx]
        op = rng.choice(["adjacent", "delete", "insert", "transpose"])

        if op == "adjacent":
            edit = _adjacent_edit(chars, idx, rng)
            if edit:
                edits.append(edit)

        elif op == "delete":
            del chars[idx]
            edits.append(KeyboardEdit(op, idx, original, ""))

        elif op == "insert":
            neighbors = QWERTY_NEIGHBORS.get(original.lower(), original.lower())
            inserted = rng.choice(neighbors)
            chars.insert(idx, inserted)
            edits.append(KeyboardEdit(op, idx, "", inserted))

        elif op == "transpose":
            can_transpose = (
                idx + 1 < len(chars)
                and chars[idx + 1].isalpha()
                and not _is_protected(idx + 1, spans)
            )
            if can_transpose:
                before = chars[idx] + chars[idx + 1]
                chars[idx], chars[idx + 1] = chars[idx + 1], chars[idx]
                after = chars[idx] + chars[idx + 1]
                edits.append(KeyboardEdit(op, idx, before, after))
            else:
                # Do not let a randomly invalid transposition create a zero-noise row.
                edit = _adjacent_edit(chars, idx, rng)
                if edit:
                    edits.append(edit)

    if not edits:
        # Defensive fallback for any unforeseen edge case.
        idx = eligible[0]
        edit = _adjacent_edit(chars, idx, rng)
        if edit:
            edits.append(edit)

    return "".join(chars), [e.__dict__ for e in edits]
