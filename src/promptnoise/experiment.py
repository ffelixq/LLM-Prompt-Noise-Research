from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yaml

from .cost import estimate_cost_usd
from .evaluation import score_response
from .providers import make_provider


def _load_model_config(path: str | Path, model_config_id: str) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)
    models = payload.get("models", {})
    if model_config_id not in models:
        raise KeyError(f"Model config '{model_config_id}' not found in {path}")
    config = dict(models[model_config_id])
    if not config.get("enabled", False):
        raise ValueError(
            f"Model config '{model_config_id}' is disabled. Verify the model ID and set enabled: true."
        )
    return config


def _existing_keys(output_path: Path) -> set[tuple[str, str, int, str]]:
    if not output_path.exists() or output_path.stat().st_size == 0:
        return set()
    frame = pd.read_csv(output_path)
    keys = set()
    for _, row in frame.iterrows():
        keys.add(
            (
                str(row["question_id"]),
                str(row["condition"]),
                int(row["run_number"]),
                str(row["model_config_id"]),
            )
        )
    return keys


def run_experiment(
    input_path: str | Path,
    models_path: str | Path,
    model_config_id: str,
    output_path: str | Path,
    run_number: int = 1,
    limit: int | None = None,
) -> pd.DataFrame:
    variants = pd.read_csv(input_path)
    if limit:
        variants = variants.head(limit)

    config = _load_model_config(models_path, model_config_id)
    provider = make_provider(config)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    completed = _existing_keys(output_path)
    new_rows: list[dict] = []

    for _, row in variants.iterrows():
        key = (
            str(row["question_id"]),
            str(row["condition"]),
            run_number,
            model_config_id,
        )
        if key in completed:
            continue

        started = time.perf_counter()
        error = None
        response_text = ""
        input_tokens = output_tokens = reasoning_tokens = cached_tokens = None
        raw_usage = None

        try:
            result = provider.generate(str(row["test_prompt"]))
            response_text = result.text
            input_tokens = result.input_tokens
            output_tokens = result.output_tokens
            reasoning_tokens = result.reasoning_tokens
            cached_tokens = result.cached_tokens
            raw_usage = result.raw_usage
        except Exception as exc:  # keep long runs resumable
            error = f"{type(exc).__name__}: {exc}"

        latency_ms = (time.perf_counter() - started) * 1000

        if error is None:
            correct, format_correct = score_response(
                response_text,
                str(row["expected_answer"]),
                str(row["scorer"]),
            )
        else:
            correct, format_correct = False, False

        api_cost = estimate_cost_usd(
            input_tokens,
            output_tokens,
            config.get("input_usd_per_million"),
            config.get("output_usd_per_million"),
        )

        record = {
            **row.to_dict(),
            "experiment_id": config.get("experiment_id", "pilot_v1"),
            "model_config_id": model_config_id,
            "provider": config["provider"],
            "model_id": config["model"],
            "reasoning_mode": config.get("reasoning_effort"),
            "temperature": config.get("temperature"),
            "run_number": run_number,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "reasoning_tokens": reasoning_tokens,
            "cached_tokens": cached_tokens,
            "latency_ms": latency_ms,
            "ttft_ms": None,
            "raw_response": response_text,
            "correct": int(correct),
            "format_correct": int(format_correct),
            "api_cost_usd": api_cost,
            "raw_usage_json": json.dumps(raw_usage, ensure_ascii=False) if raw_usage else None,
            "error": error,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        }
        new_rows.append(record)

        current = pd.DataFrame([record])
        write_header = not output_path.exists() or output_path.stat().st_size == 0
        current.to_csv(output_path, mode="a", header=write_header, index=False)

    return pd.DataFrame(new_rows)
