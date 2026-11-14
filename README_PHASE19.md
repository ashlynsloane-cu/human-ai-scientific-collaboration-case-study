# Phase 19 — False-exclusion review and project-scope corrections

This add-only, public-safe methods package follows the Phase 18 private investigator adjudications. It documents three source-reviewed, investigator-confirmed project conversations restored from the excluded group, without publishing source IDs or conversation text.

## Population reconciliation

- Scope: 597 exported ChatGPT conversations created on or after October 1, 2025, considered for the Hsp60/10–ROSMAP computational study.
- Phase 15 public count: 222 included, 298 excluded, 77 uncertain.
- Phase 16 private adjudications: 48 wet-lab exclusions, yielding 222 / 346 / 29.
- Phase 17 private adjudications: 12 computational inclusions, yielding 234 / 346 / 17.
- Phase 18 private adjudications: 9 inclusions and 8 exclusions from remaining uncertain cases, yielding 243 / 354 / 0; one mixed-context conversation retained as included.
- Phase 19: 3 investigator-confirmed false exclusions corrected, yielding **246 included / 351 excluded / 0 uncertain**.

**The earlier adjudications have private, versioned records and must not be represented as independently validated by these public tests.** Independent first-pass AI labels and human decisions remain immutable; the effective corpus is constructed through append-only overlays.

## False-exclusion validation design

1. Read the remaining 351 exclusions' current-branch user-message content and title, with source fingerprints and original conversation shards retained privately.
2. Correct the 3 source-identified errors through explicitly logged investigator evidence: one early hypothesis-development statistical comparison and two cases in which the AREA keyword was incidental to Hsp60/10 figure/manuscript work.
3. Draw a **simple random sample of 60 from the remaining 351 exclusions**, without replacement and with deterministic seed `20261114` applied to sorted private conversation IDs.
4. Add **10 randomly drawn inclusion controls**, independently selected and shuffled among the 60, to reduce raters' ability to infer original status.
5. Supply source excerpts for these 70 cases and a separate **7-case purposive review queue**. The source-identifying mapping and original classifications remain private and locked until human review.
6. Evaluate participant decisions against the locked records, report definite reversals and uncertainty separately, and only estimate the false-exclusion rate from the 60 probability-sampled exclusions after the human review is complete.

## Restrictions

- **Do not report `3/354` as a false-exclusion rate.** The three were identified from targeted exploration, not random sampling.
- The 70-case mixed review sample is **not completed**; no empirical error-rate estimate or sensitivity claim is available yet.
- Incidental occurrences of an uppercase `AREA` token do not establish that an otherwise Hsp60/10 project conversation belongs to the distinct AREA project. Such exceptions are recorded case by case rather than silently editing the prior literal filter.
- A conversation that mentions Hsp60/10 but belongs to wet-lab work, applications, or a different research project is not automatically included.
- Attachment contents and non-mainline conversation branches remain incompletely audited; source excerpt truncation can warrant an `UNCERTAIN` response.
- These records concern ChatGPT export only, not missing or deleted chats, separate Codex sessions, or a comprehensive census of all AI work.

All full case-level ledgers, review transcripts, researcher explanations, and locked label crosswalks remain private. Run synthetic tests with:

```bash
python3 -m unittest discover -s tests -p 'test_phase19_validate_false_exclusion.py' -v
```
