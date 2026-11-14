# Hsp60/10 corpus freeze and pilot-methods checkpoint (Phase 19–25)

This is an **add-only public-methods checkpoint** built from previously verified Phase 19–25 repository-safe packages. It does not contain the private ChatGPT conversation export, eligibility roster, investigator review records, pilot transcripts, or candidate-event tables. The prior frozen protocol V1 is unchanged.

## Historical sequence

- **Phases 16–18:** Private investigator adjudications were completed but do not have standalone public-safe releases in this checkpoint. Phase 19 and later documents record the aggregate transitions; source-level overlays are retained in the private archives.
- **Phase 19:** False-exclusion audit design and pre-review 246/351 working snapshot (historical only).
- **Phase 20:** Post-review 245 included / 352 excluded, zero unresolved; random exclusion sample 60/60 excluded, with a finite-population uncertainty bound; not yet formally frozen at that phase.
- **Phase 21:** Export-defined closure and source-limitation assessment.
- **Phase 22:** Final alternate-branch eligibility decisions and conditional freeze-readiness summary.
- **Phase 23:** **Qualified freeze** of the 245-conversation ChatGPT-export-defined Hsp60/10 computational project corpus; `results/phase23/freeze_manifest_aggregate.json` is the authoritative *public aggregate* freeze manifest. The private immutable roster is stored separately.
- **Phase 24:** Purposive 15-conversation coding-methods feasibility review; **draft** coding refinements, no intervention rate.
- **Phase 25:** Complete first-pass *message-level screening* for the 15-conversation pilot (1,031 messages; 464 user turns; 188 candidate/ambiguous/verification turns flagged). These are **not** adjudicated intervention events, and no causal or downstream-impact estimate is claimed.

Historical counts in earlier phase files reflect the state *at those phases*. They do not override the Phase 23 frozen 245/352 roster or claim eligibility labels changed after the freeze.

## Verification

From repository root after extraction:

```bash
shasum -a 256 -c MANIFEST_CHECKPOINT_PHASE25.sha256
python3 -m unittest discover -s tests -p 'test_phase*.py' -v
```

The supplied add-only package was tested together: 39 Phase 19/20/21/23/25 synthetic tests passed. Tests verify logic and integrity constraints, **not** independent scientific adjudication. No new GitHub commit, pull request, or tag was created during preparation of this checkpoint.

## Scientific and governance boundaries

The corpus is limited to recoverable ChatGPT conversations created on or after 2025-10-01 relevant to the computational Hsp60/10–ROSMAP project. Earlier date and scope restrictions were adopted after protocol V1 and are disclosed. This is not an exhaustive account-wide, multimodal, or multi-AI-system corpus. Incomplete non-text/alternate-branch coverage and unavailable legacy 31-row crosswalk remain limitations. The 60-case exclusion audit has nonzero sampling uncertainty. Independent event coding and proposal-unit calibration are still outstanding.

**Never commit private Phase 19–25 ZIPs, CSV review tables, user-message texts, conversation identifiers, or the private Phase 23 frozen roster.**
