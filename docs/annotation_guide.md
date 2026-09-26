# Prompt Annotation Guide

## Purpose

Use this guide for historical prompts, human-study prompts and manually reviewed synthetic variants.

A single prompt may have **multiple labels**. The categories are not mutually exclusive.

## Core labels

### typo
Accidental mechanical/spelling error such as insertion, deletion, substitution, transposition or spacing error.

### textese
Intentional conversational abbreviation/compression such as `u`, `idk`, `smth`, `shld`.

### grammar_noise
Non-standard or compressed grammatical structure not better explained by Singlish.

### singlish
Features attributable to Colloquial Singapore English. Do not label generic internet shorthand as Singlish simply because the writer is Singaporean.

Suggested feature tags:
- `sg_syntax`
- `sg_particle`
- `sg_lexical`
- `sg_code_mix`

### dyslexia_associated_pattern
A descriptive flag for a writing phenomenon documented in dyslexia research. It **does not imply that dyslexia caused the specific error**.

Suggested feature tags:
- `letter_order`
- `letter_insertion`
- `letter_deletion`
- `letter_substitution`
- `phonological_spelling`
- `homophone`
- `real_word_confusion`

## Semantic status

### surface_preserving
The task meaning and ground truth remain unchanged.

### recoverably_ambiguous
Likely meaning can be inferred but the text admits meaningful ambiguity.

### semantically_damaged
The variant changes or removes information required to preserve the original task.

Only `surface_preserving` variants should be used for the primary clean-vs-noisy causal comparison.

## Historical privacy classification

### direct_use
Safe, self-contained and non-sensitive.

### sanitized_use
Private nouns/context have been replaced while linguistic noise is preserved.

### pattern_only
The raw sentence is not stored. Only abstract transformations/error counts are retained.

## Review procedure

For final benchmark items:

1. first annotator labels independently;
2. second annotator reviews semantic equivalence;
3. disagreements are resolved and documented;
4. Singlish final items receive native-speaker naturalness review;
5. sensitive historical items are never escalated into a shared annotation sheet in raw form.
