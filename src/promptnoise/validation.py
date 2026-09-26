from __future__ import annotations

import pandas as pd

from .generation import CONDITIONS


def validate_variants(df: pd.DataFrame) -> list[str]:
    issues: list[str] = []
    required = {
        "question_id",
        "condition",
        "clean_prompt",
        "test_prompt",
        "expected_answer",
        "scorer",
        "normalized_char_distance",
    }
    missing = required - set(df.columns)
    if missing:
        return [f"Missing columns: {sorted(missing)}"]

    duplicated = df.duplicated(subset=["question_id", "condition"]).sum()
    if duplicated:
        issues.append(f"{duplicated} duplicate question/condition rows")

    per_question = df.groupby("question_id")["condition"].nunique()
    expected = len(CONDITIONS)
    bad = per_question[per_question != expected]
    if not bad.empty:
        issues.append(
            f"{len(bad)} questions do not contain all {expected} expected conditions"
        )

    clean_rows = df[df["condition"] == "clean"]
    if not (clean_rows["clean_prompt"] == clean_rows["test_prompt"]).all():
        issues.append("Some clean rows differ from their canonical prompt")

    typo_rows = df[df["condition"].str.startswith("typo_", na=False)]
    if not typo_rows.empty and (typo_rows["normalized_char_distance"] == 0).any():
        issues.append("Some typo rows contain zero measured character change")

    if df["test_prompt"].isna().any():
        issues.append("Some generated prompts are null")

    return issues
