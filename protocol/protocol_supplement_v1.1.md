# Human–AI Scientific Collaboration Case Study — Protocol Supplement v1.1

**Freeze date:** 2026-11-16  
**Status:** prospective analytic-specification supplement to the frozen `protocol/protocol_v1.0.md` and `protocol/coding_manual_v1.0.md`. Neither original document is replaced.  
**Scope:** frozen, qualified, export-defined Hsp60/10–ROSMAP corpus (245 conversations), not all human–AI research or all the investigator's account history.

## Scientific objective and original research questions (unchanged)

Characterize how human scientific oversight redirected, corrected, constrained, initiated, or accepted AI-assisted scientific work, and whether those decisions propagated into research artifacts.

- **RQ1:** How frequently did the human alter AI-generated scientific work?
- **RQ2:** Where in the scientific workflow did human steering occur?
- **RQ3:** How far did individual human interventions propagate?
- **RQ4:** How different would the final research product have been without human steering?
- **RQ5:** What kinds of AI problems required human interception?

## 1. Observation units and denominators

Three distinct units must not be conflated:

1. **Atomic AI proposal opportunity:** one identifiable, actionable scientific proposal (question, analytic approach, model, figure claim, experimental choice, etc.) presented in an assistant response. Multiple independent choices in one response create multiple opportunity units; reiterations of the same proposal without a new choice do not. Enumerate **before** reading the corresponding human response when feasible.
2. **Substantive human steering event:** a source-grounded human intervention affecting at least one scientifically meaningful dimension in protocol v1.0. Contiguous reiterations of the same decision form one event. Events may respond to one or several proposal opportunities. An event may also be **human initiated**, with no preceding AI proposal.
3. **Artifact-level observation:** one independently observable downstream effect on analysis specification, code, statistical output, figure, supplementary table, Methods, Results, Discussion, abstract/title, reviewer response, or repository/release. An artifact can be linked to multiple events; prevent duplicated attribution in unique-artifact summaries.

**RQ1 opportunity-based estimand:** number of atomic AI proposal opportunities receiving at least one substantive human alteration (modify_local/constrain/redirect/reject/correct) divided by all *human-addressed and observable* atomic proposal opportunities in the eligible corpus, after distinguishing opportunities with no observed human response. Report human-initiated events separately, not in the numerator or denominator of this estimand. Report acceptances and no-response separately. Do not divide by user-message count or total assistant messages.

Opportunity-level measurement requires an **opportunity register**, including source assistant message, proposal span, response window, disposition, event IDs and censoring/observability; the 229-event inventory alone is insufficient. One event may address multiple opportunities, and multiple events may concern one opportunity; avoid numerator inflation with unique opportunity identifiers.

## 2. Intervention and comparison coding

Preserve v1.0 codes: `accept`, `modify_local`, `constrain`, `redirect`, `reject`, `correct`, `initiate`; decision level 0–4; divergence D0–D4; workflow domain and issue/error codes.

- `accept` is an AI proposal opportunity disposition, **not automatically a substantive human steering event**. Revisit candidate event eligibility where the sole evidence is 'yes, continue' or faithful execution of an AI proposal.
- `initiate` requires a substantive, novel human scientific choice not already present in the relevant immediate AI proposal; if no AI predecessor, divergence and AI counterfactual fields are N/A, not D0.
- A request to verify/check is not a confirmed scientific correction unless an erroneous premise is identified and corrected. A precautionary limitation is distinct from a demonstrated AI error.
- Resolve multi-part user turns as atomic decisions and contiguous duplicate turns before final event counts.
- For RQ4 compare the observed immediate predecessor AI proposal with the subsequent human decision. This is **local proposal-level divergence**, not an estimate of what a hypothetical autonomous AI scientist would have accomplished.

## 3. RQ-specific primary summaries

- **RQ1:** eligible opportunity count; per-opportunity altered/accepted/unanswered proportions with explicit denominator; separate initiated-event count. At the conversation level, report number of conversations with one or more opportunities. If exhaustive opportunity enumeration is not verified, report **pilot only**, no corpus-level steering rate.
- **RQ2:** count and proportion of independently coded steering events by workflow domain, intervention class, and decision level; event-based denominator after de-duplication. Cross-domain coding is allowed, but primary domain categories are exclusive. Distinguish human initiation from AI-response alterations.
- **RQ3:** event-by-artifact-class binary evidence matrix, number of distinct artifact classes per event, prevalence of each class, and final retention. Report observed, partial, and indeterminate separately; negative recommendations can be adopted through manuscript wording, documented non-execution or scientific claim restraint. Artifact correspondence alone is not causal attribution.
- **RQ4:** empirical distribution of D0–D4 and CF0–CF4 **only for events with a recoverable and actionable AI predecessor**; do not treat missing predecessors as no divergence. Present exemplar quotations under governed access, not in public repository.
- **RQ5:** confirmed errors/problems by issue class and workflow; distinguish independently established error, plausible concern, correction request, and mistaken human assertion. The denominator for issue-class proportions is interventions with an independently adjudicated issue, not all 229 automatically.

## 4. Evidence outcomes (supplemental, not replacement for RQs)

A = source-linked substantive contribution (candidate / confirmed / excluded). B = independently supported downstream adoption/alignment (supported / partial / indeterminate / not retained). C = supported causal sequence (direct revision chain / suggestive chronology / not established). Never infer C from B. Absence of a script cannot refute an intentional avoidance, claim recalibration, or rejected experiment.

## 5. Missingness and validation

Enumerate assistant proposal opportunities and link to source-bearing user replies. Preserve `not recoverable`, `not actionable`, `unanswered`, `coding uncertain` distinctly. For documented no-response, distinguish missing continuation from rejection. Do not assign interaction type based only on user-text linguistic cues.

Independently double-code a predefined, category-stratified sample at **both event-boundary/opportunity-detection and label levels**, blind to the primary coder's labels; document independent agreement, disagreements, and adjudicated outputs. The Phase 49 60-case sample is an initial **calibration**, not an independent holdout after method iteration. Draw a separate holdout after freeze of instructions and piloting. The originating investigator alone cannot provide independent validation.

Bootstrap or confidence intervals may describe sampling uncertainty within the selected corpus; they must not imply generalizability from one investigator/project. Cluster by conversation when appropriate and disclose prevalence-dependent kappa limitations. No causal treatment effect or generalized human–AI performance estimate is identified by this observational single-case design.

## 6. Primary-versus-exploratory boundaries

Original RQ1–RQ5 endpoints above are primary. `contribution per user turn`, `conversation start month`, `within-conversation position`, and exploratory subgroup associations are **secondary/descriptive**, not substitutes for the opportunity denominator. Do not interpret archived conversation creation month as intervention date. No composite impact score (retain v1.0 ban on D×S×P).

## 7. Predeclared processing gates and stopping rule

1. Verify frozen conversation IDs and source message integrity; record unlocated/unrecoverable sources.
2. Build complete atomic opportunity register from recoverable assistant messages, including response mapping and human-initiated events; test boundary coding reliability.
3. Apply v1.0 codebook to all eligible events, adjudicate ambiguous/duplicate events; do not silently retain all 229 if exclusions apply.
4. Link downstream artifacts; preserve indeterminate outcomes; audit a blinded subset for independent reliability.
5. **Only then** release corpus-level RQ1–RQ5 primary estimates. Exploratory/pilot feasibility metrics can be reported earlier with explicit calibration-only labels.

Targeted evidence follow-up stops when primary downstream artifact and directly linked revision history have been inspected, or when obtaining additional evidence would not alter a prespecified primary endpoint. Additional searches may be triggered by material discrepancies; do not indefinitely chase a higher 'verified' percentage.

## 8. Analysis versioning and audit governance

- Preserve original protocol v1.0 and coding manual unmodified.
- The 229-event Phase 49 register remains a provisional source-linked inventory; the 84 implementation-supported/7 manuscript-only tally is a historical artifact-evidence snapshot, not the primary steering rate.
- Exclude private chats, message IDs, transcript snippets, participant-level data, and restricted evidence from the public GitHub repository.
- Version all coding-rule changes; log deviations and label exploratory work. Use synthetic tests for public scripts, independently inspect private outputs before publication.
