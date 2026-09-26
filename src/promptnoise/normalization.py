from __future__ import annotations

import re
from typing import Protocol


TEXT_NORMALIZATIONS = {
    "u": "you",
    "ur": "your",
    "r": "are",
    "pls": "please",
    "bc": "because",
    "smth": "something",
    "shld": "should",
    "cld": "could",
    "wld": "would",
    "ppl": "people",
    "rn": "right now",
    "idk": "I do not know",
}


class TextGenerator(Protocol):
    def generate(self, prompt: str): ...


def deterministic_textese_normalize(text: str) -> str:
    result = text
    for short, full in TEXT_NORMALIZATIONS.items():
        result = re.sub(rf"\b{re.escape(short)}\b", full, result, flags=re.IGNORECASE)
    return result


def llm_normalize(generator: TextGenerator, text: str) -> str:
    instruction = (
        "Rewrite the user text into clear Standard English while preserving every "
        "number, named entity, code token, requested output format, and intended meaning. "
        "Do not answer the request. Return only the normalized request.\n\n"
        f"USER TEXT:\n{text}"
    )
    response = generator.generate(instruction)
    return response.text
