#!/usr/bin/env python3
"""Apply a private investigator-eligibility overlay without overwriting past labels.

Usage:
 python3 scripts/phase15_apply_targeted_adjudication.py \
  --base PRIVATE_PHASE14.csv --cases PRIVATE_TARGETED_24.csv \
  --overlay PRIVATE_ADJUDICATION.csv \
  --output-ledger PRIVATE_PHASE15.csv --output-summary PRIVATE_SUMMARY.json
"""
import argparse
from collections import Counter
import csv
import json

VALID={"include","exclude","uncertain"}

def load_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def save_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader();w.writerows(rows)

def apply(base, cases, overlay):
    byid={r["conversation_id"]:r for r in base}
    if len(byid)!=len(base):raise ValueError("Duplicate base conversation")
    cby={r["case_id"]:r for r in cases}
    if len(cby)!=len(cases):raise ValueError("Duplicate source case")
    if len({r["conversation_id_PRIVATE"] for r in cases})!=len(cases):
        raise ValueError("Duplicate source conversation")
    if len({r["review_case_id"] for r in overlay})!=len(overlay):
        raise ValueError("Duplicate overlay case")
    if len({r["conversation_id_PRIVATE"] for r in overlay})!=len(overlay):
        raise ValueError("Duplicate overlay conversation")
    changes={}
    for o in overlay:
        case=cby.get(o["review_case_id"])
        if case is None:raise ValueError("Unknown review case")
        cid=o["conversation_id_PRIVATE"]
        if cid!=case["conversation_id_PRIVATE"] or cid not in byid:
            raise ValueError("Source conversation mismatch")
        orig=byid[cid]
        if (o["source_case_text_sha256"]!=case["case_sha256"] or
            o["source_file_PRIVATE"]!=case["source_file_PRIVATE"] or
            orig["source_file_private"]!=case["source_file_PRIVATE"] or
            orig["title_private"]!=case["title"] or
            orig["created_utc"]!=case["created_utc"]):
            raise ValueError("Source record mismatch")
        if (orig["current_working_label"]!="uncertain" or
            o["phase14_previous_label"]!="uncertain"):
            raise ValueError("Cannot change an already definitive decision")
        if orig["AREA_literal_match"]=="TRUE":
            raise ValueError("Conflicts with existing explicit AREA scope exclusion")
        if orig.get("phase14_human_label", "") not in ("", "uncertain"):
            raise ValueError("Conflicts with prior human definitive label")
        if o["original_ai_label_preserved"]!=orig["ai_original_label"]:
            raise ValueError("Original AI rating mismatch")
        if o["earlier_human_label_preserved"]!=orig.get("phase14_human_label", ""):
            raise ValueError("Original human rating mismatch")
        if o["phase14_previous_adjudication_type"]!=orig["adjudication_type"]:
            raise ValueError("Prior adjudication type mismatch")
        if (o["investigator_decision"] not in VALID or
            o["investigator_decision"]=="uncertain" or
            not o["investigator_rationale"].strip()):
            raise ValueError("Invalid decision or missing rationale")
        changes[cid]=o
    out=[]
    for r in base:
        x=r.copy();o=changes.get(r["conversation_id"])
        x["phase15_pre_review_label"]=r["current_working_label"]
        x["phase15_effective_label"]=o["investigator_decision"] if o else r["current_working_label"]
        x["phase15_investigator_case_id"]=o["review_case_id"] if o else ""
        x["phase15_investigator_reason"]=o["investigator_rationale"] if o else ""
        x["phase15_evidence_tier"]=o["basis"] if o else ""
        out.append(x)
    return out, dict(sorted(Counter(r["phase15_effective_label"] for r in out).items()))

def main():
    p=argparse.ArgumentParser()
    for key in ["base","cases","overlay","output-ledger","output-summary"]:
        p.add_argument("--"+key,required=True)
    a=p.parse_args()
    rows,counts=apply(load_csv(a.base),load_csv(a.cases),load_csv(a.overlay))
    save_csv(a.output_ledger,rows)
    with open(a.output_summary,"w",encoding="utf8") as f:
        json.dump({"count":len(rows),"labels":counts},f,indent=2,sort_keys=True);f.write("\n")

if __name__=="__main__":main()
