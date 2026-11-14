# Phase 13 — AREA project boundary

## Investigator directive
Exclude conversations with literal uppercase `AREA` from the computational Hsp60/10–ROSMAP case-study corpus, even if they contain ROSMAP. This is an investigator-directed post-freeze exclusion rule, not evidence that previous AI judgments were erroneous.

## Operationalization
- Unit: complete conversation among 597 created from October 1, 2025 onward.
- Scan original title, mapped user and assistant text across mainline and alternative branches.
- Case-sensitive independent-token `AREA` detection; this includes underscore-delimited filenames. Do not match unrelated lowercase `area` or substrings in longer words.
- Any matched conversation receives a provisional scope exclusion, with original label and adjudication status preserved.
- Do not infer inclusion for unmatched conversations; existing include/exclude/uncertain classifications remain untouched.
- Match counts and provenance are retained locally, and automatic false-positive candidates are explicitly quarantined for later human adjudication.

## Evidence limitations
An assistant's incidental mention may trigger a literal match even where the user's scientific work is Hsp60/10. Two potential over-exclusion cases were identified and flagged. No final corpus freeze or contribution coding should be based on unresolved literal-match exceptions. The prior human ratings, earlier validity estimates and four previous wet-lab investigator exclusions remain unchanged.

## Reproducibility
Script accepts an owner-local 597-row ledger and matching source JSON shards; rejects duplicate/missing IDs, invalid labels and source hash mismatches if the private hash ledger is supplied. Outputs only private overlay and updated ledger, never source content to public result files.
