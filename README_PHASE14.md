# Phase 14 — Integrate Phase 11 human eligibility decisions

This public-safe, add-only package documents the Phase 11 blinded human review overlay onto the 597-conversation, post-AREA rule, post-fall-wet-lab exclusion Phase 13 ledger. **All private records stay local.**

- `docs/phase14_human_reconciliation_methods.md` — reconciliation algorithm, precedence, limitations
- `results/phase14_eligibility_aggregate.json` — aggregate-only working outcome
- `scripts/phase14_apply_human_review.py` — deterministic overlay validation (requires private inputs locally)
- `tests/test_phase14_apply_human_review.py` — 14 synthetic tests

No human or AI contribution claims are derived from these data. Original AI labels are immutable. The subsequent 24-case targeted packet is private, not part of the public ZIP.

Run `python3 -m unittest discover -s tests -p 'test_phase14_apply_human_review.py' -v`.
