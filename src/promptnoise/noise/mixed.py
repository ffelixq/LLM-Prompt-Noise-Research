from __future__ import annotations

import random

from .grammar import grammar_noise
from .keyboard import keyboard_noise
from .textese import textese_noise


def mixed_realistic_noise(
    text: str,
    rng: random.Random,
    protected_tokens: list[str] | None = None,
) -> tuple[str, list[dict]]:
    result, e1 = textese_noise(text, rng, probability=0.75)
    result, e2 = grammar_noise(result, rng)
    result, e3 = keyboard_noise(result, rate=0.05, rng=rng, protected_tokens=protected_tokens)
    return result, e1 + e2 + e3
