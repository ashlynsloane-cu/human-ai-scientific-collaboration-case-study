# Phase 6: Corpus completeness and probability-audit setup

**Status:** Discovery / review preparation, not final eligibility classification.

This expansion deliberately preserves the original 2026-11-12 frozen V1 protocol and the original independent eligibility-review labels. The Phase 5 first-pass corpus contained 140 reviewed conversations, 69 provisional inclusions, 65 post-adjudication exclusions, and six still unresolved. Phase 6 examines the 909 remaining conversations rather than inferring exclusion from absence of Hsp60/10 keywords.

## Design

1. Verify every `conversations-###.json` file against the original export manifest byte count **and frozen Phase 4 SHA-256 file digests**, and verify the investigator overlay targets the unchanged first-pass CSV fingerprint; reconcile all conversation IDs against the Phase 4 1,049-record index.
2. Reproduce the Phase 5 investigator overlay as distinct, non-destructive classifications. Never overwrite the original 140-case ledger.
3. Construct a deterministic token-based TF-IDF retrieval index on current-branch conversation title, user text, and assistant text. Use reviewed provisional inclusions as **retrieval exemplars only**. Reviewed exclusions provide a weak negative-control similarity penalty. The score is not an eligibility probability or an independently validated classifier.
4. Prepare private review queues for the 200 originally flagged conversations not in the Phase 5 pilot and the 709 previously unscreened, not yet reviewed conversations.
5. Define a new **prospective, probability-based review sample** *within these 709 previously unscreened, unreviewed conversations*: divide this finite population into four post-pilot similarity quartiles, then use a fixed SHA-256 sampling seed to select 20 records from each quartile (80 total). Original screening and prior pilot review are not used as eligibility outcomes for this sample. Sampling can produce an unbiased estimate of the reviewer-defined inclusion rate **in this specific 709-case finite population**, conditioned on full and adequate manual review and with weights accounting for quartile size. Because retrieval model setup followed the Phase 5 pilot, it is **not** an independent evaluation of model recall across the original archive.
6. Keep all cases' final labels blank until full-context, asset-aware human/AI adjudication. Do not treat excerpt-only judgments as final when images or files could be decisive.

## Reproduction

```
python3 scripts/phase6_corpus_recall_audit.py \
  --export-dir /secure/export \
  --phase4-index /secure/phase4/all_conversations_qc_index.csv \
  --phase4-digests /secure/phase4/source_file_digests.csv \
  --pilot-ledger /secure/phase5/pilot_eligibility_first_pass.csv \
  --adjudication-overlay /secure/phase5/eligibility_investigator_adjudication_overlay_PRIVATE.csv \
  --out-private /secure/phase6_review \
  --out-public results/phase6
python3 -m unittest discover -s tests -p 'test_phase6_corpus_recall_audit.py' -v
```

The private queues include original conversation identifiers, titles, and source-text snippets. They must **never** be committed, disclosed publicly, or shared for independent review without privacy/consent clearance. Only `results/phase6/corpus_completeness_design.json`, this method note, the script and synthetic tests are repository-safe.

## Scientific gates still closed

- This is *not* a classification of 909 conversations and does not establish exhaustive recall.
- The 80-case audit has been sampled but **not yet coded**. Estimate prevalence/uncertainty only after coding; missing images/attachments must be flagged, not imputed irrelevant.
- Six original ambiguous cases remain unresolved.
- The original reconstructed 31-candidate list must be reconciled with actual export conversation IDs.
- The entire eligible corpus requires appropriate human or independent-coder review.
- No human–AI steering frequency, intellectual-origin percentage, figure provenance, intervention effect, or E5 absence claim is authorized by these outputs.
