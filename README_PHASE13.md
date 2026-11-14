# Phase 13 — Investigator-directed AREA exclusion rule

This is an add-only, post-protocol-freeze scope adjustment applied to the October 1, 2025–onward Hsp60/10 computational-study audit. The investigator directed that conversations containing the uppercase acronym **AREA** be excluded, including those involving ROSMAP. The rule is based on the presence of uppercase standalone `AREA` in the title or user/assistant messages (including alternate branches). Ordinary lowercase `area` is not a trigger.

The public package includes only aggregate counts, methodology and reproducible validation code. All conversation identifiers, excerpts, investigator rationales and source-linked review files remain in the **private** archive.

**Critical limitation:** A literal token match is not equivalent to verified separate-project membership. Two conversations appear to contain incidental uppercase mentions despite primary Hsp60/10 content; they are provisionally excluded by the investigator's literal rule but specifically flagged for exception review **before final corpus freeze**.

The frozen V1 protocol is not silently amended. This rule and all before/after labels must remain visible in audit history. No human or AI classification is retrospectively rewritten and earlier reliability analyses remain unchanged. Final validation of the date-restricted corpus is still outstanding.

To replay with owner-local source files:

```bash
python3 scripts/phase13_area_scope_rule.py \
  --ledger /path/to/PHASE10_SCOPE_597_EFFECTIVE_AFTER_WETLAB_EXCLUSION_PRIVATE.csv \
  --export-dir /path/to/unpacked_export \
  --outdir /path/to/private_output \
  --expected-size 597 \
  --frozen-hash-ledger /path/to/PRIVATE_PROVENANCE.json
python3 -m unittest discover -s tests -p test_phase13_area_scope_rule.py -v
```

The output produced by the script is private and must not be committed. No outside research artifacts are required.
