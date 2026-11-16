# Validating aggregate FDR outputs

`python3 scripts/check_fdr_family.py path/to/results.csv --p-column p --adjusted-column fdr`

If the family was adjusted separately by contrast, add `--family-column comparison`.

**Interpretation:** A match supports numerical consistency with BH adjustment over the
*exported family*. It does **not** verify model choice, sample independence, the original
complete test family, or that the export was unfiltered. A mismatch is an audit flag,
not proof of a statistical error. Confirm the generating script, model and complete
hypothesis universe before classifying an adjustment as incorrect.

This repository should contain only synthetic tests and reviewed public data.
Do not commit participant-level data, lab records, unredacted conversations, or
source-linked private adjudication registers.
