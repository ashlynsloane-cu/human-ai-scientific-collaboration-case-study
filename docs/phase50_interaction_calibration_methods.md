# Phase 50 — Interaction-context recovery and calibration methods

This code operationalizes the *context retrieval* prerequisite for the frozen study's original RQ1–RQ5; it does **not** compute the RQ1 steering rate.

## Recovery definition

An original, source-linked human event has `user_and_preceding_assistant_recovered` only when the event's anchor user node exists on a conversation branch, its user text is nonempty, and the nearest prior assistant ancestor has nonempty text. The parser traverses parent links and skips tool nodes. The nearest assistant **may still lack an actionable scientific proposal**; further blinded, atomic proposal segmentation is required.

No predecessor is a separate status. Missing archival context is **not** equivalent to an AI acceptance, absence of steering, or zero divergence.

## Aggregate feasibility findings (not main outcomes)

- Eligible frozen corpus: 245 conversations; archived full-message shards recover 244.
- Provisional event register: 229 source-linked entries; 222 corresponding conversations recovered.
- Earlier assistant text recoverable for 190 event anchors (not yet 190 valid proposal comparisons).
- All 229 events' original user-source hash checks passed; exact human-text equality against archive part strings succeeds for 212 events and remaining formatting/representation mismatches require manual review.
- Prespecified Phase 49 calibration sample: 60 entries; 49 have recoverable preceding assistant text, 8 have no preceding assistant, 1 has an empty predecessor text, 2 lack the conversation shard.
- A convenience first-15-case qualitative coding pilot surfaced source-boundary/eligibility concerns. This is **not** an independent-coded sample and provides no population steering frequency.

## Required next primary-analysis gate

For each recovered assistant response: partition distinct scientific proposal opportunities; map subsequent human decisions to proposal IDs, include unanswered and accepted opportunities, adjudicate boundary cases with independent coders, then calculate RQ1. Retain initiation without AI proposal separately. For RQ4, compare exact predecessor proposal and documented human change only when both exist.

## Governance

Only the parser and synthetic tests belong in the public repository. Never commit source JSON, conversation IDs, private event registers, assistant or user message text, or investigator-coded examples. Keep the original v1.0 protocol and manual intact; the v1.1 supplement is additive and must be clearly versioned.
