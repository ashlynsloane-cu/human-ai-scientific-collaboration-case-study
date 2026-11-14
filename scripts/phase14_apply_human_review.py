"""Apply independent human decisions to a private screening ledger without rewriting history.

This module contains no case identifiers or source text. Keep actual input/output CSVs private.
"""
from collections import Counter

ALLOWED = {"include", "exclude", "uncertain"}
HARD_SCOPE_TYPES = {"INVESTIGATOR_AREA_LITERAL_SCOPE_RULE", "INVESTIGATOR_SCOPE_EXCLUSION"}
HUMAN_ADJUDICATION = "INVESTIGATOR_HUMAN_BLINDED_PHASE11"


def validate_and_apply(base, decisions, *, expected=40):
    """Return (new_rows, audit_rows, aggregate) from private lists of dictionaries."""
    if len(base) != len({r["conversation_id"] for r in base}):
        raise ValueError("Duplicate base conversation identifiers")
    if len(decisions) != expected:
        raise ValueError("Unexpected number of human decisions")
    if len(decisions) != len({r["case_id"] for r in decisions}):
        raise ValueError("Duplicate human case identifiers")
    if len(decisions) != len({r["conversation_id"] for r in decisions}):
        raise ValueError("Duplicate mapped conversation identifiers")
    lookup = {r["conversation_id"]: r for r in base}
    after = {k: dict(r) for k, r in lookup.items()}
    audit = []
    for d in decisions:
        cid, human = d["conversation_id"], d["human_label"]
        if cid not in lookup:
            raise ValueError("Unknown human-reviewed conversation")
        if human not in ALLOWED:
            raise ValueError("Invalid human label")
        old = lookup[cid]
        if old["current_working_label"] not in ALLOWED:
            raise ValueError("Invalid existing label")
        if d.get("original_ai_label") != old["ai_original_label"]:
            raise ValueError("Locked initial AI label mismatch")
        if d.get("case_text_sha256") is None or len(d["case_text_sha256"]) != 64:
            raise ValueError("Missing case evidence fingerprint")
        if d.get("source_fingerprint") != old["source_fingerprint_private"]:
            raise ValueError("Base ledger source fingerprint mismatch")
        if not str(d.get("human_rationale", "")).strip():
            raise ValueError("Human decision lacks rationale")
        if old["adjudication_type"] in HARD_SCOPE_TYPES and human != old["current_working_label"]:
            raise ValueError("Human label conflicts with existing hard scope rule; requires separate adjudication")
        new = after[cid]
        prev = old["current_working_label"]
        new["phase14_previous_label"] = prev
        new["phase14_previous_adjudication_type"] = old["adjudication_type"]
        new["phase14_human_label"] = human
        new["phase14_human_case_id_PRIVATE"] = d["case_id"]
        if old["adjudication_type"] in HARD_SCOPE_TYPES:
            new["phase14_status"] = "CONFIRMED_AGAINST_PREEXISTING_SCOPE_RULE"
        else:
            new["current_working_label"] = human
            new["adjudication_type"] = HUMAN_ADJUDICATION
            new["phase14_status"] = "HUMAN_ADJUDICATION_APPLIED"
        audit.append({"case_id": d["case_id"], "conversation_id": cid,
                      "previous": prev, "human": human,
                      "effective": new["current_working_label"],
                      "action": new["phase14_status"],
                      "human_rationale": d["human_rationale"],
                      "case_text_sha256": d["case_text_sha256"],
                      "original_ai_label": old["ai_original_label"]})
    ordered = [after[r["conversation_id"]] for r in base]
    before = Counter(r["current_working_label"] for r in base)
    final = Counter(r["current_working_label"] for r in ordered)
    n_changes = sum(r["previous"] != r["effective"] for r in audit)
    return ordered, audit, {"total": len(base), "reviewed": len(decisions),
        "before": dict(sorted(before.items())), "after": dict(sorted(final.items())),
        "human_labels": dict(sorted(Counter(d["human_label"] for d in decisions).items())),
        "changed_labels": n_changes,
        "uncertain_resolved": sum(a["previous"] == "uncertain" and a["effective"] != "uncertain" for a in audit),
        "original_ai_labels_preserved": True}
