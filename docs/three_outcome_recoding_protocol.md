# Three-outcome framework for a human–AI scientific contribution audit

This implementation is a **reproducible recode of existing adjudicated status**, not a new verification of the underlying scientific events.

- **A: Documented candidate contribution**: Source-linked provisional candidate. Independent scientific eligibility/duplication review remains pending.
- **B: Downstream adoption/alignment evidence**: For computational tasks, implementation may be in code or saved output. For preventive claims and editorial constraints, manuscript wording is a suitable end product. Existence of a consistent artifact does **not** demonstrate that the person caused it.
- **C: Causal influence**: Not established from the status register alone. Requires temporal sequence and appropriate process evidence; counterfactual causation is still a stronger claim.

The five Phase47 B statuses map without upgrading evidence: implementation supported -> supported by artifact; manuscript retention -> supported by final manuscript; partial -> partial; unverified -> not established; not retained in main pipeline -> scope-specific non-retention.

**Safety:** This repo is public. Never commit source-linked private registers, conversation text, controlled human-subjects data, private research outputs, identifying participant records, or credentials. Run the script locally with a private register and retain its output privately. Synthetic tests do not need research data.

## Reproducibility

```bash
python3 -m unittest discover -s tests -p 'test_three_outcome_recoding.py' -v
python3 scripts/recode_three_outcomes.py /private/path/master.csv /private/path/recoded.csv
```

Existing category labels and the source denominator are provisional; the descriptive census is not a population estimate. Missing implementation evidence is not evidence of a failed contribution. The published numeric totals require an investigator-approved, disclosure-reviewed summary; no private numeric outputs are included in this package.
