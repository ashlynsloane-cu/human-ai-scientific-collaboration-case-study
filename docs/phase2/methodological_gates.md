# Phase-2 review gates — human–AI Hsp60/10 study

These are operational checks and **not changes to the frozen V1.0 protocol**.

| Gate | State as of 2026-11-13 | Boundary / required evidence |
|---|---|---|
| Export integrity | PASS | All 11 JSONs parsed and matched manifest sizes; file-level SHA-256 retained privately |
| Frozen V1 source integrity | PASS | Three documents exist at `v1.0.0-protocol-freeze`, blob-identical to `main` |
| Baseline corpus availability | PASS | 31-candidate v0.2 CSV and summary accessible on `main` |
| Baseline-to-export reconciliation | READY, NOT STARTED | Link 31 reconstructed labels to actual conversation IDs; document ambiguous matches |
| Branch-aware message extraction | PASS for 291 screened conversations | Distinguish mainline from alternate branches; do not double-count |
| Conversation inclusion | PENDING | Manual review of 149 priority, 142 other screened, and five lexical rescues |
| Exposure E0–E5 | PENDING | Audit message and attachment evidence, especially any possible E5 |
| Human steering events | PENDING | Confirm preceding AI proposal + user response; avoid treating linguistic cues as interventions |
| L0–L4 / D0–D4 coding | PENDING | Independent coders, reliability and adjudication per frozen manual |
| Artifact propagation/persistence | PENDING | Code and manuscript diffs, figure history, manuscript versions, release evidence |
| Statistical conclusions | NOT STARTED | Adjudicated sample + documented uncertainty and sensitivity analyses |

**Interpretation:** 2,028 machine-detected cues are *not* 2,028 coded human interventions. No impact, causal, acceptance, or persistence claims are yet supported.
