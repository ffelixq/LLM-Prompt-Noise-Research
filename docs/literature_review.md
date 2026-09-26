# Literature Review and Research Gap

This document is a working literature map, not a claim that the search is exhaustive. Re-check recent literature before the final report.

## Prompt robustness and typo perturbation

### PromptRobust
Studies adversarial prompt perturbations across character-, word-, sentence- and semantic-level changes. It established that seemingly small prompt changes can substantially alter model performance.

- Project/paper search anchor: https://arxiv.org/abs/2306.04528

### Gan et al. — adversarial typos in reasoning (EMNLP 2024)
Demonstrates that strategically selected character-level errors can strongly degrade reasoning benchmarks. This is an **adversarial** setting rather than ordinary human typing.

- https://aclanthology.org/2024.emnlp-main.584/
- https://arxiv.org/abs/2411.05345

### Chai et al. — tokenization and typographical variation (EMNLP Findings 2024)
Connects typographical variation with subword-tokenization behaviour and model robustness.

- https://aclanthology.org/2024.findings-emnlp.86/

### POSIX (EMNLP Findings 2024)
Introduces a prompt-sensitivity metric for intent-preserving prompt variants and shows that instruction/model scale alone does not eliminate prompt sensitivity.

- https://aclanthology.org/2024.findings-emnlp.852/
- https://arxiv.org/abs/2410.02185

### MulTypo (ACL 2026)
A particularly important baseline for this project. It generates keyboard-layout-aware human-like typos and evaluates many open LLMs across multiple tasks/languages. It already addresses severity and realistic synthetic typing errors.

- https://aclanthology.org/2026.acl-long.729/
- https://github.com/cisnlp/multypo

**Implication for this project:** novelty cannot be “typos hurt LLMs.” We instead compare synthetic noise with authentic LLM-user input and add efficiency/cost measurements.

## Grammar, imperfect English and informal input

### Imperfect English / MT prompting (EACL Findings 2026)
Studies realistic spelling and grammatical imperfections in translation-related prompts. Reported findings suggest spelling noise can be more damaging than some phrase-level grammatical variation.

- https://aclanthology.org/2026.findings-eacl.38/

### Abbreviation reconstruction (NAACL 2022)
Shows that large language models can infer heavily abbreviated expressions, particularly with context.

- https://aclanthology.org/2022.naacl-main.91/

**Gap used here:** abbreviation reconstruction is not the same as asking whether textese changes correctness, reasoning expenditure, tokens and cost on downstream tasks.

## Human typing research

### How We Type
HCI work using keypress, gaze and hand-movement data to study real typing behaviour.

- https://userinterfaces.aalto.fi/how-we-type/

### How We Type — Mobile
Studies mobile typing, visual attention, finger guidance and error correction.

- https://userinterfaces.aalto.fi/how-we-type-mobile/

**Gap used here:** these studies characterize humans; this project studies the downstream impact of naturally produced typing noise on LLM inference.

## Singlish

### Singlish message paraphrasing / normalization (COLING 2022)
Develops Singlish-to-Standard-English normalization resources and studies lexical/syntactic/semantic normalization.

- https://aclanthology.org/2022.coling-1.345/

### Colloquial Singaporean English style transfer (ACL 2025)
Provides large-scale Singlish style-transfer data with fine-grained linguistic dimensions including syntax, lexical borrowing, pragmatics and code-switching.

- https://aclanthology.org/2025.acl-long.1309/

### Singlish discourse particles (PACLIC 2025)
Evaluates model understanding of discourse particles and highlights that local pragmatic meaning remains difficult.

- https://aclanthology.org/2025.paclic-1.2/

### Singlish resources / translation (LREC 2026)
Adds newer Singlish resources and translation/normalization work.

- https://aclanthology.org/2026.lrec-1.280/

**Gap used here:** prior work largely asks whether models can translate/generate/understand Singlish. This project asks whether **semantically equivalent Singlish task prompts** alter downstream accuracy and inference efficiency.

## Dyslexia and NLP/LLMs

### Price & Wu — dyslexic-style text and commercial MT (ACL Findings 2025)
A close predecessor to the accessibility component. It evaluates commercial NLP systems on synthetic dyslexia-associated error types and authentic writing.

- https://aclanthology.org/2025.findings-acl.708/

The study motivates separating obvious nonword errors from homophone/real-word confusion and also warns that synthetic dyslexic-style noise cannot represent the full heterogeneity of dyslexic writing.

### DysList corpus
An annotated corpus resource for studying dyslexic writing.

- https://aclanthology.org/L14-1492/

**Gap used here:** prior work is strongly translation/NLP-focused. This project studies general task prompting plus token, reasoning, latency and cost behaviour.

## Project-level research gap

The proposed contribution is a **unified real-world prompt-noise benchmark** connecting:

1. controlled synthetic keyboard noise;
2. grammar/textese;
3. Singlish language variation;
4. dyslexia-associated writing phenomena;
5. sanitized historical prompts written to an LLM;
6. controlled human typing data;
7. modern reasoning/non-reasoning LLMs;
8. correctness **and** inference efficiency;
9. normalization cost-benefit analysis.

The strongest comparisons are expected to be:

- synthetic vs authentic human noise;
- obvious nonword vs valid-word contextual errors;
- Standard English vs matched Singlish;
- clean vs textese;
- ordinary keyboard noise vs dyslexia-associated conditions at comparable edit severity;
- direct noisy inference vs correction/normalization pipelines.

## Literature review table schema for expansion

The final literature CSV should include:

```text
paper
year
venue
research_question
models
dataset
noise_type
metrics
main_result
limitations
relationship_to_our_project
url
```
