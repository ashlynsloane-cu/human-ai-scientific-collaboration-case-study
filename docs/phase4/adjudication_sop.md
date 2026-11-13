# Standard operating procedure: screen, trace, code, link

1. **Screen whole conversations.** Start with `PRIVATE_LOCAL_ONLY/review_pilot.csv`; inspect titles and source metadata first, then open only the original conversations needed to establish relevance and context. Do not give independent coders unrestricted access to unrelated personal chats. Label `include`, `exclude`, or `uncertain`, give an explicit reason, and record any inaccessible visual/file content. Do not rely on titles. The 100 probability-pilot entries are sampled independently from the four original screening strata. The 40 additional non-text selections are deliberately enriched, NOT an unbiased sample; five lexical rescues are a census of the previously known rescue set. There are 140 distinct records because selections overlap.
2. **Estimate missed-corpus risk before declaring coverage.** Compare adjudicated project-inclusion prevalence by original stratum. If any previously unflagged conversations are in scope, revise retrieval procedures with a versioned change log; repeat validation. Even if none are found, do not claim perfect recall from a 25-of-758 sample. Consider reviewing all originally unscreened conversations, especially those with missing multimodal context.
3. **Review artifact exposure.** For each included conversation, separately inspect user messages, attachments and rendered visuals where legitimately available. Unavailable content stays `unassessed`; do not assume there was no participant-level information.
4. **Define event boundaries.** Consider the exact preceding AI proposal and one or more contiguous human turns; distinguish `initiate` from response, and merge repeated reminders of the same choice under the frozen rule. Never equate a keyword/affirmation with implementation.
5. **Code without looking at desired outcomes.** Two independent coders use the unchanged V1 intervention types, decision levels, divergence classes, domains and error categories. Record source node identifiers only in a private source map. For ordinal decision level/divergence, use weighted kappa; for nominal categories Cohen's kappa; for binary artifact flags percent agreement (plus further metrics if justified).
6. **Trace implementation separately.** Ask: Was the change made in an analysis script, figure source, results table, manuscript, or experimental record? Timestamped code diffs and run logs are stronger evidence of implementation than the assistant claiming 'Done.' Mark `UNVERIFIED` when there is no artifact evidence. Never use commit author as a proxy for intellectual authorship.
7. **Assign final retention and temporal persistence only after dated downstream artifacts are verified.** A file named with a future date is not proof of submission. For human-initiated events with no preceding AI, the preceding-AI counterfactual must be explicitly non-applicable/unknown; do not invent it.
8. **Reconcile baseline reconstructed candidates.** Use the already frozen 31-row candidate corpus as a **candidate index**, not a source of authoritative conversation titles. Match by full content and time context; retain one-to-many ambiguity until adjudicated.
9. **Maintain a transparency ledger.** Record query terms, sampling seed and algorithm, screening versions, source fingerprints, coder IDs, decisions, reviewer changes, software/runtime versions, and evidence gaps in private logs. Publish only minimized aggregate metadata.

## Attribution evidence tiers (descriptive, not impact scoring)

- **Observed proposal:** an AI or human message proposed a method, hypothesis, coding change or figure.
- **Observed adoption:** a later human message explicitly accepted the proposal.
- **Verified implementation:** timestamped code, notebook, figure source, protocol or analysis output reflects the proposal.
- **Verified downstream persistence:** a dated later artifact retains the implemented decision.
- **Unestablished intellectual origin:** if an idea is pasted from an email, coworker, paper, other AI or preexisting plan, source-of-origin remains uncertain. Speaker role is not proof of original authorship.

These evidence tiers avoid assigning speculative percentages of research contributed by AI or humans.

## Privacy and review authorization

Keep the unfiltered personal-account export and unrelated conversations restricted to its owner. Independent coders should receive only approved, project-specific and appropriately redacted excerpts. If the work will be published or shared outside the team, obtain appropriate institutional guidance on privacy, coauthor consent, and whether ethical review is required before disclosure.
