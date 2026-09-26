from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation


def _norm(value: str) -> str:
    return " ".join(str(value).strip().split()).casefold()


def score_exact(response: str, expected: str) -> tuple[bool, bool]:
    correct = _norm(response) == _norm(expected)
    return correct, correct


def score_numeric(response: str, expected: str) -> tuple[bool, bool]:
    matches = re.findall(r"[-+]?\d+(?:\.\d+)?", response.replace(",", ""))
    if not matches:
        return False, False
    try:
        observed = Decimal(matches[0])
        target = Decimal(str(expected).replace(",", ""))
    except InvalidOperation:
        return False, False
    correct = observed == target
    format_correct = len(matches) == 1 and _norm(response).strip("%$ ") == _norm(str(expected))
    return correct, format_correct


def score_mcq(response: str, expected: str) -> tuple[bool, bool]:
    match = re.search(r"(?<![A-Za-z])([A-D])(?![A-Za-z])", response.upper())
    if not match:
        return False, False
    observed = match.group(1)
    target = expected.strip().upper()
    correct = observed == target
    format_correct = response.strip().upper() == target
    return correct, format_correct


def score_response(response: str, expected: str, scorer: str) -> tuple[bool, bool]:
    if scorer == "numeric":
        return score_numeric(response, expected)
    if scorer == "mcq":
        return score_mcq(response, expected)
    if scorer == "exact":
        return score_exact(response, expected)
    raise ValueError(f"Unknown scorer: {scorer}")
