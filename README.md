# LLM Prompt Noise Research

A reproducible benchmark for studying how **real-world prompt variation** affects LLM correctness and computational efficiency.

The project separates several phenomena that are often collapsed into “bad English”:

- mechanical keyboard noise (adjacent-key substitutions, omissions, transpositions, spacing errors);
- grammatical variation and compression;
- textese / messaging abbreviations;
- Singlish as a **language variety**, not an error;
- dyslexia-associated writing phenomena as an **accessibility/robustness** condition, not a diagnostic label;
- mixed real-world input;
- authentic historical prompts and controlled human typing data.

## Primary outcomes

For each clean/noisy prompt pair and model, the benchmark can record:

- correctness and format compliance;
- input/output/reasoning tokens where exposed;
- end-to-end latency and time-to-first-token where exposed;
- API cost;
- robustness ratio;
- token overhead;
- cost per correct response.

## Research design

The project has three realism levels:

1. **Controlled synthetic noise** — causal, reproducible perturbations.
2. **Historical natural input** — sanitized real prompts paired with clean semantic equivalents.
3. **Human typing study** — standardized tasks typed under controlled device/typing conditions.

See [docs/research_protocol.md](docs/research_protocol.md) for the full methodology and [docs/literature_review.md](docs/literature_review.md) for the research context.

## Quick start

Python 3.11+ is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,providers,dashboard]"
cp .env.example .env
```

Generate prompt variants from the included 50-question pilot:

```bash
python -m promptnoise.cli generate \
  --input data/benchmark/pilot_50.csv \
  --output data/generated/pilot_variants.csv \
  --seed 20260927
```

Validate the generated dataset without making API calls:

```bash
python -m promptnoise.cli validate --input data/generated/pilot_variants.csv
```

Run a configured model after adding the relevant API key:

```bash
python -m promptnoise.cli run \
  --input data/generated/pilot_variants.csv \
  --models config/models.example.yaml \
  --model-id YOUR_CONFIG_ID \
  --output results/raw/pilot_results.csv
```

Analyse collected results:

```bash
python -m promptnoise.cli analyse \
  --input results/raw/pilot_results.csv \
  --output results/tables/pilot_summary.csv
```

Launch the dashboard:

```bash
streamlit run dashboard/app.py
```

## Pilot before scale

Do **not** immediately run the full planned experiment. The intended order is:

1. validate the 50-question pilot;
2. test one cheap/free model;
3. check scorers, token metadata and meaning preservation;
4. freeze the methodology;
5. build the 250-question final benchmark;
6. run the multi-model study;
7. then add historical/human studies and correction experiments.

## Privacy

Do not commit raw private chat exports, API keys, health/financial/workplace-sensitive prompts, or identifying participant data.

Historical examples must be classified as **direct-use**, **sanitized-use**, or **pattern-only** before entering the research corpus.

## Status

This repository contains the **research protocol + executable pilot framework**. The final 250-question benchmark and participant data should only be frozen after the pilot methodology has been validated.
