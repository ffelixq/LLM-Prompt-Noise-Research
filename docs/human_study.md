# Human Typing Study Protocol

## Goal

Measure the noise humans naturally produce when formulating LLM requests and compare its distribution and downstream model effects with synthetic perturbation methods.

## Recommended initial sample

10–20 participants for a student-scale pilot.

The study is exploratory unless a power analysis and larger recruitment plan are completed.

## Task design

Participants receive an **intent**, not text to copy.

Example:

> Ask an AI to calculate the final price of a $120 item after a 15% discount.

This allows natural sentence structure, textese, Singlish and typing behaviour to emerge.

## Core within-participant conditions

1. laptop — careful
2. laptop — rapid/no corrections
3. phone — careful
4. phone — rapid/no corrections

Optional subconditions:
- hidden entered text until submission;
- autocorrect OFF;
- autocorrect ON.

Do not add every optional condition to the first participant pilot.

## Suggested instrumentation

Log only research-relevant metadata:

- anonymous participant ID;
- task ID;
- device class;
- condition;
- autocorrect state;
- final submitted prompt;
- start/end timestamps;
- backspace count;
- edit count where technically feasible.

Do not record unrelated keystrokes outside the study interface.

## Singlish

Do not instruct all participants to “make it Singlish” in the natural typing condition. Let natural variation emerge.

A separate controlled Singlish task set can be validated by Singaporean annotators.

## Dyslexia

If dyslexia status is studied:

- collection must be optional and consented;
- distinguish diagnosed / self-identified only if ethics approval and sample size justify it;
- provide “prefer not to say”;
- never infer dyslexia from spelling alone.

## Analysis

Compare:

- error-type frequencies;
- normalized edit distance from an investigator-created clean semantic rendering;
- textese frequency;
- Singlish-feature frequency;
- tokenization overhead;
- downstream model correctness;
- cost/latency.

Participant-level repeated measures should be handled with mixed-effects or repeated-measures methods rather than treating every prompt as independent.
