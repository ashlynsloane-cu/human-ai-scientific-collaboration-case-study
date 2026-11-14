# Phase 25 — Pilot-wide message screening and decision-unit stress test

Status: **completed first-pass message-level screen; independent event adjudication outstanding**.
This is not a completed primary-outcome analysis. The frozen Phase 23 eligibility corpus and protocol V1 were not changed.

## Input and coverage
15 purposively selected conversations from the 245-conversation qualified frozen ChatGPT-export corpus. All 1,031 canonical text messages (464 user, 567 assistant) were source-mapped and fingerprinted. All 464 user turns received a first-pass triage category. 30 source-anchored examples were reviewed qualitatively. A candidate boundary-review queue contains 188 turns, including 139 manually identified candidate scientific decision turns, 27 boundary-ambiguous turns and 22 verification/disagreement checks. **None of these numbers is an event count or intervention rate.** The remaining user turns also require checking for false-negative candidate screens during independent coding.

The work is *source-grounded but not independently validated*. Its manual/heuristic selection should not be used as model-performance or prevalence data. An assistant message may include zero, one, or many actionable scientific proposals; therefore 567 is NOT a decision-opportunity denominator.

## Pilot findings for primary analysis design
- V1 `initiate` decisions may begin with a researcher prompt, before any AI proposal. Do not invent a counterfactual AI alternative or set D0 for such cases; mark proposal-based divergence N/A pending codebook amendment.
- Scientific ideas can originate with a colleague or a prior paper and be articulated by the researcher. Preserve source-of-idea, speaker in transcript, and who changed the proposal as distinct fields.
- Source discussion may report **verification requests** without producing an objectively confirmed correction. Separate 'question raised' / 'error evidenced' / 'change observed'.
- Routine plotting aesthetics, repeated troubleshooting, and confirmations do not automatically satisfy frozen V1 steering criteria. Scientific figure re-interpretation can satisfy them, so a figure-editing title alone does not decide.
- A sequence may contain nonalternating roles, repeated user messages, and multiple scientific opportunities in a single assistant response. Units must be linked to IDs and semantic choices, not turns.
- AI statements like 'updated script' or 'fixed figure' are not artifact verification. Preserve proposed, assistant-claimed, user-reported and externally verified states separately.
- Post hoc final-retention assessment risks hindsight bias: code intervention from source exchange before consulting downstream artifacts.

## Two distinct denominators (proposed clarification; not adopted into frozen V1)
1. **Response-based steering:** among actionable AI-origin proposals for which a human response is observed, classify explicit accept / modify / constrain / reject / correct / redirect. Unanswered AI proposals are not accepted.
2. **Origin distribution:** classify independent, substantive scientific decision episodes as researcher-origin, AI-origin, external/colleague, mixed or unclear. This is NOT an AI-vs-human 'percentage of science'.

Primary V1 steering-event count and type/domain remain governed by frozen definitions. Underlying opportunity inventories, event detection, and decision episodes must be independently assessed. No numeric primary outcomes are reported.

## Proposed independent validation
Provide one uninvolved coder with the 15 full source transcripts and a blank user-turn/source spreadsheet, **without initial AI-coded labels**. The coder must identify actionable proposals, decision episodes and steering events independently; merely rating our 30 preselected examples would create detection bias. Reconcile event boundaries using source user-message IDs and a documented matching rule. Report event-detection agreement (precision/recall/F1 of matched spans, coder-count differences) separately from conditional categorical agreement for intervention type and level. Recode the pilot after any explicit operational addendum. Then validate a distinct held-out sample before full 245-conversation coding.

## Study limitations
Purposive 15-conversation selection; current-branch text only; alternate branches and nontext were not exhaustively coded. The user is the studied investigator, and human firsthand recollection cannot replace source evidence for behavioral counts. No repository/manuscript output propagation verification in this phase. No inference about counterfactual autonomous-AI research trajectories.
