from __future__ import annotations

from pathlib import Path

import pandas as pd


def summarise_results(input_path: str | Path, output_path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(input_path)
    successful = df[df["error"].isna()] if "error" in df.columns else df.copy()

    metrics = {
        "correct": "mean",
        "format_correct": "mean",
        "question_id": "count",
        "input_tokens": "mean",
        "output_tokens": "mean",
        "reasoning_tokens": "mean",
        "latency_ms": "mean",
        "api_cost_usd": "sum",
    }
    metrics = {k: v for k, v in metrics.items() if k in successful.columns}

    summary = (
        successful.groupby(["model_config_id", "condition", "task_type"], dropna=False)
        .agg(metrics)
        .reset_index()
        .rename(
            columns={
                "correct": "accuracy",
                "format_correct": "format_accuracy",
                "question_id": "n",
                "input_tokens": "avg_input_tokens",
                "output_tokens": "avg_output_tokens",
                "reasoning_tokens": "avg_reasoning_tokens",
                "latency_ms": "avg_latency_ms",
                "api_cost_usd": "total_cost_usd",
            }
        )
    )

    clean = summary[summary["condition"] == "clean"][
        ["model_config_id", "task_type", "accuracy"]
    ].rename(columns={"accuracy": "clean_accuracy"})

    summary = summary.merge(clean, on=["model_config_id", "task_type"], how="left")
    summary["accuracy_drop"] = summary["clean_accuracy"] - summary["accuracy"]
    summary["robustness_ratio"] = summary["accuracy"] / summary["clean_accuracy"].replace(0, pd.NA)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_path, index=False)
    return summary
