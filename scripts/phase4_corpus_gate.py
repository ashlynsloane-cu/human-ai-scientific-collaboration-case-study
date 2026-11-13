#!/usr/bin/env python3
"""Reproducible pre-coding integrity and bias audit for ChatGPT exports.

No message bodies, IDs, or titles are written to the publication-safe output.
The private review queues MUST stay on encrypted/local restricted storage.
This script does not assign human steering, contribution, exposure or causation.
"""

import argparse
import collections
import csv
import datetime as dt
import hashlib
import json
import re
from pathlib import Path

PATTERN = re.compile(r"conversations-\d{3}\.json$")
STRATA = ("A_core_evidence", "B_context_review", "C_weak_or_ai_only",
          "out_of_scope_screen")


def message_text(message):
    parts = (message.get("content") or {}).get("parts")
    if not isinstance(parts, list):
        return ""
    return "\n".join(p for p in parts if isinstance(p, str))


def nontext_parts(message):
    parts = (message.get("content") or {}).get("parts")
    if not isinstance(parts, list):
        return 0
    return sum(not isinstance(part, str) for part in parts)


def mainline(mapping, current):
    """Return nodes by parent order, and nonfatal structural issues.

    Root pseudo-parents can be missing in historical ChatGPT exports; report
    their occurrence without labeling the export corrupt.
    """
    if not current or current not in mapping:
        return [], "missing_or_unknown_current_node", 0
    visited = set()
    path = []
    node_id = current
    unlinked_terminus = 0
    while node_id is not None:
        if node_id in visited:
            return list(reversed(path)), "cycle", unlinked_terminus
        if node_id not in mapping:
            unlinked_terminus += 1
            break
        visited.add(node_id)
        path.append(node_id)
        node_id = mapping[node_id].get("parent")
    return list(reversed(path)), "ok", unlinked_terminus


def read_csv(path):
    with Path(path).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path, records, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)


def stable_sample(population, size, seed, label):
    """Stable SHA-256-ranked pseudorandom subset, independent of Python RNG."""
    ranked = sorted(
        population,
        key=lambda item: (
            hashlib.sha256((str(seed) + ":" + label + ":"
                            + item["conversation_id"]).encode()).digest(),
            item["conversation_id"]),
    )
    return ranked[:size]


def build(export, screening_file, phase2_root, private, public, sample_n,
          multimodal_n, seed):
    files = sorted(f for f in export.iterdir() if PATTERN.fullmatch(f.name))
    if not files:
        raise ValueError("No conversations-###.json files located")
    manifest = json.loads((export / "export_manifest.json").read_text())
    manifest_files = {
        entry["path"]: entry["size_bytes"]
        for entry in manifest.get("export_files", [])
        if "path" in entry and "size_bytes" in entry
    }
    listed_jsons = {key for key in manifest_files if PATTERN.fullmatch(key)}
    present_jsons = {f.name for f in files}
    if present_jsons != listed_jsons:
        raise ValueError("Missing/extra conversation JSONs relative to manifest")
    file_digests = []
    for f in files:
        data = f.read_bytes()
        if len(data) != manifest_files[f.name]:
            raise ValueError(f"Manifest byte mismatch: {f.name}")
        file_digests.append({
            "filename": f.name, "size_bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        })

    screened = {r["conversation_id"]: r
                for r in read_csv(screening_file)}
    if len(screened) != len(read_csv(screening_file)):
        raise ValueError("Duplicate IDs in original screening index")
    if any(row.get("screening_tier") not in STRATA[:-1]
           for row in screened.values()):
        raise ValueError("Phase 1 input must contain only A/B/C flagged rows")
    rescues = read_csv(phase2_root / "out_of_scope_rescue_candidates.csv")
    rescue_ids = {r["conversation_id"] for r in rescues}
    if len(rescue_ids) != len(rescues):
        raise ValueError("Duplicate lexical-rescue conversation IDs")
    old_msgs = read_csv(phase2_root / "message_provenance_index.csv")
    old_events = read_csv(phase2_root / "candidate_intervention_queue.csv")
    old_coverage = {(r["conversation_id"], r["node_id"])
                    for r in old_msgs}

    overall = collections.Counter()
    contents = collections.Counter()
    candidates = []
    ids = set()
    event_issue = collections.Counter()
    chain_mapped = {}
    node_roles = {}
    eligible_nodes = set()
    intervening_user_turns = 0
    prior_ai_not_latest_visible = 0
    for f in files:
        for record in json.loads(f.read_text(encoding="utf-8")):
            cid = record.get("id") or record.get("conversation_id")
            if not cid or cid in ids:
                raise ValueError("Empty or duplicate conversation ID")
            ids.add(cid)
            mapping = record.get("mapping") or {}
            path, status, external_root = mainline(
                mapping, record.get("current_node"))
            overall["conversations"] += 1
            overall["structural_status:" + status] += 1
            overall["unlinked_root_terminus"] += external_root
            overall["nodes_total"] += len(mapping)
            stratum = screened.get(cid, {}).get(
                "screening_tier", "out_of_scope_screen")
            if stratum not in STRATA:
                raise ValueError(f"Unexpected screening tier {stratum}")
            counts = collections.Counter()
            path_positions = {node_id: idx for idx, node_id in enumerate(path)}
            chain_mapped[cid] = path_positions
            for node_id, node in mapping.items():
                msg = node.get("message") or {}
                if not msg:
                    continue
                role = (msg.get("author") or {}).get("role") or "other"
                if role not in ("assistant", "user"):
                    continue
                kind = (msg.get("content") or {}).get("content_type") or "missing"
                text_value = message_text(msg)
                multimedia = nontext_parts(msg)
                attachments = (msg.get("metadata") or {}).get("attachments") or []
                if not isinstance(attachments, list):
                    attachments = []
                node_roles[(cid, node_id)] = role
                overall["all_user_assistant_nodes"] += 1
                contents["role:" + role] += 1
                contents["kind:" + role + ":" + kind] += 1
                if role == "user" and kind == "multimodal_text":
                    overall["user_multimodal_nodes"] += 1
                    if multimedia:
                        overall["user_multimodal_with_nontext_parts"] += 1
                    if text_value.strip():
                        overall["user_multimodal_with_text"] += 1
                    if not text_value.strip():
                        overall["user_multimodal_without_text"] += 1
                overall["attachment_metadata_references"] += len(attachments)
                if node_id in path_positions:
                    overall["mainline_user_assistant_nodes"] += 1
                    counts["mainline_nodes"] += 1
                    counts["mainline_user_multimodal"] += bool(
                        role == "user" and kind == "multimodal_text")
                    counts["mainline_nontext_parts"] += multimedia
                    counts["mainline_attachments"] += len(attachments)
                    if role == "user":
                        counts["mainline_user_nodes"] += 1
                    # These are source nodes, not necessarily visible dialogue.
                    if text_value.strip() or attachments or multimedia:
                        eligible_nodes.add((cid, node_id))
                else:
                    counts["other_branch_user_assistant_nodes"] += 1
                    if role == "user":
                        counts["other_branch_user_multimodal"] += bool(
                            kind == "multimodal_text")
                        counts["other_branch_user_attachments"] += len(attachments)

            candidates.append({
                "conversation_id": cid,
                "title": record.get("title") or "",
                "source_file": f.name,
                "stratum": stratum,
                "rescued_by_phase2_lexical_search": cid in rescue_ids,
                "created_utc": dt.datetime.fromtimestamp(
                    record["create_time"], dt.timezone.utc).isoformat()
                if isinstance(record.get("create_time"), (int, float)) else "",
                "structural_status": status,
                "needs_nontext_review": bool(
                    counts["mainline_user_multimodal"]
                    or counts["mainline_attachments"]
                    or counts["other_branch_user_multimodal"]
                    or counts["other_branch_user_attachments"]),
                **{name: int(counts[name]) for name in (
                    "mainline_nodes", "mainline_user_nodes",
                    "mainline_user_multimodal", "mainline_nontext_parts",
                    "mainline_attachments", "other_branch_user_assistant_nodes",
                    "other_branch_user_multimodal", "other_branch_user_attachments")},
                "manual_project_inclusion": "UNASSESSED",
                "manual_exposure_E0_E5": "UNASSESSED",
                "manual_notes": "",
            })
    if not set(screened).issubset(ids):
        raise ValueError("First-screened conversations absent from export")
    if not rescue_ids.issubset(ids):
        raise ValueError("Lexical-rescue conversations absent from export")

    # Verify that the old Phase-2 source pointers resolve to the current tree.
    event_ptr_errors = []
    for row in old_events:
        cid = row["conversation_id"]
        user_id = row["human_user_message_node_id"]
        ai_id = row["preceding_ai_message_node_id"]
        if (cid, user_id) not in eligible_nodes:
            event_issue["user_pointer_unresolved_or_invisible"] += 1
            event_ptr_errors.append(row["candidate_id"])
        pos = chain_mapped.get(cid, {})
        if ai_id:
            if ai_id in pos and user_id in pos:
                gap = sum(
                    (cid, intermediate) in old_coverage
                    and node_roles.get((cid, intermediate)) == "user"
                    and pos[ai_id] < index < pos[user_id]
                    for intermediate, index in pos.items())
                if gap:
                    intervening_user_turns += 1
                latest_ai = max((index for intermediate, index in pos.items()
                                 if (cid, intermediate) in old_coverage
                                 and node_roles.get((cid, intermediate)) == "assistant"
                                 and index < pos[user_id]), default=-1)
                if latest_ai != pos[ai_id]:
                    prior_ai_not_latest_visible += 1
            if node_roles.get((cid, ai_id)) != "assistant":
                event_issue["assistant_pointer_invalid_role"] += 1
                event_ptr_errors.append(row["candidate_id"])
            elif ai_id not in pos or user_id not in pos or pos[ai_id] >= pos[user_id]:
                event_issue["assistant_pointer_not_prior_on_current_branch"] += 1
                event_ptr_errors.append(row["candidate_id"])
        elif row["interaction_context"] == "user_following_ai":
            event_issue["missing_prior_ai_pointer"] += 1
    overall["previous_phase2_metadata_pointers"] = len(old_coverage)
    overall["phase2_candidate_cues"] = len(old_events)
    overall["old_eligible_message_nodes_not_resolved"] = sum(
        item not in eligible_nodes for item in old_coverage)

    # Prespecified probability pilot: fixed n drawn from each original tier.
    pilot = {}
    for tier in STRATA:
        pop = [row for row in candidates if row["stratum"] == tier]
        pilot[tier] = stable_sample(pop, sample_n, seed, tier)
    # Enriched strata are qualitative QA, not random prevalence estimates.
    enrich = {}
    for tier in ("in_first_screen", "out_of_scope_screen"):
        pop = [row for row in candidates
               if row["needs_nontext_review"] and
               ((row["stratum"] != "out_of_scope_screen")
                == (tier == "in_first_screen"))]
        enrich[tier] = stable_sample(pop, multimodal_n, seed, "visual:" + tier)
    tagged = {}
    for tier, rows in pilot.items():
        for row in rows:
            tagged.setdefault(row["conversation_id"], (row, []))[1].append(
                "probability_pilot:" + tier)
    for tier, rows in enrich.items():
        for row in rows:
            tagged.setdefault(row["conversation_id"], (row, []))[1].append(
                "nontext_enrichment:" + tier)
    for row in candidates:
        if row["rescued_by_phase2_lexical_search"]:
            tagged.setdefault(row["conversation_id"], (row, []))[1].append(
                "lexical_rescue_census")
    review_rows = []
    for record, reasons in tagged.values():
        r = dict(record)
        r["selection_reasons"] = ";".join(sorted(reasons))
        review_rows.append(r)
    review_rows.sort(key=lambda x: (x["stratum"], x["conversation_id"]))
    private.mkdir(parents=True, exist_ok=True)
    public.mkdir(parents=True, exist_ok=True)
    write_csv(private / "review_pilot.csv", review_rows,
              [*candidates[0].keys(), "selection_reasons"])
    write_csv(private / "all_conversations_qc_index.csv", candidates,
              list(candidates[0]))
    write_csv(private / "source_file_digests.csv", file_digests,
              ["filename", "size_bytes", "sha256"])
    write_csv(private / "phase2_unresolved_event_pointers.csv",
              [{"candidate_id": identifier} for identifier in
               sorted(set(event_ptr_errors))], ["candidate_id"])

    aggregate = {
        "phase": "phase4_pre_coding_gate_not_intervention_coding",
        "input_files_manifest_size_verified": len(files),
        "conversation_count": overall["conversations"],
        "first_screened": len(screened),
        "not_first_screened": len(ids) - len(screened),
        "lexical_rescue_unadjudicated": len(rescue_ids),
        "first_pass_strata": {
            k: sum(x["stratum"] == k for x in candidates) for k in STRATA},
        "all_user_assistant_nodes_including_branches": overall[
            "all_user_assistant_nodes"],
        "mainline_user_assistant_nodes_including_nonvisible": overall[
            "mainline_user_assistant_nodes"],
        "user_multimodal_nodes_all_branches": overall["user_multimodal_nodes"],
        "user_multimodal_with_nontext_parts_all_branches": overall[
            "user_multimodal_with_nontext_parts"],
        "user_multimodal_without_text_all_branches": overall[
            "user_multimodal_without_text"],
        "attachment_metadata_references_all_branches": overall[
            "attachment_metadata_references"],
        "conversations_with_nontext_review_needed": sum(
            x["needs_nontext_review"] for x in candidates),
        "nontext_review_by_original_stratum": {
            tier: sum(x["needs_nontext_review"] and x["stratum"] == tier
                      for x in candidates) for tier in STRATA},
        "current_node_status_counts": dict(sorted(
            (key.removeprefix("structural_status:"), val)
            for key, val in overall.items()
            if key.startswith("structural_status:"))),
        "missing_root_parent_endpoints": overall["unlinked_root_terminus"],
        "old_phase2_candidate_cues_not_accepted_events": len(old_events),
        "phase2_source_pointer_issues": dict(event_issue),
        "candidate_cues_with_intervening_visible_user_turns": intervening_user_turns,
        "candidate_cues_with_nonlatest_visible_ai_pointer": prior_ai_not_latest_visible,
        "phase2_source_message_pointers_unresolved": overall[
            "old_eligible_message_nodes_not_resolved"],
        "sampling": {
            "seed": seed,
            "algorithm": "SHA256-ranking(seed, stratum, conversation_id)",
            "pilot_n_per_tier": sample_n,
            "probability_pilot_n": sum(len(x) for x in pilot.values()),
            "nontext_oversample_n_by_category": {
                k: len(v) for k, v in enrich.items()},
            "lexical_rescue_census_n": len(rescue_ids),
            "distinct_private_review_records": len(review_rows),
            "not_intervention_count": True,
        },
        "research_gate": "BLOCK_FINAL_INCLUSION_AND_ATTRIBUTION",
        "exposure_E5_inference": "NOT_PERMITTED_WITHOUT_ASSET_REVIEW",
        "artifact_attribution": "NOT_YET_VERIFIED",
        "limitations": [
            "Original records include multimodal components not interpreted here.",
            "Attachment metadata does not establish image or file contents.",
            "Heuristic inclusion is not adjudicated; pilot is not an exhaustive audit.",
            "Potential eligibility among unscreened threads is unquantified.",
            "Git provenance alone cannot establish intellectual or code authorship.",
            "Automated candidate cues are not steering-event outcomes.",
            "Private review records include source IDs, filenames and titles; "
            "do not publish.",
        ],
    }
    (public / "corpus_gate_aggregate.json").write_text(
        json.dumps(aggregate, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    return aggregate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--export-dir", type=Path, required=True)
    parser.add_argument("--phase1-screening", type=Path, required=True)
    parser.add_argument("--phase2-private", type=Path, required=True)
    parser.add_argument("--out-private", type=Path, required=True)
    parser.add_argument("--out-public", type=Path, required=True)
    parser.add_argument("--pilot-per-tier", type=int, default=25)
    parser.add_argument("--nontext-per-category", type=int, default=20)
    parser.add_argument("--seed", default="20261113")
    args = parser.parse_args()
    if args.pilot_per_tier < 1 or args.nontext_per_category < 0:
        parser.error("Sample sizes must be positive / nonnegative")
    result = build(args.export_dir, args.phase1_screening,
                   args.phase2_private, args.out_private,
                   args.out_public, args.pilot_per_tier,
                   args.nontext_per_category, args.seed)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
