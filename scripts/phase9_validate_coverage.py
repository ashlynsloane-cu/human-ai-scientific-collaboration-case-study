#!/usr/bin/env python3
"""Validate Phase 9 private eligibility screening without publishing source records.

Standard-library only. Source excerpt AI labels are *provisional*, not scientific ground truth.
No case titles, conversation IDs, excerpts, paths, or source hashes are serialized to public output.
"""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path

PART_HIGH = 'HIGH_CONTEXT_RANK'
PART_LOW = 'LOW_RANK_PROBABILITY_AUDIT'
LOW_SEED = 'hsp60-p9-lowrank-qc-20261113'
LABELS = {'include', 'exclude', 'uncertain'}
PUBLIC_FIELDS = {
    'phase', 'record_kind', 'export_total', 'previous_reviewed',
    'remaining_at_phase_start', 'new_source_excerpt_assessed',
    'new_high_ranked_conversations', 'new_lower_rank_probability_review',
    'new_provisional_labels', 'new_provisional_by_partition',
    'working_total_distinct_assessed', 'still_without_source_excerpt_assessment',
    'cumulative_provisional_labels_with_previous_investigator_overlay',
    'remaining_608_full_text_indexed_for_retrieval',
    'remaining_608_nontext_flagged', 'remaining_608_no_user_text',
    'new_200_nontext_flagged',
    'remaining_608_asset_text_payloads_assessed', 'single_ai_reviewer',
    'new_independent_human_reviews', 'no_new_confirmed_inclusion_from_200_excerpt_based_reviews',
    'no_corpus_freeze_or_recall_estimate', 'original_frozen_protocol_unchanged',
    'selection_bias_warning', 'confound_warning',
}


def read_csv(path):
    with open(path, newline='', encoding='utf-8') as stream:
        return list(csv.DictReader(stream))


def verify_unique(rows, key):
    values = [row[key] for row in rows]
    if len(values) != len(set(values)):
        raise ValueError(f'duplicate {key}')


def expected_selection(remainder):
    """Fixed selection independent of AI labels or desired outcomes."""
    verify_unique(remainder, 'conversation_id')
    ordered = sorted(
        remainder,
        key=lambda row: (-float(row['priority_score']), row['conversation_id']),
    )
    high = ordered[:120]
    low = sorted(
        ordered[120:],
        key=lambda row: hashlib.sha256(
            (LOW_SEED + '|' + row['conversation_id']).encode('utf-8')
        ).hexdigest(),
    )[:80]
    return {row['conversation_id']: (PART_HIGH, i + 1)
            for i, row in enumerate(high)} | {
            row['conversation_id']: (PART_LOW, i + 1)
            for i, row in enumerate(low)
    }


def validate_selection(ledger, remainder):
    if len(remainder) != 608 or len(ledger) != 200:
        raise ValueError('Expected 608 source-indexed and 200 selected conversations')
    selection = expected_selection(remainder)
    verify_unique(ledger, 'conversation_id')
    if set(selection) != {row['conversation_id'] for row in ledger}:
        raise ValueError('Review selection differs from frozen pre-label ranking/sample')
    for row in ledger:
        partition, order = selection[row['conversation_id']]
        if row['selection_partition'] != partition or int(row['selection_order']) != order:
            raise ValueError('Review partition/order mismatch')
        if row['ai_provisional_label'] not in LABELS:
            raise ValueError('Invalid provisional eligibility label')
        if not row['ai_source_context_rationale'].strip():
            raise ValueError('Missing source-specific rationale')
        if row['reviewer'] != 'SINGLE_AI_PROVISIONAL':
            raise ValueError('Cannot represent a model review as independent adjudication')
        if row['human_blind_label'].strip() or row['final_adjudicated_label'].strip():
            raise ValueError('Cannot overwrite or invent unperformed human adjudication')
        if row['source_excerpts_reviewed'] != 'SELECTED_USER_MESSAGE_EXCERPTS_NOT_FULL_CONVERSATION':
            raise ValueError('Review coverage status was altered')
    return True


def source_user_parts(conversation):
    mapping = conversation['mapping']
    parent = conversation['current_node']
    seen = set()
    chain = []
    while parent and parent in mapping:
        if parent in seen:
            raise ValueError('Conversation parent cycle')
        seen.add(parent)
        chain.append(mapping[parent])
        parent = mapping[parent]['parent']
    chain.reverse()
    turns = []
    for node in chain:
        msg = node.get('message') or {}
        if (msg.get('author') or {}).get('role') != 'user':
            continue
        parts = (msg.get('content') or {}).get('parts') or []
        text = '\n'.join(p for p in parts if isinstance(p, str)).strip()
        if text:
            turns.append((node['id'], text))
    return turns


def verify_sources(ledger, export_dir, source_digests):
    root = Path(export_dir)
    source_map = {row['filename']: row for row in read_csv(source_digests)}
    source_files = sorted(root.glob('conversations-*.json'))
    if len(source_files) != 11 or set(source_map) != {p.name for p in source_files}:
        raise ValueError('Source shard coverage differs from frozen export')
    byfile = {}
    for file in source_files:
        contents = file.read_bytes()
        if len(contents) != int(source_map[file.name]['size_bytes']):
            raise ValueError('Source file size drift')
        if hashlib.sha256(contents).hexdigest() != source_map[file.name]['sha256']:
            raise ValueError('Source file hash drift')
        byfile[file.name] = {
            c['id']: c for c in json.loads(contents.decode('utf-8'))
        }
    for row in ledger:
        c = byfile[row['source_file_private']][row['conversation_id']]
        turns = source_user_parts(c)
        lookup = dict(turns)
        node = row['source_user_node_id']
        if node not in lookup:
            raise ValueError('Evidence user node not in mainline text')
        if hashlib.sha256(lookup[node].encode()).hexdigest() != row['user_message_sha256']:
            raise ValueError('Evidence user message fingerprint mismatch')
        all_text = '\n'.join(text for _, text in turns)
        if hashlib.sha256(all_text.encode()).hexdigest() != row['entire_user_text_sha256']:
            raise ValueError('Full user text fingerprint mismatch')
    return {'source_shards_verified': len(source_files), 'evidence_nodes_verified': len(ledger)}


def aggregate(ledger, prior, remaining=None):
    current = Counter(row['ai_provisional_label'] for row in ledger)
    remaining = remaining or []
    # Counts here reflect incomplete non-text coverage; never exposure class absence.
    remaining_nontext = sum(r.get('nontext_unassessed') == 'True' for r in remaining)
    remaining_no_user = sum(r.get('source_user_count') == '0' for r in remaining)
    reviewed_nontext = sum(r.get('nontext_assessment') == 'UNASSESSED' for r in ledger)
    prior_labels = prior['working_total_ai_labels_including_investigator_phase5_overlay']
    if prior['total_distinct_with_ai_review'] != 441:
        raise ValueError('Prior phase count changed')
    if sum(prior_labels.values()) != 441:
        raise ValueError('Prior phase labels inconsistent')
    total = Counter(prior_labels) + current
    by_part = {p: dict(sorted(Counter(
        row['ai_provisional_label'] for row in ledger
        if row['selection_partition'] == p).items())) for p in (PART_HIGH, PART_LOW)}
    out = {
        'phase': '9',
        'record_kind': 'source_excerpt_ai_first_pass_not_final',
        'export_total': 1049,
        'previous_reviewed': 441,
        'remaining_at_phase_start': 608,
        'new_source_excerpt_assessed': 200,
        'new_high_ranked_conversations': 120,
        'new_lower_rank_probability_review': 80,
        'new_provisional_labels': dict(sorted(current.items())),
        'new_provisional_by_partition': by_part,
        'working_total_distinct_assessed': 641,
        'still_without_source_excerpt_assessment': 408,
        'cumulative_provisional_labels_with_previous_investigator_overlay': dict(sorted(total.items())),
        'remaining_608_full_text_indexed_for_retrieval': True,
        'remaining_608_nontext_flagged': remaining_nontext,
        'remaining_608_no_user_text': remaining_no_user,
        'new_200_nontext_flagged': reviewed_nontext,
        'remaining_608_asset_text_payloads_assessed': False,
        'single_ai_reviewer': True,
        'new_independent_human_reviews': 0,
        'no_new_confirmed_inclusion_from_200_excerpt_based_reviews': True,
        'no_corpus_freeze_or_recall_estimate': True,
        'original_frozen_protocol_unchanged': True,
        'selection_bias_warning': (
            'HIGH_CONTEXT_RANK is enriched. LOW_RANK_PROBABILITY_AUDIT samples only '
            'the lower-ranked 488, not the full 608. Both sets require human validation '
            'before inference.'
        ),
        'confound_warning': (
            'The original screen is known to miss some project material. Generic lab/figure/'
            'paper conversations stay UNCERTAIN when source linkage cannot be established.'
        ),
    }
    if sum(total.values()) != 641:
        raise ValueError('Cumulative count does not partition reviewed corpus')
    if set(out) != PUBLIC_FIELDS:
        raise ValueError('Public output fields differ from allowlist')
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--private-ledger', required=True, type=Path)
    parser.add_argument('--remaining-index', required=True, type=Path)
    parser.add_argument('--prior-aggregate', required=True, type=Path)
    parser.add_argument('--source-dir', type=Path)
    parser.add_argument('--source-digests', type=Path)
    parser.add_argument('--public-output', required=True, type=Path)
    args = parser.parse_args()
    ledger, remaining = read_csv(args.private_ledger), read_csv(args.remaining_index)
    validate_selection(ledger, remaining)
    if bool(args.source_dir) != bool(args.source_digests):
        parser.error('Specify both --source-dir and --source-digests to verify original bytes')
    if args.source_dir:
        verify_sources(ledger, args.source_dir, args.source_digests)
    report = aggregate(ledger, json.loads(args.prior_aggregate.read_text()), remaining)
    args.public_output.parent.mkdir(parents=True, exist_ok=True)
    args.public_output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print('Passed: 200 review records, fixed partitions, source rules, public minimization')
    if args.source_dir:
        print('Passed: 11 export shards and 200 user evidence nodes verified')


if __name__ == '__main__':
    main()
