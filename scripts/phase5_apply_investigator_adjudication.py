"""Apply a private, append-only investigator eligibility adjudication overlay.

Public outputs contain aggregates only. The immutable first-pass labels and original
blinded-review labels are not rewritten. No independent reliability measure is
recomputed using adjudicated decisions.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

VALID = {"include", "exclude", "uncertain"}


def load_rows(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def summarize(first_pass, overrides):
    """Validate provenance and return public-safe aggregate counts only."""
    original = {}
    for row in first_pass:
        ident = row["conversation_id"]
        if not ident or ident in original:
            raise ValueError("missing or duplicated first-pass conversation ID")
        if row["decision"] not in VALID:
            raise ValueError("invalid first-pass decision")
        original[ident] = row["decision"]

    revised = original.copy()
    audit_counts = Counter()
    seen_cases = set()
    seen_ids = set()
    for row in overrides:
        case_id, ident = row["case_id"], row["conversation_id"]
        if not case_id or case_id in seen_cases or ident in seen_ids:
            raise ValueError("missing/duplicated adjudication record")
        seen_cases.add(case_id)
        seen_ids.add(ident)
        if ident not in original:
            raise ValueError("adjudication record absent from first-pass corpus")
        if row["locked_ai_label"] != original[ident]:
            raise ValueError("locked AI label differs from original source")
        if row["final_label"] not in VALID - {"uncertain"}:
            raise ValueError("adjudication cannot leave final label uncertain")
        if not row["investigator_rationale"].strip():
            raise ValueError("adjudication missing investigator rationale")
        if row["evidence_status"] != "INVESTIGATOR_CLARIFICATION_NOT_INDEPENDENT":
            raise ValueError("unrecognized adjudication evidence status")
        revised[ident] = row["final_label"]
        audit_counts["reviewed"] += 1
        audit_counts["changed"] += (original[ident] != revised[ident])
        audit_counts["resolved_uncertain"] += (original[ident] == "uncertain" and revised[ident] != "uncertain")
        audit_counts["originally_included_unchanged"] += (original[ident] == "include" and revised[ident] == "include")

    before, after = Counter(original.values()), Counter(revised.values())
    return {
        "status": "PROVISIONAL_INVESTIGATOR_ADJUDICATION_NOT_CORPUS_FREEZE",
        "first_pass_n": len(original),
        "first_pass": {name: before[name] for name in ["include", "exclude", "uncertain"]},
        "post_adjudication": {name: after[name] for name in ["include", "exclude", "uncertain"]},
        "reviewed_case_count": audit_counts["reviewed"],
        "changed_case_count": audit_counts["changed"],
        "uncertain_cases_resolved": audit_counts["resolved_uncertain"],
        "included_case_confirmed_unchanged": audit_counts["originally_included_unchanged"],
        "independence": "investigator adjudication, not an independent second review",
        "reliability_rule": "preserve original blind 40 agreement estimates; do not recompute from adjudicated labels",
        "exposure_and_implementation": "not evaluated by this aggregate",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--first-pass", required=True, type=Path)
    parser.add_argument("--adjudication", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = summarize(load_rows(args.first_pass), load_rows(args.adjudication))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
