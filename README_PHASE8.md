# Phase 8 — Expanded conversation eligibility screening (provisional)

This add-only research-methods package documents the next source-text eligibility tranche for the full Hsp60/10 human–AI collaboration case study. **No intervention outcomes, attribution percentages, or final corpus declarations are made here.** The V1 protocol and earlier investigator decisions remain unchanged.

## Source coverage (AI triage only)

- Original export: **1,049** conversations, **11** locked JSON source shards.
- Previously screened for eligibility: **200** (Phase 5 pilot 140, Phase 7 tranche 60).
- Newly screened in Phase 8: **241** distinct source conversations, comprising 164 of the originally flagged remainder and 77 of the already-selected Phase 6 probability sample. Three additional probability-sample cases were previously screened in Phase 7 and their original labels were not changed.
- Total with at least one provisional source-context classification: **441**.
- Remaining without a source-context classification: **608**.
- Every one of the initial **291 keyword-screened candidates** has now received provisional source-context triage, but not full human adjudication.

The 441 working labels (including the Phase 5 investigator addendum) are **206 include, 163 exclude, 72 uncertain**. These counts are subject to human review, full-context/source gaps, and further corpus-retrieval work.

## Included files

- `docs/phase8/methods_and_limits.md` — design, eligibility interpretation, sampling, human-review safeguard and scientific stopping rules.
- `results/phase8/phase8_eligibility_aggregate.json` — aggregate-only classifications and source-coverage status.
- `scripts/phase8_validate_eligibility.py` — standard-library source-hash, node, de-duplication, original-ledger preservation and public-aggregate verification. Requires private files stored outside the repository.
- `tests/test_phase8_validate_eligibility.py` — synthetic QA tests, no original conversations.
- `results/phase8/test_execution.json` — local verification status and limitations.
- `MANIFEST_PHASE8.sha256` — SHA-256 of the additive public-safe files.

The private counterpart contains the 241 records with identifiers and source fingerprints, 3 preserved overlap checks, the original 80-case probability-sample blind worksheet, a 40-case new stratified blind validation allocation, and 45 new uncertain cases needing adjudication. **Never commit any private records or the ChatGPT export.**

## Reproduce the source checks

Run unit tests in the study repository root:

```bash
python3 -m unittest discover -s tests -p 'test_phase8_validate_eligibility.py' -v
```

Run the validator using the local private source files. Get argument names with:

```bash
python3 scripts/phase8_validate_eligibility.py --help
```

A validator pass certifies identity, sample continuity, and a reproducible aggregate. **It does not certify that the AI made correct scientific eligibility judgments.** Independent human review is mandatory before freezing the corpus.
