# Final Benchmark Freeze Checklist

Do not run the expensive/full multi-model collection until all items below are satisfied.

- [ ] 50-question pilot generated deterministically.
- [ ] CI tests pass.
- [ ] Pilot clean accuracy checked on at least one target model.
- [ ] No universal ceiling/floor effect.
- [ ] Automatic scorers manually audited.
- [ ] Typo severity produces ordered edit-distance distributions.
- [ ] Protected numbers/operators survive perturbation.
- [ ] All primary variants marked surface-preserving after review.
- [ ] Textese rules reviewed for accidental semantic changes.
- [ ] Final Singlish prompts reviewed for naturalness and equivalence.
- [ ] Dyslexia-associated conditions described non-diagnostically.
- [ ] Historical corpus privacy review completed.
- [ ] Human-study ethics/consent requirements confirmed before recruitment.
- [ ] Exact final model IDs frozen.
- [ ] Provider inference settings frozen.
- [ ] Pricing snapshot frozen.
- [ ] Final 250-question benchmark checksum recorded.
- [ ] Reproducibility subset selected before final results are inspected.
- [ ] Analysis script/version frozen.

After freezing, changes require a new benchmark version and must not silently replace the original final dataset.
