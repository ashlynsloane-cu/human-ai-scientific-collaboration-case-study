"""Map pre-adjudicated evidence statuses into three separate study outcomes.

Accepts aggregate-compatible CSV register with event_id, scientific_category,
scientific_phase, phase47_reconciled_evidence_state. Do NOT commit input registers.
"""
import argparse
import csv
from collections import Counter
from pathlib import Path

MAPPING = {
    "IMPLEMENTATION_SUPPORTED": "SUPPORTED_BY_DOWNSTREAM_ARTIFACT",
    "MANUSCRIPT_RETENTION_ONLY": "SUPPORTED_BY_FINAL_MANUSCRIPT",
    "PARTIAL_OR_AMBIGUOUS": "PARTIAL_OR_AMBIGUOUS",
    "EXACT_IMPLEMENTATION_UNVERIFIED": "NOT_ESTABLISHED",
    "NOT_RETAINED_IN_MAIN_PIPELINE": "NOT_RETAINED_IN_MAIN_PIPELINE_ONLY",
}


def recode(rows):
    ids = [row["event_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("event_id must be unique")
    result = []
    for row in rows:
        status = row["phase47_reconciled_evidence_state"]
        if status not in MAPPING:
            raise ValueError("Unexpected evidence status: " + status)
        rec = dict(row)
        rec["outcome_A"] = "SOURCE_LINKED_PROVISIONAL"
        rec["outcome_B"] = MAPPING[status]
        rec["outcome_C"] = "NOT_ESTABLISHED_FROM_CURRENT_REGISTER"
        result.append(rec)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    with args.input.open(newline="", encoding="utf-8-sig") as handle:
        records = list(csv.DictReader(handle))
    if not records:
        raise ValueError("Empty register")
    out = recode(records)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        w = csv.DictWriter(handle, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    print(f"Records: {len(out)}; Outcome B: {dict(Counter(r['outcome_B'] for r in out))}")


if __name__ == "__main__":
    main()
