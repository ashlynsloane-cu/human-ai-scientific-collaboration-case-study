# Phase 9 — Conservative expansion of conversation eligibility screening

This **add-only** package extends the Phase 8 source-context eligibility audit from 441 to 641 **distinct, provisionally assessed** conversations from the 1,049-conversation ChatGPT export. Its 200 new source-excerpt reviews use 120 context-ranked cases and 80 SHA-256-selected cases from the remaining lower-ranked pool. The Phase 8 corpus decisions, investigator overlays, and frozen V1 protocol are unchanged.

This is **not** an independently adjudicated eligibility corpus. The new 200 labels were assigned by the same AI reviewer using selected source-message excerpts, not a full multimodal or all-branches read. No human second review was performed for these 200. No new AI-contribution or human-intervention inference is authorized.

## Public files

- `results/phase9/eligibility_progress_aggregate.json` — public-safe counts and limitations, never case-level records
- `scripts/phase9_validate_coverage.py` — deterministic selection, source-fingerprint checks, aggregate reproduction, and disclosure allowlist
- `tests/test_phase9_validate_coverage.py` — 14 tests using synthetic records only
- `docs/phase9/eligibility_methods.md` — sampling and inclusion methodology
- `docs/phase9/validation_and_stopping_gates.md` — what must happen before corpus freeze
- `MANIFEST_PHASE9.sha256` — SHA-256 of this package's files, excluding the manifest

## How to check

```bash
shasum -a 256 -c MANIFEST_PHASE9.sha256
python3 -m unittest discover -s tests -p 'test_phase9_validate_coverage.py' -v
```

## Full source-level verification (local/private only)

The public bundle is sufficient to reproduce software checks with synthetic fixtures, but source-level replay requires the private Phase 9 ledger, the private 608-conversation digest, all 11 original ChatGPT export JSON shards, and frozen source hashes. For example:

```bash
python3 scripts/phase9_validate_coverage.py \
  --private-ledger /secure/private/phase9_200_provisional_private.csv \
  --remaining-index /secure/private/remaining_608_digest_PRIVATE.csv \
  --prior-aggregate results/phase8/phase8_eligibility_aggregate.json \
  --source-dir /secure/chatgpt-export \
  --source-digests /secure/private/source_file_digests.csv \
  --public-output /tmp/phase9_eligibility_progress_recomputed.json
cmp /tmp/phase9_eligibility_progress_recomputed.json results/phase9/eligibility_progress_aggregate.json
```

The actual source-message excerpts, titles, conversation IDs, reviewer rationales, and full export **must not** enter the public repository, including as temporary, subsequently deleted commits. None are included here.
