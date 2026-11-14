# Phase 20 — Eligibility adjudication and freeze-readiness gate

Date: 2026-11-14. This is a **post-freeze investigator eligibility adjudication** under the previously documented computational-project, date, and AREA scope amendments. It does **not** overwrite the frozen protocol or earlier independent classifications.

The private investigator confirmations resolve seven previously uncertain human review responses. The pre-review working corpus was 246 INCLUDE / 351 EXCLUDE; effective decisions are 245 INCLUDE / 352 EXCLUDE / 0 UNCERTAIN among 597 conversations.

The Phase 19 randomly sampled exclusions were selected from the 351 exclusions in the prior corpus. After source review, all 60 are excluded; none is a confirmed missed inclusion. Among 10 separately sampled included controls, nine are included and one is excluded as unrelated wet-lab work. Seven purpose-selected cases are all excluded. The targeted sample and controls are NOT part of the random exclusion prevalence estimator.

The exact one-sided 95% finite-population upper bound under a hypergeometric zero-miss model is 15 possible missed inclusions out of the original 351 exclusions (4.27%). Conditional on correct investigator labeling and genuinely random selection, this is a conservative count bound. It does not measure missing or deleted conversations or attachments, or the impact of post-freeze changes in scope.

**Freeze gate: NOT READY.** See `docs/phase20/freeze_readiness.md`. No original human or AI labels were overwritten. Private case identifiers, source text, source paths, and the 597-row source ledger are not published.

The generic replay script takes private input files as arguments. All private inputs must remain outside the public repo. The confidence bound uses only the Python standard library.
