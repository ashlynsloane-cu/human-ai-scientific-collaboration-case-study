# Phase 4: pre-coding reliability and corpus-completeness gate

**Status: preliminary integrity checks passed; scientific inclusion and causal attribution remain blocked.**

This is a quality-control extension to the *frozen* November 12, 2026 protocol v1.0. It changes no eligibility criterion, event definition, code category, or outcome definition. The purpose is to identify coverage biases, branch/attachment problems and source-pointer errors **before** adjudicating candidate human–AI events.

## Source scope

- All eleven conversation JSON files listed in the user's ChatGPT export manifest, not merely the 291 previously flagged threads.
- Phase 1 A/B/C screening results, Phase 2 private message pointers and candidate-event queue.
- Other human/AI interactions (e.g. Codex, research assistants, lab notebook, unrecorded meetings) are **not established** by this export; the entire-project exposure denominator is therefore not known.
- Historical research repository and manuscript snapshots will be independently tracked in an artifact provenance register. They are not substitutes for original decision records.

## Executed checks

The checked-in aggregate (`results/phase4/corpus_gate_aggregate.json`) is the output of a completed local run on the uploaded files. Local source digests and review queues are excluded from this repository. The test suite contains **synthetic** data, not private conversations.

## Run locally

Requires Python 3.10+ and only the standard library. Keep every private input and output OUTSIDE the Git repository.

```bash
python3 scripts/phase4_corpus_gate.py \
  --export-dir /path/to/private_chat_export \
  --phase1-screening /path/to/private_phase1/screening_candidates.csv \
  --phase2-private /path/to/private_phase2/PRIVATE_LOCAL_ONLY \
  --out-private /path/to/private_phase4/PRIVATE_LOCAL_ONLY \
  --out-public results/phase4
python3 -m unittest discover -s tests -p 'test_phase4_*.py' -v
```

`--seed 20261113` produces a fixed, SHA-256-ranked sample from the original screening strata: up to 25 per stratum. Non-text enrichment adds up to 20 from screened and 20 from unscreened conversations; all five previously found lexical-rescue records are included. Overlapping selections are deduplicated and retain all selection reasons.

### Output categories

- **Public/repository-safe**: aggregate counts, limitations and tests. No message bodies, source IDs, conversation titles or attachment names.
- **Private/local-only**: complete metadata QC index (all export conversations), 140 unique prioritized pilot-review records, eleven source-file SHA-256 fingerprints, and any source-pointer errors. Titles and IDs in these files must never be committed.

## Interpretation

Passing the script establishes manifest-size matching, source-node pointer resolution, branch graph traversal, and a reproducible review queue. **It does not establish project inclusion, exhaustive AI exposure, the source/accuracy of an uploaded image, E0–E5 classifications, event correctness, independent coding, artifact propagation, causal effects, or final retention.**

See `pre_coding_gates.md` and `adjudication_sop.md` before coding any scientific event.
