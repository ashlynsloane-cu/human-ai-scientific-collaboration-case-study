# Phase 4: scientific and reproducibility gates

Methodological commitments are anchored to `v1.0.0-protocol-freeze` (protocol, coding manual, data governance). This document is an **operational QC plan**, not a protocol amendment.

| Gate | Required evidence | Current state | Prohibited shortcut |
|---|---|---|---|
| G0. Frozen source integrity | Tag resolves and V1 documents unchanged | VERIFIED independently through GitHub | Edit frozen V1 files |
| G1. Export integrity | Manifest-listed 11 JSONs, all sizes match; IDs resolve | PASSED; cryptographic SHA-256 held privately | Conflate matched byte sizes with proof of completeness of all research interactions |
| G2. Corpus recall | Manual yes/no/uncertain adjudication; examine 758 previously unscreened and multimodal cases via transparent sampling and follow-up | OPEN | Treat 291 lexical hits or 5 rescues as a final corpus |
| G3. Message semantics | Verify screen captures, PDFs, attachments and alternate branches before E0–E5 exposure coding | OPEN | Infer E0 or E5 from filenames or regex hits |
| G4. Event identification | Review full preceding AI proposal and human reply, contiguous turns, reused text, event boundaries | OPEN | Treat 2,028 lexical cues as steering events |
| G5. Independent reproducibility | At least two coders, blinded as practical, assess preregistered subset; kappa/weighted kappa/agreement, disagreements adjudicated | OPEN | Claim reliability from passing parser unit tests |
| G6. Artifact linkage | Check implementation against versioned R/Python sources, commits, figures, outputs, scientific documents and dated experiment records | OPEN | Attribute authorship from Git user name or text similarity alone |
| G7. Scientific synthesis | Compute outcomes only after G2–G6; separate descriptive association from causal claim | OPEN | Declare AI impact or counterfactual history from an anecdote |

## Observed limitations requiring action

- The ChatGPT archive includes multimodal messages with non-text parts; the current extractor does not visually interpret them. Files referenced by the account export were *not* all uploaded here. Zero reported E5 incidents cannot be inferred.
- Some human messages arise without a preceding AI response; these can be human-initiated scientific proposals but do not support a literal preceding-AI counterfactual. The frozen manual already includes an `initiate` category; preserve it.
- In 45 **candidate cues**, another visible user turn falls between the referenced AI message and the candidate response. The pointer is still chronologically valid, but independent adjudication must assess whether these represent one contiguous decision or multiple distinct interventions.
- The source-provenance checks passing on all existing Phase 2 candidate pointers establishes only mechanical pointer integrity.
- The manuscript documents labeled with 2026-11-16 in their filenames are *dated drafts or anticipated submission versions* as of 2026-11-13; they are not verified post-submission artifacts by filename alone.

## Independence and audit trail

Keep original exports immutable. Never silently regenerate the V1 source, change data exposure judgments or overwrite an adjudication without preserving a revision. Any change to primary scientific definitions requires v1.1+ and an explicit rationale, not a Phase 4 script edit.

A human coder who participated in the Hsp60/10 research may participate in coding; at least one independent coder should not have worked on the original project. Preserve each coder's source references, disagreements, adjudication and reason codes. AI suggestions to coders are **not** an independent second human rater.
