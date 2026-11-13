# Phase 2 — Hsp60/10 corpus provenance audit

This directory records a **pre-adjudication automated extraction**, not finalized human intervention coding. The 11 exported conversation JSON files (1,049 total conversations) yielded 291 first-screened candidate conversations and five additional lexical-rescue candidates. The private evidence and original exports are **not** included in the repository.

## What is included

- `results/phase2/summary.json`: aggregate screening and candidate-event counts, with explicit unverified claims.
- `results/phase2/monthly_activity.csv`: aggregate monthly counts, not a list of subjects or conversation IDs.
- `results/phase2/validation_report.json`: automated provenance checks.
- `scripts/`: reproducible extraction and validation logic; requires private input files to run.
- `docs/phase2/methodological_gates.md`: adjudication gates; unchanged frozen protocol.
- `docs/phase2/protocol_source_verification.md`: source-integrity verification against tagged V1 protocol.

The analysis scripts must be run in a restricted local workspace against the original ChatGPT export and the phase-1 screening CSV. **Do not push their input files or generated private indexes.**

The three frozen V1 markdown files were verified to be available at tag `v1.0.0-protocol-freeze` and identical by blob SHA to `main` on November 13, 2026. The baseline 31-candidate corpus exists on `main` and was not in that frozen protocol tag. Reconciliation is **ready to start, not completed**.

This package adds new paths only; no protocol, existing candidate corpus, existing README, or existing `.gitignore` is replaced.
