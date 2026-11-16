# Contribution dynamics: conversation-cohort analysis

**Estimand:** number of registered, provisional contribution events per 100 user turns, grouping both events and turns by the date their *conversation opened*. A conversation may remain active across multiple months. This is **not** event occurrence date or a valid calendar-month contribution rate.

**Denominator:** all user turns of the source-screened 245-conversation corpus, including conversations with zero registered events. The 229 contribution register has not been independently established to be exhaustive or free of duplicate substantive decisions. Accordingly the rate describes registry capture, not true prevalence of scientific contributions.

**Independence:** events cluster within conversations; do not treat them as independent observations in naive regressions or use conventional binomial CIs. Do not draw temporal-causal inferences from these descriptive statistics.

**Human/AI interaction:** this audit has the **human user turns only**, not preceding assistant responses. Therefore ``human originated``, ``AI correction``, and ``AI refinement`` cannot be validly assigned with the supplied source alone. The 60-case private review sample requires the surrounding AI and human exchanges and independent annotation. A user phrase like “wait” is not a validated correction label.

**Governance:** no user message text, participant data, restricted results, private event register, or source-message identifiers should be committed to the public repository. The script and tests contain synthetic examples only.

Usage after preparing local, approved input CSVs with columns:

```
python3 scripts/cohort_event_density.py --event-csv /private/events.csv --user-turn-csv /private/user_turns.csv --output-csv /private/cohort_summary.csv
python3 -m unittest discover -s tests -p 'test_cohort_event_density.py' -v
```

Only submit aggregate results to public GitHub after disclosure review.
