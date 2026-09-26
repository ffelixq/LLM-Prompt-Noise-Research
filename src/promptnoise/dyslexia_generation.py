from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

import pandas as pd

from .metrics import character_metrics, word_distance
from .noise.dyslexia import dyslexia_noise

MODES = ["letter_order", "nonword", "homophone", "real_word_confusion"]


def _rng(seed: int, question_id: str, mode: str) -> random.Random:
    digest = hashlib.sha256(f"{seed}|{question_id}|{mode}".encode()).digest()
    return random.Random(int.from_bytes(digest[:8], "big"))


def generate_dyslexia_variants(
    benchmark: pd.DataFrame,
    seed: int = 20260927,
) -> pd.DataFrame:
    """Generate a separate accessibility-focused perturbation dataset.

    The labels describe literature-informed writing phenomena. They are not a
    simulation or diagnosis of dyslexia in any individual.
    """

    rows: list[dict] = []
    for _, source in benchmark.iterrows():
        qid = str(source["question_id"])
        clean = str(source["prompt"])
        for mode in MODES:
            noisy, edits = dyslexia_noise(clean, _rng(seed, qid, mode), mode)
            metrics = character_metrics(clean, noisy)
            rows.append(
                {
                    **source.to_dict(),
                    "condition": f"dyslexia_assoc_{mode}",
                    "clean_prompt": clean,
                    "test_prompt": noisy,
                    "generation_seed": seed,
                    **metrics,
                    "word_distance": word_distance(clean, noisy),
                    "semantic_status": "needs_review",
                    "perturbation_metadata": json.dumps(edits, ensure_ascii=False),
                }
            )
    return pd.DataFrame(rows)


def generate_dyslexia_file(
    input_path: str | Path,
    output_path: str | Path,
    seed: int,
) -> pd.DataFrame:
    benchmark = pd.read_csv(input_path)
    variants = generate_dyslexia_variants(benchmark, seed)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    variants.to_csv(output_path, index=False)
    return variants
