# Phase 14 — Integrating independent investigator eligibility decisions

This is an **add-only**, post-freeze investigator adjudication overlay. It does not amend the protocol file or edit the human workbook. The source workbook, individual human rationales, IDs, and private ledger remain local.

## Inputs and precedence

- Start from the 597-row Phase 13 effective ledger (2025-10-01 and later), with the four earlier wet-lab exclusions and 45 AREA literal rule matches already applied.
- Link the 40 independently recorded Phase 11 human case IDs to 40 conversations using the locked **private** crosswalk, and cryptographically verify the private transcript text and source fingerprints.
- Preserve `ai_original_label`, the Phase 13 row and original human decision fields. Append a separate human-adjudication audit, never overwrite a first-pass decision.
- For any existing hard-scope investigator rule, refuse contradictory human overlays pending explicit scope adjudication. Matching judgments confirm without replacing the earlier scope-reason tag.
- For other reviewed cases, record the human classification as the effective working label, regardless of whether AI previously selected INCLUDE, EXCLUDE, or UNCERTAIN. Do not treat an AI `UNCERTAIN` as disagreement error.
- Report agreement and adjudicated counts separately. This is the investigator's retrospective project knowledge, not an independent blinded gold standard of conversation content.

## Observed results

The 40 original human entries were complete; 11 differ from the Phase 13 working labels, resolving 10 uncertain cases. The effective working count becomes **200 include / 296 exclude / 101 uncertain**. The 597-row sampling frame does not change. No new scientific interventions have been coded.

## Limits

Only one experienced investigator supplied retrospective context; possible incorporation and recall bias remain. The next 24-case source-context queue is selected for **targeted adjudication**, not population recall estimation. Project-defined inclusion and exclusion and the AREA literal rule are post-freeze clarifications. Formal sensitivity analyses and a separate probability sample are necessary before a final corpus freeze.
