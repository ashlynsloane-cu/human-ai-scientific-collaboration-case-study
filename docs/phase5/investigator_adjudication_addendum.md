# Phase 5 investigator adjudication addendum

Status: **provisional investigator-adjudicated eligibility**, not a corpus freeze or an independent replication. This is an append-only resolution of three previously flagged review cases under the frozen V1 inclusion criteria. No protocol definitions, source records, or original coder labels were altered.

## Resolution

One calibration case provisionally included in the original first-pass review was confirmed as eligible despite its exploratory analysis not ultimately being used. Two previously uncertain conversations were excluded following direct investigator clarification that they do not belong to the scoped Hsp60/10 research project. These decisions reflect investigator testimony, **not independent artifact corroboration**.

Among the original 140 adjudication-pilot records, the provisional state moves from **69 included / 63 excluded / 8 uncertain** to **69 included / 65 excluded / 6 uncertain**. The first-pass record and original blinded human and AI classifications remain locked in their separate private files. The six remaining uncertain cases are unresolved, and the remainder of the 1,049-conversation export has not undergone final eligibility adjudication.

## Reliability safeguard

The independent blind-40 comparison remains **38/40 exact agreement (95%), nominal Cohen κ ≈ 0.903**. Do not recompute κ after consensus resolution. The eight-case calibration set was not part of the formal reliability statistic, and investigator adjudication is not an independent third-coder assessment. All included cases still require exposure/attachment auditing and source-based event review.

## Provenance and reproduction

The original 140-case first-pass CSV, raw user-review workbook, first-pass AI labels, and all per-conversation resolutions stay outside Git. The separate private resolution overlay contains stable conversation pointers, original and final decisions, original source-record fingerprints, reviewer partition, and rationale. Use the standard-library `scripts/phase5_apply_investigator_adjudication.py` with the original private CSV and private overlay; it validates the locked labels and emits **aggregates only**.

```bash
python3 scripts/phase5_apply_investigator_adjudication.py \
  --first-pass /PRIVATE/path/pilot_eligibility_first_pass.csv \
  --adjudication /PRIVATE/path/eligibility_investigator_adjudication_overlay_PRIVATE.csv \
  --output results/phase5/investigator_adjudication_aggregate.json
python3 -m unittest discover -s tests -p 'test_phase5_investigator_adjudication.py' -v
```

Never commit the private overlay, source excerpts, full transcripts, or the uploaded human review workbooks. Review these three resolutions with their source records before external release of case-level conclusions.
