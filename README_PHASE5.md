# Phase 5 — first-pass Hsp60/10 corpus eligibility review

This add-only package records a **provisional**, source-anchored eligibility review of the 140-case Phase 4 pilot. It does **not** alter the November 12, 2026 frozen V1 protocol or the original ChatGPT export. Results are not scientific intervention or contribution counts.

**Important:** The first pass was performed by a single AI assistant inspecting extracted original source-message text and selected context. It was **not** independent double-coding, exhaustive human review, a complete multimodal audit, or a complete 1,049-conversation eligibility adjudication.

The private decision ledger (conversation IDs, source-node IDs, source snippets and review notes) is intentionally absent. Keep it outside this repository. A 40-case blinded second-review sample has been prepared privately, **not redacted or distributed**.

See `docs/phase5/` and `results/phase5/` for status and methods.

Run aggregate reconstruction from a separately stored private first-pass ledger:

```bash
python3 scripts/phase5_adjudication_summary.py \
  --private-ledger /path/outside/repo/pilot_eligibility_first_pass.csv \
  --out results/phase5/eligibility_first_pass_aggregate.json

python3 -m unittest discover -s tests -v
```

Do not commit the original conversation exports, the private review ledger, code that embeds private source IDs, or unredacted blinded reviewer packets.
