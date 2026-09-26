# Research Protocol v1.0

## Working title

**Real-World Prompt Noise: How Human Typing Errors, Textese, Singlish and Dyslexia-Associated Writing Patterns Affect LLM Accuracy and Computational Efficiency**

## Core question

How do realistic human prompt variations affect the accuracy and computational efficiency of modern large language models?

## Research questions

- **RQ1:** How does increasing keyboard typo severity affect task accuracy?
- **RQ2:** Do spelling, grammar variation, textese and mixed noise affect models differently?
- **RQ3:** Do noisy prompts change input-token consumption?
- **RQ4:** Do noisy prompts change output/reasoning-token consumption?
- **RQ5:** Are some model families/sizes more robust than others?
- **RQ6:** Do synthetic typo generators accurately represent actual human errors?
- **RQ7:** Do phone/laptop, careful/rapid, proofreading and autocorrect conditions change downstream outcomes?
- **RQ8:** Is prompt normalization worth its additional cost/latency?
- **RQ9:** How does natural Singlish compare with semantically equivalent Standard English?
- **RQ10:** Which Singlish features contribute to observed differences?
- **RQ11:** How do dyslexia-associated writing phenomena compare with ordinary keyboard errors at similar severity?
- **RQ12:** Do authentic and synthetic dyslexia-associated inputs produce different outcomes?
- **RQ13:** Which dyslexia-associated error categories are most disruptive?

## Preregistered hypotheses for the pilot

- **H1:** Increasing typo severity will reduce accuracy.
- **H2:** Mechanical spelling errors will generally be more disruptive than mild grammatical variation when intent remains clear.
- **H3:** Misspelled prompts will tend to increase input-token counts.
- **H4:** Some noisy prompts will increase reasoning/output expenditure even when answers remain correct.
- **H5:** Reasoning-heavy tasks will be more sensitive than simple extraction/classification tasks.
- **H6:** Robustness will differ by model family and size; scale alone will not guarantee robustness.
- **H7:** Synthetic noise will not perfectly reproduce real human noise.
- **H8:** Normalization will be more useful for severe than mild noise.
- **H9:** Singlish may change performance/efficiency relative to matched Standard English.
- **H10:** Singlish feature types may differ in difficulty.
- **H11:** Real-word/contextual errors may be more disruptive than obvious nonword errors.

Do not rewrite these hypotheses after looking at final benchmark results. Any post-hoc ideas must be explicitly marked exploratory.

## Prompt taxonomy

### A. Mechanical / keyboard noise

- adjacent-key substitution
- character omission
- character insertion
- repeated key
- transposition
- missing space
- merged words
- rapid/no-proofreading typing

### B. Grammatical variation

- article omission
- preposition omission
- tense changes
- subject/verb mismatch
- grammar compression

### C. Textese

Examples include `u`, `rn`, `idk`, `smth`, `shld`, `cld`, `pls`, `bc`.

Textese is intentional compression, not a typo.

### D. Singlish

Treat Singlish as a language variety, not an error condition.

Subfeatures:
- syntax
- pragmatic particles
- lexical items
- code-switching

### E. Dyslexia-associated writing phenomena

Treat these as literature-informed writing phenomena, not diagnostic markers.

- letter insertion/deletion/substitution
- sequential/letter-order errors
- phonological spellings
- homophone substitutions
- real-word confusion

### F. Mixed real-world input

Natural combinations of multiple categories.

## Pilot benchmark

The included pilot contains 50 authored questions:

- 10 factual/MCQ
- 10 mathematics
- 10 logical reasoning
- 10 coding
- 10 extraction/instruction-following

The pilot is for **method validation**, not final publication-level conclusions.

## Controlled conditions

Main pilot conditions:

- clean
- typo_02
- typo_05
- typo_10
- typo_20
- grammar
- textese
- singlish_pilot
- mixed_realistic

The dyslexia-associated perturbation experiment is kept separate to avoid exploding the factorial design.

## Meaning-preservation rule

The primary benchmark studies different surface forms of the **same intended task**.

Do not corrupt:
- essential numbers;
- operators;
- answer choices;
- identifiers required for code correctness;
- ground-truth-bearing named entities.

Each generated prompt should be classifiable as:

1. **surface-preserving**
2. **recoverably ambiguous**
3. **semantically damaged**

Only surface-preserving variants belong in the primary causal comparison.

## Model comparison rule

Primary robustness claims use **within-model clean-to-noisy change**, not raw accuracy ranking.

For model (m):

```text
robustness_ratio = accuracy_noisy(m) / accuracy_clean(m)
```

This separates baseline capability from robustness.

## Repetitions

Do not triple the entire experiment.

- run the complete final benchmark once;
- preregister a reproducibility subset;
- run that subset two additional times.

## Inference controls

For every request:

- fresh context;
- no web;
- no tools;
- no retrieval;
- fixed model ID;
- fixed documented parameters;
- short output format where possible;
- log exact provider metadata.

Do not force identical temperature/reasoning parameters onto models that do not support the same semantics. Keep settings fixed **within each model**.

## Primary metrics

- accuracy
- format compliance
- accuracy drop
- robustness ratio
- input-token overhead
- output-token overhead
- reasoning-token overhead where exposed
- end-to-end latency
- time-to-first-token where available
- estimated API cost
- cost per correct response

## Statistical plan

### Binary correctness
Use paired comparisons; McNemar's test is suitable for clean/noisy pairs.

### Multi-factor analysis
Use logistic regression or mixed-effects logistic models:

```text
logit(P(correct)) ~ noise + model + task + noise:model
```

### Human study
Include participant-level repeated/random effects where possible.

### Continuous metrics
Report paired differences, medians, effect sizes and bootstrap confidence intervals.

### Correlations
Use Spearman correlation for noise severity against token/accuracy metrics where monotonic rather than linear relationships are expected.

### Multiple comparisons
Use Holm correction for families of pairwise tests.

## Pilot stop/go criteria

Before scaling to 250 questions, confirm:

1. generated prompts preserve intended meaning at acceptable rates;
2. scorers correctly mark at least a manually audited sample;
3. provider usage metadata is captured correctly;
4. no sensitive historical data is leaking into outputs;
5. clean benchmark is neither at extreme floor nor ceiling for all candidate models;
6. perturbation severity produces measurably different edit distances.

If any criterion fails, fix methodology before scaling.
