# Eligibility review method, first pass

## Input and sampling

The starting population was the 1,049-conversation ChatGPT export checked in Phase 4. That phase generated a **140-case review set** comprising (with overlaps deduplicated):

1. A deterministic SHA-256-ranked, seed-20261113, *25-per-original-stratum* pilot (100 total, A/B/C/previously unscreened).
2. Deliberately enriched conversations containing non-text or attachment metadata (20 from the original screen and 20 from the unscreened set, before overlaps).
3. A census of the five previously identified lexical-rescue candidates.

These categories overlap: **do not treat 100 + 40 + 5 as 145 distinct conversations**. The 140 distinct cases are not a simple random sample; prevalence in the combined set cannot be generalized to all 1,049 conversations.

## First-pass reading procedure

The assistant inspected source-derived message-text digests for **all 140 cases**, including opening user turns, project-specific mentions, later turns, attachment existence, and selected assistant context; ambiguous cases received additional expanded source review. The reviewed source was the current conversation branch from the export. This is a **content-based provisional review**, not an assertion that all messages, alternate branches, user-uploaded files or embedded visuals have been completely read. Source metadata, message IDs, selected private quotations, SHA-256 content fingerprints and a case-specific rationale were retained in the local/private decision ledger.

Provisional decisions use only the V1 inclusion scope:

- `include`: the reviewed evidence connects a conversation materially to the Hsp60/10 research project.
- `exclude`: evidence identifies a separate project or an unrelated conversation, with no substantiated project link in the reviewed source.
- `uncertain`: available text does not permit confident project identity and/or decisive attachment contents are missing. **Do not resolve uncertain by keyword alone.**

A cross-conversation inference (e.g. same GSEA gene list) is explicitly flagged; it cannot substitute for independent origin verification.

## Sources of uncertainty and bias

- **Review independence:** one AI-assisted reviewer, no independent human coder, no blinded reliability result or adjudicated disagreements.
- **Incomplete assets:** mainline user messages can contain PDF/PNG/ZIP/R scripts and non-text material. Metadata is not proof of content, and absence of reviewed data is not absence of E5 data.
- **Scope confusion:** ROSMAP was also used in a different rotation studying AREA, monocyte/bulk RNA, and proteomics. Such conversations should not automatically be counted as part of Hsp60/10 research.
- **History:** editing or referencing Hsp60/10 in a GRFP application is not necessarily a substantive contribution to the underlying scientific project.
- **Temporal coverage:** several candidate project conversations predate the 2026 manuscript; the frozen protocol sets subject-matter rules rather than authorizing exclusion solely by year.
- **Screening recall:** a confirmed source-text match was found among the previously unscreened pilot cases. The remaining unscreened archive requires expanded inspection before claims of exhaustiveness.
- **Attribution:** Git authorship, a chat discussing code, and a later matching figure do not establish intellectual authorship or causal effect.

## Interpretation rules

The 69 included conversations are provisional source candidates, **not 69 confirmed steering events**. These counts must not be converted into a percentage of the entire project's human or AI contributions. No E0–E5 absence-of-exposure statement, null-result absence, implementation or final-retention inference follows from this review.

## Reproducing public aggregates

Run the standard-library script against the **private** CSV; it checks IDs, decisions, reason coverage, and the original pilot selection design before emitting only aggregate counts. The associated tests use synthetic records and verify non-disclosure of source identifiers. A separate local-only validator checked 140/140 real source pointers and hashes; no raw record is in Git.
