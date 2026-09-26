# Ethics, Privacy and Accessibility Rules

## Historical prompts

Do not commit raw chat-history exports.

Each candidate historical prompt must be reviewed and assigned:

- **direct-use** — self-contained and non-sensitive;
- **sanitized-use** — linguistic pattern retained but private subject matter replaced;
- **pattern-only** — original text is not stored; only abstract error transformations are retained.

Exclude prompts containing or revealing:

- names or identifying personal details;
- credentials/API keys;
- precise locations;
- medical/health details;
- financial/account information;
- workplace-confidential information;
- private messages from third parties;
- unique identifiers.

## Dyslexia

Dyslexia is an accessibility dimension, not a synonym for “bad spelling.”

Rules:

1. Do not infer that an individual typo was caused by dyslexia.
2. Use the term **dyslexia-associated writing phenomena** for categories supported by literature.
3. A single participant cannot represent the dyslexic population.
4. If participant dyslexia status is collected, it is optional, sensitive and requires explicit consent.
5. Report heterogeneity and avoid diagnostic claims.

## Singlish

Singlish is a language variety, not an error condition.

Keep Singlish analysis separate from:
- grammar errors;
- textese;
- mechanical typos.

Naturalness and semantic equivalence should be reviewed by Singaporean speakers before final inclusion.

## Human participants

Before recruitment:

- confirm the institution's requirements for student human-subject research;
- obtain informed consent;
- explain what is logged;
- use anonymous participant IDs;
- provide a withdrawal mechanism;
- collect standardized research tasks, not private messages;
- minimize sensitive demographics;
- define data-retention and deletion procedures.

## Free API tiers

Do not send sensitive human-study data to free developer APIs unless their data-use terms have been checked and the study consent covers it.

For public benchmark prompts, this is normally less concerning because the content is synthetic/non-personal.

## Publication

Release:
- clean benchmark;
- synthetic variants;
- aggregate results;
- fully de-identified approved human data, if consent permits.

Do not release:
- raw private chat exports;
- participant names/contact details;
- sensitive demographic mappings;
- secrets/keys.
