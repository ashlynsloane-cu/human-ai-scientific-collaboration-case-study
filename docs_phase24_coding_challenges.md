# Pilot methodological challenges and proposed resolutions (draft)

1. **Source vs articulation vs response.** Track idea origin (human / AI / third party / mixed), who raised it in the transcript, and the human response to any prior AI proposal as separate fields.
2. **Opportunity denominator.** An assistant reply may contain several distinct actionable scientific proposals. Define *atomic proposal opportunities*; don't use raw assistant-message count as the denominator. Unanswered proposals are not accepted proposals.
3. **Initiation without immediate AI predecessor.** User-initiated ideas in conversation-opening messages may count under V1 `initiate`, but should not receive AI-proposal divergence/counterfactual codes without a source-linked predecessor. Document as N/A.
4. **Verification gate versus correction.** Requests to check a value or supply metadata must not be called successful corrections unless a specific erroneous premise and outcome are established.
5. **Multi-part and repeated turns.** Define criteria for splitting independent scientific choices and deduplicating repeated clarifications of one decision.
6. **Scientific versus cosmetic.** A figure's visual styling alone is not a scientific intervention; a scientifically misleading encoding or altered interpretation may be.
7. **Implementation evidence.** Distinguish proposal, planned execution, assistant claim, user-reported execution, and independently verified artifact state.
8. **Coders.** Pilot event detection and boundaries independently, not merely labels assigned to AI-selected spans. Treat calibration data separately from later holdout reliability analysis.
9. **Observational limits.** Immediate transcript-grounded divergence is not a causal counterfactual of a hypothetical autonomous-AI project.

This draft is not a modification to the frozen V1 codebook or scope. Adopt a versioned supplement before production coding.
