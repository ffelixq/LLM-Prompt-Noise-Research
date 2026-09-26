from __future__ import annotations

from pathlib import Path

import pandas as pd
from statsmodels.stats.contingency_tables import mcnemar


def paired_correctness(
    df: pd.DataFrame,
    condition: str,
    clean_condition: str = "clean",
) -> pd.DataFrame:
    """Return question-level paired correctness for one model and two conditions."""

    clean = df[df["condition"] == clean_condition][
        ["question_id", "model_config_id", "correct"]
    ].rename(columns={"correct": "clean_correct"})
    noisy = df[df["condition"] == condition][
        ["question_id", "model_config_id", "correct"]
    ].rename(columns={"correct": "noisy_correct"})

    return clean.merge(noisy, on=["question_id", "model_config_id"], how="inner")


def mcnemar_by_model(
    df: pd.DataFrame,
    condition: str,
    clean_condition: str = "clean",
) -> pd.DataFrame:
    paired = paired_correctness(df, condition, clean_condition)
    rows = []

    for model_id, group in paired.groupby("model_config_id"):
        both_correct = int(((group.clean_correct == 1) & (group.noisy_correct == 1)).sum())
        clean_only = int(((group.clean_correct == 1) & (group.noisy_correct == 0)).sum())
        noisy_only = int(((group.clean_correct == 0) & (group.noisy_correct == 1)).sum())
        both_wrong = int(((group.clean_correct == 0) & (group.noisy_correct == 0)).sum())

        table = [[both_correct, clean_only], [noisy_only, both_wrong]]
        test = mcnemar(table, exact=True)

        rows.append(
            {
                "model_config_id": model_id,
                "condition": condition,
                "n_pairs": len(group),
                "clean_only_correct": clean_only,
                "noisy_only_correct": noisy_only,
                "statistic": float(test.statistic),
                "p_value": float(test.pvalue),
            }
        )

    return pd.DataFrame(rows)


def write_mcnemar(
    input_path: str | Path,
    condition: str,
    output_path: str | Path,
) -> pd.DataFrame:
    df = pd.read_csv(input_path)
    result = mcnemar_by_model(df, condition)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False)
    return result
