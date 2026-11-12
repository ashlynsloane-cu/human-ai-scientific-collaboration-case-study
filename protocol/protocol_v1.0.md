# Human–AI Scientific Collaboration Case Study
## Protocol Version 1.0
**Frozen:** 2026-11-12

## Purpose
This project studies how human scientific oversight changed the trajectory of an Hsp60/10–ROSMAP research project conducted with substantial ChatGPT assistance across hypothesis generation, analysis design, coding, plotting, manuscript drafting/editing, peer review, and reproducibility/release work.

The study quantifies:
1. how often the human altered AI-generated scientific work;
2. where in the scientific workflow human steering occurred;
3. how far individual interventions propagated into downstream artifacts;
4. how different the final research product would have been if immediately preceding AI proposals had been accepted unchanged; and
5. what kinds of AI errors, overreach, or implementation problems required human interception.

## Research Questions
RQ1: How frequently did the human alter AI-generated scientific work?
RQ2: Where in the scientific workflow did human steering occur?
RQ3: How far did individual human interventions propagate?
RQ4: How different would the final research product have been without human steering?
RQ5: What kinds of AI problems required human interception?

## Unit of Analysis
The primary unit is one substantive human steering event.

A steering event is counted only if a user intervention changes at least one of:
- scientific question;
- mechanistic interpretation;
- statistical specification;
- comparator/null/covariate/sensitivity analysis;
- interpretation of evidence;
- scientific content of a visualization;
- manuscript scientific claim or framing;
- reviewer-response scientific strategy;
- reproducibility/provenance/release state.

Routine confirmations, requests to continue, requests for explanation, and purely conversational messages are excluded.

## Corpus Inclusion Criteria
Include every recoverable ChatGPT conversation materially related to:
- Hsp60 / HSP60 / HSPD1;
- Hsp10 / HSP10 / HSPE1;
- mitochondrial chaperonin biology;
- MIC when connected to Hsp60/10 project reasoning;
- ROSMAP or ROS/MAP analysis;
- Hsp60/10 client or interactor analysis;
- manuscript planning, drafting, editing, figures, tables, reviewer revisions, or submission for the Hsp60/10 project;
- project-specific Braak/CERAD analyses;
- project-specific DLD/DLST, C1QBP, or other entities when context establishes relevance;
- repository, release, Zenodo, figure/table, or submission work for this project.

Conversation titles alone are insufficient for inclusion/exclusion. Full conversation content must be searched.

## Corpus Exhaustiveness Rule
Do not state that "all project conversations" were analyzed until an auditable complete conversation export or equivalent exhaustive account-level corpus has been searched using the predeclared inclusion terms plus context-based review.

Until then, all counts must be labeled as lower bounds or corpus-limited counts.

## Coding Order
1. Identify the complete eligible conversation corpus.
2. Extract candidate steering events without assigning impact scores.
3. De-duplicate events that represent the same decision across contiguous turns.
4. Apply the frozen coding manual.
5. Link each event to downstream artifacts.
6. Perform independent double-coding on a predefined subset.
7. Calculate inter-rater reliability.
8. Resolve disagreements by adjudication.
9. Only after primary coding is complete, derive any composite metrics or summary indices.

## No Composite Impact Score in Version 1
Version 1 explicitly prohibits hand-assigned multiplicative impact scores such as D × S × P.

Preserve observable dimensions separately:
- decision_level;
- divergence_class;
- artifact_propagation_count;
- final_retention;
- temporal_persistence;
- downstream_dependency_count.

A composite score may be considered only after empirical distributions are known and sensitivity analyses demonstrate robustness to alternative weighting schemes.

## Independent Coding
At least two coders should independently code a predefined subset of events.

Recommended reliability statistics:
- Cohen's kappa for nominal categories;
- weighted kappa for ordinal categories;
- percent agreement for binary fields.

If the researcher whose behavior is being studied is one coder, at least one coder should not have participated in the original project.

## Versioning
Any changes to these rules require a new protocol version.

Version 1.0 is frozen before comprehensive intervention coding begins.
