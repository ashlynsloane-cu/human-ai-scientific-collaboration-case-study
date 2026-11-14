# Phase 8 source-text eligibility audit: methods, limitations, and gates

## Scope and unit

The unit remains the **whole conversation** under frozen V1 inclusion rules. Conversations qualify when their source demonstrates substantive relevance to the Hsp60/10 research process, including failed or abandoned research. General laboratory advice is **not automatically Hsp60/10 project work**; unrelated AREA/other projects are not included solely because they use ROSMAP or similar methods. Grant/personal-statement retrospectives without original project research work are not automatically included.

## Frame and selection

Phase 6 produced the full 1,049-conversation index and a fixed 80-case probability audit from the 709 originally unscreened, post-pilot conversations. That sample was selected independently of new Phase 8 labels: 20 per post-pilot similarity quartile, using SHA-256 ranking and seed `20261113-phase6-prospective`.

Phase 7 independently screened 60 cases using a mixture of priority and random methods. Phase 8 processed the **164 original first-screened cases remaining after prior phases**, plus all 80 Phase 6 probability-sample cases. Three probability cases already classified in Phase 7 were carried forward unchanged. Therefore Phase 8 contributes **241 new** classifications, not 244.

This work is a **single-AI, selected-source-text triage**. It inspected source-derived excerpts from opening, later and keyword-bearing current-branch user turns with selected assistant context, plus expanded source checks for ambiguous cases. It is **not** an exhaustive examination of all mainline turns, alternate branches, images, attached files or off-platform history for every case. Its assignment to `include`, `exclude`, or `uncertain` is provisional pending independent review.

## Distinguishing categories

- **Include:** direct Hsp60/10 mechanism/experimental/analysis/figure/manuscript/submission/reproducibility work, or distinctive source context that materially identifies this project. Implementation and later retention are **not** eligibility requirements.
- **Exclude:** clearly different research project, unrelated subject, or purely retrospective biography without new project research activity.
- **Uncertain:** plausible methodological or figure overlap but no sufficient identifying project context; missing decisive attachments; or ambiguous mixed-purpose conversations. Never exclude merely because a keyword is absent.

All AI first-pass decisions are local-only alongside original message IDs, immutable SHA-256 fingerprints and private justifications. The original 140-case investigator addendum is applied as an overlay rather than overwriting locked classifications. No changes were made to V1 coding or prior blinded human agreement.

## Audit results and caution

The 80-case Phase 6 probability sample currently has **65 provisional AI exclusions and 15 unresolved classifications** (including three carried-forward Phase 7 cases). **There are no confirmed human eligibility outcomes for this sample yet.** These frequencies are not a missed-conversation rate. In particular, a lack of AI-labeled inclusion in a small sample is not proof that the screen had perfect recall. The probability sample's defined denominator is 709; it cannot be extrapolated naively to all 1,049 conversations or the 49 previously pilot-reviewed unscreened cases.

The 40-case Phase 8 human validation allocation was selected by fixed SHA rank before using the new AI labels: 10 from each of A, B, C, and the probability-audit partition. It is **balanced for disagreement diagnostics**, not designed to estimate the inclusion prevalence of the full export. Human source excerpts in that packet hide AI decisions. The 45 new uncertain cases form a **separate targeted follow-up group** and must not inflate the 40-case reliability denominator.

## Source provenance checks

The standard-library validator checks:

1. All eleven original JSON shards against the frozen source-file SHA-256 ledger and exact byte counts.
2. Exactly 1,049 unique source conversation IDs.
3. New private decisions are distinct from the 140 pilot cases and 60 Phase 7 cases.
4. Original source user-node pointer and full first-user-message SHA-256 for each of the 241 new records.
5. The original Phase 5 investigator overlay points to the original pilot record, original AI label, and source quote fingerprint.
6. Every one of the 80 probability-sample cases is accounted for once across Phase 7 and Phase 8.
7. Human and final decision fields remain blank in new AI-only records.
8. Public summary excludes private message IDs, content, quotations, dates, and private classifications.

**Passing these checks establishes source and computation integrity; it does not establish the factual correctness of the inclusion labels.**

## Prespecified safeguards before final inference

1. Independent human review of a blinded, preselected subset and targeted review of all substantive uncertainties. Preserve both initial labels and explanations.
2. Document and adjudicate every human–AI disagreement. Compute Cohen's kappa and exact agreement on the prespecified blind subset; describe the stratification and its effect on generalizability.
3. Review the remaining **608 unscreened-by-context** conversations. Use broad high-recall discovery, and audit non-text components or missing assets where project identity depends on them.
4. Reconcile the 31 reconstructed 2026 seed records to unique original conversation IDs, preserving ambiguities.
5. Complete inclusion/exposure and branch audits before freezing a fingerprinted eligible corpus. No E5 absence claim without actual exposure evidence.
6. Only after this point start frozen V1 substantive steering-event coding and later artifact linkage.

## Governance

All conversation identifiers, personal messages, source snippets, attachment links, AI and human case-level annotations remain local and unpublished. The public repository contains methods, synthetic tests, and aggregate status only. This phase does not establish intellectual authorship or AI causal effects.
