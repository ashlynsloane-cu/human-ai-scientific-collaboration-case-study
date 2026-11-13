# Phase 3: Entire-project human–AI provenance audit

**Scope**: The scientific workflow, not only the manuscript. This is an operational expansion of evidence collection under the existing frozen protocol v1.0; it does not alter any inclusion, coding, or impact rules.

## What is in scope

- Original Hsp60/10/MIC hypothesis generation and reframing, including competing mechanistic interpretations and abandoned ideas.
- Experimental planning, model systems, controls, Western blots and qPCR, independent of whether findings entered the ROSMAP manuscript.
- Public dataset discovery and suitability, ROSMAP/MSBB cohort choice, RNA and TMT QC, preprocessing, and participant/sample matching decisions.
- Statistical specifications: differential-abundance contrasts, abundance-matched mitochondrial null models, correlation/network analysis, covariates, sensitivity analyses, and candidate prioritization.
- Computational code development, debugging, tests, and reproducibility failures and recoveries.
- Figure conception, aesthetics when they affect scientific communication, panel-level interpretation, implementation, corrections, and abandonment.
- Biological interpretation, mechanistic overreach, alternative hypotheses, and retained/constrained conclusions.
- Manuscript preparation, peer-review responses, supplementary materials, repository packaging and Zenodo submission.

See `data/phase3/full_project_workstream_register.csv` for evidence requirements and statuses.

## Two complementary evidence streams

**Primary, protocol-v1 stream — Human scientific steering events.**
A substantive human decision is evaluated using the exact frozen definitions and linked to the immediately preceding AI proposal when applicable. Human-initiated directions are also possible. No event is scored from keyword cues alone.

**Secondary, descriptive AI contribution inventory — Not a modification to V1.**
Record substantive AI suggestions, implementation work, accepted ideas, alternatives, detected errors, and whether the actual research contains corresponding changes. This prevents the project from reducing AI's role to mistakes or human corrections. If inferential metrics based on the AI inventory are added as *new primary outcomes*, that requires an explicit protocol amendment/version; do not silently change V1.

## Direction of attribution

1. Record who first introduced the concrete idea within the recoverable evidence (human, AI, reviewer, external literature, collaborator, unknown). A human request to `write code` is not automatically AI-originated scientific design; an AI-proposed analysis is not automatically adopted.
2. Capture the exact conversational sequence, including branch alternatives and links to prior messages.
3. Separate a *proposal* from *approval*, *actual execution*, *verification*, and *final retention*. ChatGPT saying it ran an analysis does not independently establish that it ran.
4. Link to dated analysis scripts, commit diffs, output files, figure source and versions, and the manuscript only when present.
5. Identify revisions that changed direction, results, analysis, or interpretation, and record proposals rejected before implementation.

## Negative and missing evidence

A rejected AI proposal may shape the project even without a downstream artifact. Conversely, an artifact may have been independently created or edited by a colleague, Codex, or another tool without traceable chat evidence. Record each as such; do not force attribution. Filename dates are descriptive and not independently proof of submission chronology.

## Data governance

Public GitHub files must contain neither raw account exports nor unredacted transcripts, participant-level ROSMAP data, source message node IDs, private document titles/identifiers, or unreviewed internal excerpts. Internal source maps and source-file hashes remain local. Do not publish manuscript variants just because research outputs are accessible.

## Current state

- The V1 protocol and coding manual were verified directly in the public case-study repository, including the frozen tag.
- The public ROSMAP/Hsp60/10 analysis repository is available as a separate evidence source.
- The private ChatGPT export can support message-level chronological reconstruction.
- Eight uploaded research artifacts are available for local version/figure tracing, but no causal human–AI attribution follows from their filenames or text differences alone.
- All downstream implementation/retention coding remains pending evidence triangulation and adjudication.
