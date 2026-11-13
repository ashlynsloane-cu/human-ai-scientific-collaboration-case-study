# Attribution and evidence-linkage rules (Phase 3)

These procedures are operational source-handling practices; **the frozen V1 coding manual remains authoritative**.

| Evidence level | What is established | What is not established |
|---|---|---|
| P: Proposed | Attributable human or AI utterance specifies a scientific or technical action | Execution, adoption, validity |
| Q: Requested/approved | Later human utterance explicitly requests or approves it | Execution or persistence |
| I: Implemented | Dated code, figure, analysis file, experiment record, or other corroborating artifact exists | Correct execution or downstream retention |
| V: Verified | Reproducible run, tests, plotted output/data comparison, or independent review corroborates implementation | Final retention unless final artifact checked |
| R: Retained | Implemented change is present in identified final frozen output/release | Sole authorship or counterfactual project history |

A project change may also be **rejected before implementation**, or **superseded** by a later decision. These cannot be collapsed into a generic impact score.

For every candidate event, connect `source_conversation + node_id`, `preceding AI node`, optional `following AI node`, code/plot/artifact checksum, relevant Git commit/ref, review/adjudication status. Preserve the source identifiers locally, never in the public repository.

Do not assert AI authorship from a file in Git, nor user authorship from a pasted prompt. An AI-generated Codex suggestion is distinct from a figure that was actually produced and manually revised. A reviewer is an additional source of scientific direction and should be distinguished from the user and AI.

## Workstream-specific corroboration

- **Hypothesis**: initial proposal, alternatives, explicit constraints, later rationale/model or a document showing reframing.
- **Methods**: proposed statistical design contrasted against executable scripts and inputs; assess whether prescribed adjustment or test was actually run.
- **Code**: timestamped commits and diffs, run/test logs; note that Git authorship is not necessarily human authorship of the code text.
- **Figures**: map chat requests to figure script change, corresponding generated graphic, manuscript figure legend, final figure, and any rejection/revision.
- **Interpretation**: compare model outputs with the statements made, including withdrawn claims and explicit limitations.
- **Manuscript**: compare all archived versions without assuming the latest uploaded filename was the submitted publication version.

## Denominators

Primary V1 asks about substantive **human steering events**, not total messages. Secondary descriptive measures may count *AI proposals* with explicit, prespecified identification rules and de-duplication. Do not calculate proportions of AI ideas accepted or human decisions altered until both numerator and denominator populations have been validated across the eligible corpus.
