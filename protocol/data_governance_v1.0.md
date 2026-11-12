# Data Governance Version 1.0
**Frozen:** 2026-11-12

## Core Principle
This meta-research project studies the interaction process. It does not require and must not include raw or participant-level ROSMAP data.

## Data Exposure Classification
- E0 — Conceptual: scientific discussion without project data.
- E1 — Code / Analysis Specification: code, pseudocode, model definitions, statistical plans, pipeline descriptions.
- E2 — Textual Research Artifacts: manuscript text, reviewer comments, responses, documentation, repository prose.
- E3 — Aggregate / Derived Results: aggregate counts, coefficients, P values, summary statistics, model outputs, derived non-participant-level results.
- E4 — Derived Visualizations / Summary Tables: plots or tables containing summarized/derived project results.
- E5 — Raw or Participant-Level Data: raw matrices, participant-level molecular measurements, individual phenotype records, subject identifiers, controlled-access row-level data, or equivalent.

## Publication Rule
Do not state "No raw or participant-level ROSMAP data were supplied to ChatGPT" unless the complete included corpus has been audited and contains zero E5 interactions.

Until then, use:
"The meta-analysis was designed to exclude raw and participant-level ROSMAP data; project interactions were audited for data-exposure class before analysis."

## Meta-Dataset Minimization
The public intervention ledger should avoid reproducing ROSMAP-derived numerical results unless necessary.

Prefer:
- "Human required regeneration from authoritative output"
over copying coefficients;
- "Human corrected pathology-model interpretation"
over reproducing result tables.

## Prohibited Public Content
- raw ROSMAP files;
- participant-level records;
- subject identifiers;
- controlled-access row-level data;
- credentials/access tokens;
- restricted paths revealing protected systems.

## Allowed Public Content
- conversation IDs or pseudonymous hashes;
- dates;
- coded intervention categories;
- paraphrased decision summaries;
- artifact propagation indicators;
- counterfactual categories;
- aggregate intervention counts;
- inter-rater reliability statistics.

## Audit Requirement
Before public release:
1. run corpus-wide E0–E5 classification;
2. manually review all candidate E5 records;
3. remove/redact restricted content;
4. document exclusions;
5. retain an internal audit log separate from the public dataset.

## Interpretation Guardrail
Do not imply that ChatGPT had direct access to ROSMAP repositories or participant-level datasets unless verified evidence shows that this occurred.
