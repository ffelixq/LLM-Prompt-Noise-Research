from __future__ import annotations

from rapidfuzz.distance import Levenshtein


def character_metrics(clean: str, noisy: str) -> dict[str, float | int]:
    distance = Levenshtein.distance(clean, noisy)
    denom = max(len(clean), len(noisy), 1)
    return {
        "char_distance": int(distance),
        "normalized_char_distance": float(distance / denom),
    }


def word_distance(clean: str, noisy: str) -> int:
    return int(Levenshtein.distance(clean.split(), noisy.split()))
