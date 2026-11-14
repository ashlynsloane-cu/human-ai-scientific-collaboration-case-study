# Phase 10 — Investigator date-scope restriction and complete provisional screening

**Status: source-linked, date-scoped SINGLE-AI eligibility first pass; NOT a frozen eligible corpus.**

At the investigator's direction on 2026-11-13, the earliest eligible conversation date is **October 1, 2025 (America/Denver local time, inclusive)**. This instruction occurred **after** the V1 protocol freeze and earlier screening. It is recorded transparently as a *post-freeze investigator scope amendment*, not retroactively represented as prespecified. Do not edit or overwrite the original screening ledgers, investigator review, or agreement results.

## Scope and current provisional screen

- Original ChatGPT export: 1,049 distinct conversations.
- Outside date scope: 452 created before October 1, 2025.
- Within date scope: 597; all now have a source-context first-pass label.
- Working labels: **206 include, 274 exclude, 117 uncertain**.
- New Phase 10 post-cutoff tranche: **147** (129 provisionally exclude, 18 uncertain, zero confirmed new include).
- No conversation in the export was created before the cutoff and continued after it.
- All 206 provisional inclusions were already in the post-cutoff population.

**Complete first-pass coverage is not validated eligibility.** Most labels have not been independently human-coded; multimodal/alternate-branch context is not fully assessed. An uncertain case must NOT be reclassified as excluded merely to simplify the denominator.

## Scope restrictions and limitations

See `docs/phase10/investigator_date_scope_addendum.md` and `docs/phase10/stopping_gates.md`. Historical Phases 5–9 remain auditable and unchanged, but pre-cutoff records are out of the primary analytical denominator. Seven of the 40 original blinded reliability cases fall outside the revised window, so the historical agreement estimate is not automatically an estimate for the new 597-case scope.

## Local reproducibility

The audit requires **private**, locally held files: `census_date_metadata_PRIVATE.csv` and `PHASE10_SCOPE_597_LEDGER_PRIVATE.csv`. They MUST NOT be committed to a public repository.

```bash
python3 -m unittest discover -s tests -p 'test_phase10_validate_scoped_eligibility.py' -v
python3 scripts/phase10_validate_scoped_eligibility.py \
  --census /path/to/private/census_date_metadata_PRIVATE.csv \
  --ledger /path/to/private/PHASE10_SCOPE_597_LEDGER_PRIVATE.csv \
  --expected results/phase10/scoped_eligibility_aggregate.json
```

The public script verifies date logic, non-overlap, original-label preservation, post-cutoff coverage, and count reconciliation. It cannot determine whether individual research conversations were classified correctly.

## Confidentiality

Only aggregate tables, generic methods, and synthetic tests are published. Do not publish conversation IDs, titles, excerpts, private rationales, original exports, research files, or blinded review keys.
