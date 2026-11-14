#!/usr/bin/env python3
"""Apply investigator's literal uppercase AREA exclusion, preserving prior labels.

The rule is post-protocol-freeze and is not a verified indicator of distinct
project membership. The resulting overlay is an auditable provisional scope
operation. All source-linked outputs are PRIVATE; do not commit them.
"""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

# Only the uppercase research acronym is an automatic trigger, not generic
# lowercase 'area', and only as an independent lexical token. '_' is a delimiter.
AREA = re.compile(r'(?<![A-Za-z])AREA(?![A-Za-z])')
LABELS = {'include', 'exclude', 'uncertain'}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def read_ledger(path):
    with path.open(newline='', encoding='utf-8-sig') as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        fields = reader.fieldnames
    required = {'conversation_id', 'created_utc', 'current_working_label',
                'adjudication_type', 'source_file_private', 'title_private'}
    if not fields or not required.issubset(fields):
        raise ValueError('Missing required private ledger fields')
    ids = [x['conversation_id'] for x in rows]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError('Empty or duplicated population')
    if any(x['current_working_label'] not in LABELS for x in rows):
        raise ValueError('Unexpected label')
    return rows, fields


def message_parts(conversation):
    """All mapped user/assistant messages, with mainline-vs-alt provenance."""
    mapping = conversation.get('mapping') or {}
    on_main = set()
    node = conversation.get('current_node')
    while node and node in mapping and node not in on_main:
        on_main.add(node)
        node = mapping[node].get('parent')
    for node_id, node_data in mapping.items():
        msg = node_data.get('message') or {}
        role = (msg.get('author') or {}).get('role')
        if role not in ('user', 'assistant'):
            continue
        parts = (msg.get('content') or {}).get('parts') or []
        if not isinstance(parts, list):
            continue
        for part in parts:
            if isinstance(part, str):
                yield role, 'mainline' if node_id in on_main else 'alternative', part


def locations(conversation):
    matches = []
    title = conversation.get('title') or ''
    for m in AREA.finditer(title):
        matches.append({'role': 'title', 'branch': 'mainline',
                        'context': title[max(0, m.start()-75):m.end()+90]})
    for role, branch, content in message_parts(conversation):
        for m in AREA.finditer(content):
            matches.append({'role': role, 'branch': branch,
                            'context': content[max(0, m.start()-75):m.end()+90].replace('\n', ' ')})
    return matches


def scan(rows, export_dir):
    """Only inspect conversation objects already in the in-scope ledger."""
    rows_by_id = {r['conversation_id']: r for r in rows}
    by_source = {}
    for row in rows:
        by_source.setdefault(row['source_file_private'], set()).add(row['conversation_id'])
    found = {}
    for source, ids in sorted(by_source.items()):
        path = export_dir / source
        if not path.is_file() or not path.name.startswith('conversations-'):
            raise ValueError('Missing or unexpected source shard: ' + source)
        shard = json.loads(path.read_text(encoding='utf-8'))
        for c in shard:
            cid = c.get('id') or c.get('conversation_id')
            if cid not in ids:
                continue  # Do not examine any out-of-scope conversation.
            if cid in found:
                raise ValueError('Duplicate conversation in source')
            found[cid] = locations(c)
    missing = set(rows_by_id) - set(found)
    if missing:
        raise ValueError('Missing in-scope source conversations')
    return found


def apply(rows, found, decision_date):
    new_rows = []
    changes = []
    for old in rows:
        cid = old['conversation_id']
        matches = found[cid]
        new = dict(old)
        new['pre_AREA_rule_working_label'] = old['current_working_label']
        new['pre_AREA_rule_adjudication_type'] = old['adjudication_type']
        new['AREA_literal_match'] = 'TRUE' if matches else 'FALSE'
        new['AREA_rule_action'] = 'EXCLUDED_BY_INVESTIGATOR_RULE' if matches else 'NO_CHANGE'
        new['AREA_exception_review'] = ''  # assigned only in private exception registry
        if matches:
            new['current_working_label'] = 'exclude'
            new['adjudication_type'] = 'INVESTIGATOR_AREA_LITERAL_SCOPE_RULE'
            changes.append({
                'conversation_id_PRIVATE': cid,
                'title_PRIVATE': old['title_private'],
                'source_file_PRIVATE': old['source_file_private'],
                'source_case_id_PRIVATE': old.get('source_case_id', ''),
                'decision_date': decision_date,
                'old_label': old['current_working_label'],
                'new_label': 'exclude',
                'old_adjudication_type': old['adjudication_type'],
                'new_adjudication_type': new['adjudication_type'],
                'source_match_count': len(matches),
                'source_roles': ';'.join(sorted({m['role'] for m in matches})),
                'source_branches': ';'.join(sorted({m['branch'] for m in matches})),
                'first_source_match_excerpt_PRIVATE': matches[0]['context'],
                'reason': 'Investigator-directed exclusion for uppercase standalone AREA; even if ROSMAP mentioned',
                'evidence_class': 'investigator_post_freeze_scope_rule_plus_literal_source_match',
                'exception_review_status': ''})
        new_rows.append(new)
    return new_rows, changes


def run(ledger, export_dir, outdir, date='2026-11-13', expected_size=None,
        expected_source_hashes=None):
    rows, fields = read_ledger(ledger)
    if expected_size is not None and len(rows) != expected_size:
        raise ValueError('Unexpected ledger population')
    if expected_source_hashes:
        hashes = json.loads(expected_source_hashes.read_text())['source_sha256']
        for source, digest in hashes.items():
            if sha256((export_dir/source).read_bytes()) != digest:
                raise ValueError('Source hash mismatch: ' + source)
    old_counts = Counter(r['current_working_label'] for r in rows)
    found = scan(rows, export_dir)
    new_rows, changes = apply(rows, found, date)
    new_counts = Counter(r['current_working_label'] for r in new_rows)
    if len(new_rows) != len(rows) or sum(new_counts.values()) != len(rows):
        raise AssertionError('Population changed')
    if any(r['pre_AREA_rule_working_label'] != prior['current_working_label']
           for r, prior in zip(new_rows, rows)):
        raise AssertionError('Original classification mutated')
    if any(r['current_working_label'] != prior['current_working_label']
           for r, prior in zip(new_rows, rows) if not found[r['conversation_id']]):
        raise AssertionError('Nonmatching label changed')
    outdir.mkdir(parents=True, exist_ok=True)
    effective = outdir / 'PHASE13_597_EFFECTIVE_AREA_RULE_PRIVATE.csv'
    cols = fields + ['pre_AREA_rule_working_label', 'pre_AREA_rule_adjudication_type',
                     'AREA_literal_match', 'AREA_rule_action', 'AREA_exception_review']
    with effective.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        writer.writerows(new_rows)
    overlay = outdir / 'PHASE13_AREA_EXCLUSION_OVERLAY_PRIVATE.csv'
    with overlay.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(changes[0]) if changes else [])
        if changes:
            writer.writeheader()
            writer.writerows(changes)
    result = {
        'decision_date': date,
        'scope': 'October 1 2025 onward; computational Hsp60/10-ROSMAP project',
        'rule': 'case-sensitive standalone uppercase AREA in conversation title or mapped user/assistant text',
        'all_message_branches_scanned': True,
        'total_conversations': len(rows),
        'source_ledger_sha256': sha256(ledger.read_bytes()),
        'original_counts': dict(sorted(old_counts.items())),
        'new_working_counts': dict(sorted(new_counts.items())),
        'matched_conversations': len(changes),
        'matched_prior_labels': dict(sorted(Counter(x['old_label'] for x in changes).items())),
        'changed_labels': sum(x['old_label'] != x['new_label'] for x in changes),
        'status': 'provisional investigator rule applied; exceptional false positives require review',
    }
    (outdir/'AGGREGATE_PRIVATE.json').write_text(json.dumps(result, indent=2)+'\n')
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ledger', type=Path, required=True)
    parser.add_argument('--export-dir', type=Path, required=True)
    parser.add_argument('--outdir', type=Path, required=True)
    parser.add_argument('--expected-size', type=int)
    parser.add_argument('--frozen-hash-ledger', type=Path)
    parser.add_argument('--decision-date', default='2026-11-13')
    args = parser.parse_args()
    result = run(args.ledger, args.export_dir, args.outdir,
                 args.decision_date, args.expected_size, args.frozen_hash_ledger)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
