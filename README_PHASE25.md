# Phase 25 — Pilot-wide first-pass message screening

This package documents message-level coverage and methodological stress tests for the 15-conversation case-study pilot. It is **not a verified steering-event count** and does not modify the frozen 245-conversation eligibility corpus or the frozen V1 intervention-coding manual.

Public files: `docs/phase25_methodological_findings.md`, coverage validation script, synthetic tests, and an aggregate QA summary. The actual transcripts, message-ID ledger, user-turn triage, candidate review queue and blank second-coder sheet remain strictly private.

Run synthetic tests:
```bash
python3 -m unittest discover -s tests -p 'test_phase25_validate_pilot_coverage.py' -v
```

To validate against the private extraction locally (DO NOT commit the input files):
```bash
python3 scripts/phase25_validate_pilot_coverage.py /path/to/Hsp60_Phase25_PILOT_PRIVATE
```

**Next gate**: independent full-transcript event detection and proposal-unit segmentation, then codebook calibration. Do not publish intervention percentages or downstream-impact claims from the present screen.
