# Data Dictionary

## Benchmark source columns

| Column | Type | Description |
|---|---|---|
| question_id | string | Stable question identifier |
| task_type | category | factual, math, reasoning, coding, extraction |
| prompt | string | Clean canonical prompt |
| expected_answer | string | Ground truth or canonical output |
| scorer | category | exact, numeric, mcq, json_fields, code |
| protected_tokens | string | Pipe-separated tokens that perturbation must not modify |
| output_instruction | string | Expected response-format instruction |

## Generated variant columns

| Column | Description |
|---|---|
| question_id | Source question |
| condition | clean, typo_02, typo_05, typo_10, typo_20, grammar, textese, singlish_pilot, mixed_realistic |
| clean_prompt | Original canonical prompt |
| test_prompt | Perturbed prompt |
| seed | Generation seed |
| char_distance | Raw Levenshtein distance |
| normalized_char_distance | Distance / max string length |
| word_distance | Token-level edit distance |
| semantic_status | surface_preserving, recoverably_ambiguous, semantically_damaged |
| perturbation_metadata | JSON describing edits |

## Experiment result columns

| Column | Description |
|---|---|
| experiment_id | Run identifier |
| question_id | Question identifier |
| condition | Prompt condition |
| task_type | Task category |
| model_config_id | Configuration key |
| provider | Provider/deployment |
| model_id | Exact API model ID |
| reasoning_mode | Provider-exposed reasoning setting if any |
| temperature | Request temperature if applicable |
| seed | Request seed if applicable |
| run_number | Repetition |
| input_tokens | Provider-reported input tokens |
| output_tokens | Provider-reported visible output tokens |
| reasoning_tokens | Provider-reported reasoning tokens, otherwise null |
| cached_tokens | Provider-reported cache tokens, otherwise null |
| latency_ms | End-to-end request latency |
| ttft_ms | Time to first token if measured |
| raw_response | Model response |
| expected_answer | Ground truth |
| correct | 1/0 |
| format_correct | 1/0 |
| api_cost_usd | Cost calculated from frozen pricing table |
| error | API/runtime error if any |
| timestamp_utc | Collection timestamp |

## Historical corpus columns

Historical prompts require privacy review before inclusion.

| Column | Description |
|---|---|
| historical_id | Anonymous ID |
| noisy_prompt | Only if approved safe/sanitized |
| clean_prompt | Meaning-preserving clean reconstruction |
| usage_class | direct_use, sanitized_use, pattern_only |
| context_dependent | Whether omitted chat context is needed |
| typo | Boolean |
| textese | Boolean |
| grammar_noise | Boolean |
| singlish | Boolean |
| dyslexia_associated_pattern | Boolean; descriptive, not diagnostic |
| insertion_count | Character insertions |
| deletion_count | Character deletions |
| substitution_count | Character substitutions |
| transposition_count | Adjacent-order changes |
| missing_space_count | Missing whitespace |
| merged_word_count | Merged tokens |
| real_word_error_count | Wrong but valid lexical items |
| homophone_error_count | Homophone substitutions |
| semantic_equivalent | Human-reviewed equivalence flag |

## Human typing study columns

| Column | Description |
|---|---|
| anonymous_participant_id | Non-identifying participant code |
| task_id | Standardized intent task |
| device | laptop / phone |
| typing_condition | careful / rapid / hidden_text |
| autocorrect_status | on / off / unknown |
| final_prompt | Submitted prompt |
| typing_duration_ms | Time from start to submit |
| backspace_count | Correction behavior |
| edit_count | Total edits if instrumented |
| self_reported_dyslexia | Optional sensitive field with explicit consent only |

Never put names, account identifiers, health records, financial details, passwords, API keys or workplace-sensitive material into committed datasets.
