# Hsp60/10 case study — Phase 5 investigator adjudication addendum

**Status:** Provisional corpus-eligibility adjudication, NOT a corpus freeze.

This add-only package records three investigator clarifications without changing the frozen protocol or replacing initial reviewer decisions. It publishes aggregate numbers only. Source identities, private rationales, and the 140-case source ledger must remain local.

- `docs/phase5/investigator_adjudication_addendum.md` — procedure, limitations and evidence tiers
- `results/phase5/investigator_adjudication_aggregate.json` — aggregate 140-case provisional status
- `scripts/phase5_apply_investigator_adjudication.py` — deterministic private-overlay validation and aggregation
- `tests/test_phase5_investigator_adjudication.py` — six synthetic tests

## Local verification

```bash
python3 -m unittest discover -s tests -p 'test_phase5_investigator_adjudication.py' -v
```

To reproduce the numeric aggregate, run the script on the **private** first-pass source ledger and three-case private resolution overlay (see the addendum). The private inputs are intentionally excluded from the repository.

**Do not recompute original blinded inter-rater agreement following adjudication.** It remains 38/40 exact agreement (95%) and nominal Cohen's kappa about 0.903, before case resolution.
