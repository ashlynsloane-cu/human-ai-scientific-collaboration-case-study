#!/usr/bin/env python3
"""Verify Phase 8 private eligibility review provenance; publish aggregate data only.

This tool checks structure and traceability, NOT adjudication accuracy or recall.
No conversation text, IDs, filenames, dates, or reviewer rationales are written
into the public summary. Requires private locally held inputs and export shards.
"""

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ALLOWED_LABELS = {'include', 'exclude', 'uncertain'}
FIRST_SCREENED = {'A_core_evidence', 'B_context_review', 'C_weak_or_ai_only'}


def csv_rows(path):
    with open(path, newline='', encoding='utf-8') as stream:
        return list(csv.DictReader(stream))


def validate_sha_manifest(shard_dir, manifest):
    rows = csv_rows(manifest)
    if len(rows) != 11:
        raise ValueError('expected 11 SHA-256-locked export shards')
    files = set()
    for row in rows:
        name = row['filename']
        if name in files or '/' in name or '\\' in name:
            raise ValueError('duplicate or unsafe shard name')
        files.add(name)
        data = (Path(shard_dir) / name).read_bytes()
        if len(data) != int(row['size_bytes']):
            raise ValueError('export shard byte count mismatch')
        if hashlib.sha256(data).hexdigest() != row['sha256']:
            raise ValueError('export shard SHA-256 mismatch')
    return sorted(files)


def current_branch_nodes(conversation):
    mapping = conversation['mapping']
    node = conversation['current_node']
    seen = set()
    result = []
    while node and node in mapping:
        if node in seen:
            raise ValueError('conversation branch cycle')
        seen.add(node)
        result.append(mapping[node])
        node = mapping[node].get('parent')
    result.reverse()
    return result


def verify_user_evidence(conversation, case):
    nodes = current_branch_nodes(conversation)
    users = [n for n in nodes if (n.get('message') or {}).get('author', {}).get('role') == 'user'
             and any(isinstance(p, str) and p.strip() for p in
                     ((n.get('message') or {}).get('content') or {}).get('parts', []))]
    if not users:
        raise ValueError('conversation lacks user text on current branch')
    first = users[0]
    if first['id'] != case['source_node_id']:
        raise ValueError('evidence does not reference first current-branch user node')
    parts = (first['message'].get('content') or {}).get('parts') or []
    text = '\n'.join(p for p in parts if isinstance(p, str))
    if hashlib.sha256(text.encode()).hexdigest() != case['source_first_user_sha256']:
        raise ValueError('evidence content SHA-256 mismatch')
    return True


def verify_records(new_records, pilot_records, phase7_records, probability_records,
                   conversations):
    ids = [r['conversation_id'] for r in new_records]
    if len(ids) != len(set(ids)):
        raise ValueError('duplicate Phase 8 conversation IDs')
    previous = {r['conversation_id'] for r in pilot_records}
    previous7 = {r['conversation_id'] for r in phase7_records}
    if previous & previous7:
        raise ValueError('pilot and Phase 7 source overlap')
    if (previous | previous7) & set(ids):
        raise ValueError('Phase 8 double-counts earlier case')
    if len(previous) != len(pilot_records) or len(previous7) != len(phase7_records):
        raise ValueError('earlier review contains duplicate source IDs')
    sample = {r['conversation_id'] for r in probability_records}
    if len(sample) != len(probability_records):
        raise ValueError('probability sample repeats conversations')
    if len(sample & previous) != 0:
        raise ValueError('unexpected Phase 5 / probability-sample overlap')
    if len(sample - set(ids) - previous7) != 0:
        raise ValueError('probability audit has a missing classification')
    if not len(new_records):
        raise ValueError('empty Phase 8 ledger')
    for case in new_records:
        if case['phase8_ai_provisional_label'] not in ALLOWED_LABELS:
            raise ValueError('invalid eligibility label')
        if case['decision_status'] != 'NEW_PHASE8_AI_PROVISIONAL':
            raise ValueError('unlocked or adjudicated label in new ledger')
        if case['human_label'] or case['final_label']:
            raise ValueError('human or final label must not be synthesized')
        if case['nontext_assessment'] != 'NOT_ASSESSED':
            raise ValueError('unsupported nontext assessment')
        if case['conversation_id'] not in conversations:
            raise ValueError('conversation source not found')
        verify_user_evidence(conversations[case['conversation_id']], case)
    return True


def verify_investigator_overlay(pilot_records, investigator_overlay):
    pilot_by_id = {r['conversation_id']: r for r in pilot_records}
    if len(pilot_by_id) != len(pilot_records):
        raise ValueError('duplicate pilot conversation')
    seen = set()
    for r in investigator_overlay:
        identifier = r['conversation_id']
        if identifier in seen or identifier not in pilot_by_id:
            raise ValueError('investigator overlay has duplicate or unknown source')
        seen.add(identifier)
        if r['locked_ai_label'] != pilot_by_id[identifier]['decision']:
            raise ValueError('investigator overlay changed initial AI classification')
        if r['pilot_record_no'] != pilot_by_id[identifier]['record_no']:
            raise ValueError('investigator overlay points to wrong pilot record')
        if r['evidence_quote_sha256'] != pilot_by_id[identifier]['evidence_quote_sha256']:
            raise ValueError('investigator overlay source fingerprint mismatch')
        if r['final_label'] not in ALLOWED_LABELS:
            raise ValueError('invalid investigator decision')
    return True


def aggregate(new_records, pilot_records, phase7_records, probability_records,
              investigator_overlay):
    overlay = {r['conversation_id']: r['final_label'].lower() for r in investigator_overlay}
    pilot = Counter(overlay.get(r['conversation_id'], r['decision']) for r in pilot_records)
    prior7 = Counter(r['ai_first_pass_label'] for r in phase7_records)
    new = Counter(r['phase8_ai_provisional_label'] for r in new_records)
    total = pilot + prior7 + new
    prob_set = {r['conversation_id'] for r in probability_records}
    new_sample = Counter(r['phase8_ai_provisional_label'] for r in new_records
                         if r['conversation_id'] in prob_set)
    old_sample = Counter(r['ai_first_pass_label'] for r in phase7_records
                         if r['conversation_id'] in prob_set)
    screened = sum(r['original_stratum'] in FIRST_SCREENED for r in pilot_records)
    screened += sum(r['selection_group'] in FIRST_SCREENED for r in phase7_records)
    screened += sum(r['original_stratum'] in FIRST_SCREENED for r in new_records)
    return {
        'phase': 'phase8_source_context_expanded_eligibility',
        'reviewer': 'SINGLE_AI_PROVISIONAL_NOT_INDEPENDENT',
        'total_export_conversations': 1049,
        'previous_phase5_pilot_reviewed': len(pilot_records),
        'previous_phase7_reviewed': len(phase7_records),
        'new_this_phase': len(new_records),
        'new_reviewed_originally_screened': sum(
            r['original_stratum'] in FIRST_SCREENED for r in new_records),
        'new_reviewed_phase6_unscreened_probability': sum(
            r['conversation_id'] in prob_set for r in new_records),
        'probability_sample_overlap_carried_forward_from_phase7': sum(
            r['conversation_id'] in prob_set for r in phase7_records),
        'total_distinct_with_ai_review': sum(total.values()),
        'remaining_without_ai_source_context_review': 1049 - sum(total.values()),
        'initially_screened_total_reviewed': screened,
        'new_ai_labels': dict(sorted(new.items())),
        'working_total_ai_labels_including_investigator_phase5_overlay':
            dict(sorted(total.items())),
        'phase6_unscreened_probability_sample_provisional_ai_labels':
            dict(sorted((new_sample + old_sample).items())),
        'independent_phase8_human_reviews': 0,
        'corpus_frozen': False,
        'eligibility_error_rates_estimated': False,
        'all_nontext_reviewed': False,
        'alternate_branches_exhaustively_reviewed': False,
        'provisional_labels_not_final_or_recall_estimates': True,
    }


def run(args):
    filenames = validate_sha_manifest(args.export_dir, args.shard_digest_csv)
    new = csv_rows(args.new_private_ledger)
    pilot = csv_rows(args.pilot_private_ledger)
    p7 = csv_rows(args.phase7_private_ledger)
    prob = csv_rows(args.probability_private_sample)
    overlay = csv_rows(args.private_investigator_overlay)
    needed = {r['conversation_id'] for r in new}
    conversations = {}
    all_ids = set()
    for name in filenames:
        for c in json.loads((Path(args.export_dir) / name).read_text()):
            if c['id'] in all_ids:
                raise ValueError('duplicate conversation in export shards')
            all_ids.add(c['id'])
            if c['id'] in needed:
                conversations[c['id']] = c
    if len(all_ids) != 1049:
        raise ValueError('source export does not contain expected 1049 distinct conversations')
    verify_records(new, pilot, p7, prob, conversations)
    verify_investigator_overlay(pilot, overlay)
    result = aggregate(new, pilot, p7, prob, overlay)
    Path(args.public_aggregate_out).write_text(
        json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('export_dir', 'shard_digest_csv', 'new_private_ledger',
                 'pilot_private_ledger', 'phase7_private_ledger',
                 'probability_private_sample', 'private_investigator_overlay',
                 'public_aggregate_out'):
        parser.add_argument('--' + name.replace('_', '-'), required=True)
    result = run(parser.parse_args())
    print('PASS: traced', result['new_this_phase'], 'new cases; public aggregate only')


if __name__ == '__main__':
    main()
