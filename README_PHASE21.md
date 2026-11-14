# Phase 21 — Closure audit findings

This package is a **freeze-readiness check, not a declaration of corpus freeze**. The original V1 protocol remains unchanged.

- The effective in-scope conversation ledger remains **597 = 245 INCLUDE + 352 EXCLUDE** (0 unresolved working labels).
- All 11 export shards match locked Phase 4 byte sizes and SHA-256 hashes; 597 conversation IDs occur exactly once in the working ledger and source export.
- Phase 2 explicitly says the 31-record v0.2 file was not supplied; this cannot be proven to reconcile record-by-record. It is a **legacy-documentation gap**, not evidence of 31 additional conversations.
- Current-branch export review misses alternate user-message branches in 19 conversations (11 excluded). Two of the excluded threads have topic-keyword-bearing alternate user messages; project linkage still requires source-based contextual review.
- Of the 352 excluded conversations, 57 carry `True` in the nontext flag and 302 have any status other than explicit `False`. These heterogeneous status labels must not be interpreted as a precise count of missing attachment payloads.
- The asset filename map does not supply attachment bytes; exhaustive multimodal eligibility cannot be verified from text alone.
- The Phase 19 random negative audit is an uncertainty estimate, not an exhaustive proof of exclusion validity.

## Recommended stopping rule
Do not freeze an *account-wide exhaustive multimodal dataset*. A **qualified exported-ChatGPT-conversation corpus** may be frozen when the investigator signs the scope addendum, explicitly documents the unavailable 31-row historical record and unavailable assets/branches, inspects the two identified excluded alternate-branch cases, and declares that residual limits are methodological limitations rather than silently asserting exhaustive capture. A more stringent multimodal freeze remains blocked without the missing payloads.

No private titles, IDs, source snippets, or human rationales belong in the public repo.
