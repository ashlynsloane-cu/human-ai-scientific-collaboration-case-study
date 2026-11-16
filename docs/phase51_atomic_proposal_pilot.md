# Phase 51 — Atomic AI proposal calibration (public methods only)

**Status:** calibration, not a corpus-level estimate. Protocol v1.0 and supplement v1.1 remain frozen and unchanged.

## Rationale

One assistant reply can contain multiple actionable independent scientific proposals, and one human turn can accept one proposal while constraining another. Treat atomic proposal opportunities as the RQ1 denominator. Acceptance is an opportunity disposition, not automatically substantive steering. A human-initiated decision without a preceding AI proposal is a separate event and must not enter an AI-proposal denominator.

## Pilot process

1. Retrieve full assistant and user messages for the same conversation branch.
2. Enumerate atomic AI proposals and evidence claims with individually traceable text spans. Do not infer proposal opportunities from human text alone.
3. Assign stable opportunity IDs; do not treat an unchosen alternative as rejection.
4. Link each proposal to observed immediate user response, separately record human-initiated additions.
5. Mark ambiguity when the next turn does not resolve proposal disposition.
6. Validate IDs and required fields with `python3 -m unittest discover -s tests -p test_ai_opportunity_register.py -v`.
7. Require independent boundary coding before calculating RQ1 rates.

The private 17-opportunity calibration deliberately samples selected interactions and is not a complete enumeration, even within those messages. Its counts must not be used for primary percentages. No private message IDs, transcripts, scientific results, or experiment identifiers are included in this public package.
