from __future__ import annotations

import argparse

import pandas as pd

from .analysis import summarise_results
from .dyslexia_generation import generate_dyslexia_file
from .experiment import run_experiment
from .generation import generate_file
from .statistics import write_mcnemar
from .validation import validate_variants


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="promptnoise")
    sub = parser.add_subparsers(dest="command", required=True)

    generate = sub.add_parser("generate", help="Generate main noisy prompt variants")
    generate.add_argument("--input", required=True)
    generate.add_argument("--output", required=True)
    generate.add_argument("--seed", type=int, default=20260927)

    dyslexia = sub.add_parser(
        "generate-dyslexia",
        help="Generate separate dyslexia-associated writing-phenomena variants",
    )
    dyslexia.add_argument("--input", required=True)
    dyslexia.add_argument("--output", required=True)
    dyslexia.add_argument("--seed", type=int, default=20260927)

    validate = sub.add_parser("validate", help="Validate generated main variants")
    validate.add_argument("--input", required=True)

    run = sub.add_parser("run", help="Run one configured model")
    run.add_argument("--input", required=True)
    run.add_argument("--models", required=True)
    run.add_argument("--model-id", required=True)
    run.add_argument("--output", required=True)
    run.add_argument("--run-number", type=int, default=1)
    run.add_argument("--limit", type=int)

    analyse = sub.add_parser("analyse", help="Aggregate result metrics")
    analyse.add_argument("--input", required=True)
    analyse.add_argument("--output", required=True)

    stats = sub.add_parser("mcnemar", help="Run paired McNemar test vs clean")
    stats.add_argument("--input", required=True)
    stats.add_argument("--condition", required=True)
    stats.add_argument("--output", required=True)

    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.command == "generate":
        frame = generate_file(args.input, args.output, args.seed)
        print(f"Generated {len(frame)} rows -> {args.output}")

    elif args.command == "generate-dyslexia":
        frame = generate_dyslexia_file(args.input, args.output, args.seed)
        print(f"Generated {len(frame)} dyslexia-associated rows -> {args.output}")

    elif args.command == "validate":
        frame = pd.read_csv(args.input)
        issues = validate_variants(frame)
        if issues:
            print("Validation issues:")
            for issue in issues:
                print(f"- {issue}")
            raise SystemExit(1)
        print(f"Validation passed: {len(frame)} rows")

    elif args.command == "run":
        frame = run_experiment(
            args.input,
            args.models,
            args.model_id,
            args.output,
            run_number=args.run_number,
            limit=args.limit,
        )
        print(f"Completed {len(frame)} new requests -> {args.output}")

    elif args.command == "analyse":
        frame = summarise_results(args.input, args.output)
        print(f"Wrote {len(frame)} summary rows -> {args.output}")

    elif args.command == "mcnemar":
        frame = write_mcnemar(args.input, args.condition, args.output)
        print(f"Wrote {len(frame)} paired test rows -> {args.output}")


if __name__ == "__main__":
    main()
