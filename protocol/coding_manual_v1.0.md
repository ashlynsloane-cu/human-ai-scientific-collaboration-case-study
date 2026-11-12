# Coding Manual Version 1.0
**Frozen:** 2026-11-12

## Intervention Type
- accept: AI proposal retained without substantive human change.
- modify_local: local implementation/wording change; scientific question, analysis, and interpretation preserved.
- constrain: AI direction retained but claim/evidentiary strength narrowed.
- redirect: analysis, comparison, or scientific question changed.
- reject: AI-proposed analysis, mechanism, interpretation, or framing abandoned.
- correct: factual, mechanistic, statistical, logical, or evidentiary error fixed.
- initiate: human introduces a substantive idea not present in the immediately preceding AI proposal.

## Decision Level
- Level 0 — Cosmetic: no change to scientific content.
- Level 1 — Local: one local implementation or wording decision.
- Level 2 — Analytic Component: model, comparator, covariate, null, metric, sensitivity analysis, or scientifically meaningful figure panel changes.
- Level 3 — Scientific Inference: biological interpretation, evidentiary claim, mechanism, causal language, or meaning assigned to results changes.
- Level 4 — Project Architecture: central hypothesis, manuscript story, major analysis framework, or primary project direction changes.

## Divergence Class
Compare with the immediately preceding AI proposal:
- D0: no substantive change.
- D1: same question, analysis, and interpretation; implementation differs.
- D2: same question, but analysis specification or interpretation materially changes.
- D3: proposed analysis, claim, or mechanism replaced with another.
- D4: underlying scientific premise, central hypothesis, or major direction changes.

## Workflow Domain
Primary domain:
- hypothesis
- biological_mechanism
- statistical_design
- coding_implementation
- visualization
- interpretation
- manuscript
- peer_review
- reproducibility_release

Secondary domains may also be recorded.

## Error / Issue Category
- factual_error
- mechanistic_error
- statistical_error
- unsupported_inference
- causal_overstatement
- terminology_or_definition_error
- implementation_bug
- visualization_misrepresentation
- reproducibility_or_provenance_issue
- no_error_preference_or_design_choice

## Artifact Propagation
Record TRUE/FALSE for each:
1. hypothesis
2. analysis_specification
3. code
4. statistical_output
5. figure
6. supplementary_table
7. methods
8. results
9. discussion
10. abstract_or_title
11. reviewer_response
12. repository_or_release

Artifact propagation count = number of TRUE classes.

Do not infer propagation merely because an event was important; downstream evidence is required.

## Final Retention
- TRUE: change present in final frozen submission/release.
- FALSE: later abandoned or superseded.
- UNCERTAIN: cannot establish.

## Temporal Persistence
When dates permit:
final_retention_date - intervention_date.
If superseded:
supersession_date - intervention_date.

## Downstream Dependency Count
Count later coded decision events that explicitly depend on this event.

## Counterfactual Coding
Question: What would differ if the immediately preceding AI proposal were accepted unchanged?
- CF0_no_meaningful_difference
- CF1_implementation_difference
- CF2_analysis_specification_difference
- CF3_interpretation_or_claim_difference
- CF4_major_scientific_narrative_difference

Counterfactual coding must be transcript-grounded. Do not speculate about what the AI might have proposed later.

## Event De-duplication
Merge multiple turns when they concern the same decision, occur contiguously/immediately, and introduce no new scientific decision.
Separate later turns that introduce a different scientific choice or new constraint.

## Evidence Standard
Each coded event must retain:
- source conversation identifier;
- date/time when available;
- concise AI proposal summary;
- concise human response summary;
- downstream evidence for propagation.

No event should be coded solely from memory.
