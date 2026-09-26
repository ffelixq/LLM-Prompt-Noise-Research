from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

import pandas as pd

from .metrics import character_metrics, word_distance
from .noise import (
    grammar_noise,
    keyboard_noise,
    mixed_realistic_noise,
    singlish_pilot,
    textese_noise,
)


CONDITIONS = [
    "clean",
    "typo_02",
    "typo_05",
    "typo_10",
    "typo_20",
    "grammar",
    "textese",
    "singlish_pilot",
    "mixed_realistic",
]


def _stable_rng(seed: int, question_id: str, condition: str) -> random.Random:
    payload = f"{seed}|{question_id}|{condition}".encode()
    digest = hashlib.sha256(payload).digest()
    local_seed = int.from_bytes(digest[:8], "big")
    return random.Random(local_seed)


def _protected(value: object) -> list[str]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    return [part.strip() for part in str(value).split("|") if part.strip()]


def generate_variants(
    benchmark: pd.DataFrame,
    seed: int = 20260927,
) -> pd.DataFrame:
    rows: list[dict] = []

    required = {"question_id", "task_type", "prompt", "expected_answer", "scorer"}
    missing = required - set(benchmark.columns)
    if missing:
        raise ValueError(f"Benchmark missing required columns: {sorted(missing)}")

    for _, source in benchmark.iterrows():
        qid = str(source["question_id"])
        clean = str(source["prompt"])
        protected = _protected(source.get("protected_tokens"))

        for condition in CONDITIONS:
            rng = _stable_rng(seed, qid, condition)
            metadata: list[dict] = []

            if condition == "clean":
                noisy = clean
            elif condition.startswith("typo_"):
                rate = int(condition.split("_")[1]) / 100
                noisy, metadata = keyboard_noise(clean, rate, rng, protected)
            elif condition == "grammar":
                noisy, metadata = grammar_noise(clean, rng)
            elif condition == "textese":
                noisy, metadata = textese_noise(clean, rng)
            elif condition == "singlish_pilot":
                noisy, metadata = singlish_pilot(clean, rng)
            elif condition == "mixed_realistic":
                noisy, metadata = mixed_realistic_noise(clean, rng, protected)
            else:
                raise ValueError(condition)

            metrics = character_metrics(clean, noisy)
            rows.append(
                {
                    **source.to_dict(),
                    "condition": condition,
                    "clean_prompt": clean,
                    "test_prompt": noisy,
                    "generation_seed": seed,
                    **metrics,
                    "word_distance": word_distance(clean, noisy),
                    "semantic_status": (
                        "surface_preserving" if condition == "clean" else "needs_review"
                    ),
                    "perturbation_metadata": json.dumps(metadata, ensure_ascii=False),
                }
            )

    return pd.DataFrame(rows)


def generate_file(input_path: str | Path, output_path: str | Path, seed: int) -> pd.DataFrame:
    benchmark = pd.read_csv(input_path)
    variants = generate_variants(benchmark, seed=seed)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    variants.to_csv(output_path, index=False)
    return variants
