# Phase 9: source-context eligibility extension — methods and limits

## Prespecified framework retained

The frozen V1 protocol defines relevant **Hsp60/10 project conversations**, not just conversations that yielded final research results. Unused exploratory analyses, human rejections of AI proposals, abandoned figures, and early hypothesis development can be in scope. Similar techniques from Jordan's syndrome, AREA, coursework, Drosophila, or other laboratory projects are not automatically in scope. A genuine project link is required.

## Source population and partitions

- Export census: 1,049 unique conversations across 11 original JSON shards.
- Earlier Phases 5, 7, 8: 441 distinct source-context provisional reviews, including a preserved three-case investigator adjudication overlay from Phase 5.
- Phase 9 remaining population: 608, all from the original *unscreened* category.
- All 608 were indexed for available mainline user/assistant string-text retrieval; 159 were flagged as having non-text material, and one had no extracted text user turn. Indexing is **not** an exhaustive read of images, files, deleted branches, or other missing payloads.
- The 120 highest-ranking remaining conversations were selected by the previously generated contextual priority score, with conversation ID only as a deterministic tie-breaker.
- Of the lower-ranked 488, 80 were selected by ascending SHA-256 of the fixed seed `hsp60-p9-lowrank-qc-20261113` and conversation ID. Selection preceded the Phase 9 label assignments.
- The 120-case ranking and the 80-case probability audit **must be analyzed separately**. The latter is probabilistic **only within the lower-ranked 488**, not the whole remainder or whole account.

## Reviewed evidence and classifications

For 200 selected conversations, the single AI reviewer assessed bounded source-user excerpts and source-derived context, with original source-message pointers and SHA-256 fingerprints retained privately. Mark `include` only when the available context directly establishes an Hsp60/10 project research activity; mark `exclude` provisionally when the inspected context establishes a separate project/unrelated activity or general background without such a link; mark `uncertain` if generic lab, research software, figure, poster, paper-submission, or neuron-model discussion does not identify the relevant scientific project. No uncertain was converted to a negative simply for lacking an Hsp60 keyword.

A filename or an assistant's unverified project assertion is not sufficient for inclusion, nor does the failure to mention Hsp60 suffice for exclusion when the procedure could plausibly be project work. All exclusions remain provisional because the first pass is excerpt-based, unblinded to the project's general topic, and lacks a complete multimodal review.

## Results and non-results

- 120 ranked: 74 provisional exclusions; 46 uncertain; no confirmed inclusion.
- 80 sampled lower-ranking: 72 provisional exclusions; 8 uncertain; no confirmed inclusion.
- Combined 200: 146 provisional exclusions and 54 uncertain; zero additional independently verified inclusions.
- Total provisional audit: 641 assessed; 408 without even Phase 9-level source-excerpt review.
- The cumulative 206 include / 309 exclude / 126 uncertain working distribution is **not an estimated incidence rate** and cannot be used as a project-contribution denominator.

## Distinct limitations

1. One AI reviewer can systematically miss relevance, especially for shorthand conversations, early hypotheses, and missing attachments.
2. The same model helped develop the research process; confirmation bias is plausible. Phase 5's 40-case blinded human agreement sample cannot be assumed to validate later phases.
3. The mainline source review does not establish content completeness on alternative conversation branches.
4. The corpus is a ChatGPT export, not necessarily all AI tools or Codex sessions used in the Hsp60/10 project.
5. Statistical missed-case rates must be based on an adequately sampled, independently coded denominator. This phase did **not** estimate recall, sensitivity, specificity, kappa, or AI contribution frequency.
6. The initial 31 reconstructed candidate records still require evidence-based reconciliation to original conversation IDs; their reconstructed labels must not be treated as original chat titles.
7. Original source exports, individual case records, and investigator reasons remain private. Any later external reviewer should receive only a privacy-cleared, need-to-know packet with institutional and coauthor permissions addressed.
