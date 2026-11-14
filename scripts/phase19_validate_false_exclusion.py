"""Phase 19: independently replay private human corrections and validate review design.

Input row schemas must include conversation_id, phase18_effective_label and,
for overlay records, conversation_id, phase18_label, phase19_label, rationale.
This public module contains no actual private IDs or conversation labels.
"""
import argparse
import collections
import csv
import json
import random
from pathlib import Path

LABELS = {'include', 'exclude', 'uncertain'}


def load_csv(path):
    with open(path, encoding='utf-8', newline='') as source:
        return list(csv.DictReader(source))


def validate_and_apply(base, corrections, expected_n=None):
    """Return an unmodified original baseline and add-only phase19 overlay."""
    if expected_n is not None and len(base) != expected_n:
        raise ValueError('Unexpected population size')
    by_id = {}
    for row in base:
        key = row.get('conversation_id')
        label = row.get('phase18_effective_label')
        if not key or key in by_id:
            raise ValueError('Missing or duplicated base conversation ID')
        if label not in LABELS:
            raise ValueError('Unrecognized base label')
        by_id[key] = row
    applied = {}
    for correction in corrections:
        key = correction.get('conversation_id')
        if key not in by_id or key in applied:
            raise ValueError('Unknown or repeated overlay conversation ID')
        before = correction.get('phase18_label')
        after = correction.get('phase19_label')
        if before not in LABELS or after not in LABELS:
            raise ValueError('Unrecognized overlay label')
        if by_id[key]['phase18_effective_label'] != before:
            raise ValueError('Baseline / overlay mismatch')
        if not correction.get('rationale', '').strip():
            raise ValueError('Overlay must have rationale')
        if before == after:
            raise ValueError('No-op correction')
        applied[key] = after
    counts = collections.Counter(
        applied.get(key, row['phase18_effective_label'])
        for key, row in by_id.items()
    )
    return {'population': len(base), 'corrections': len(applied),
            'after': {k: counts.get(k, 0) for k in sorted(LABELS)}}


def validate_sample(sample, base, n_negative, n_positive):
    """Validate locked selection provenance without exposing sample identities."""
    base_map = {r['conversation_id']: r for r in base}
    seen = set()
    counts = collections.Counter()
    for item in sample:
        cid = item.get('conversation_id')
        rid = item.get('review_case_id')
        if cid not in base_map or cid in seen or not rid:
            raise ValueError('Duplicate/invalid sample record')
        seen.add(cid)
        outcome = item.get('prior_label')
        if base_map[cid].get('phase19_effective_label') != outcome:
            raise ValueError('Locked sample-label mismatch')
        if item.get('sampling_type') not in ('probability', 'included_control'):
            continue
        counts[outcome] += 1
    if counts['exclude'] != n_negative or counts['include'] != n_positive:
        raise ValueError('Unexpected locked sample allocation')
    return dict(counts)


def reconstruct_randomized_ids(base, n_negative=60, n_positive=10, seed=20261114):
    """Replay the private, concealed-label sample order deterministically."""
    by_label = collections.defaultdict(list)
    for row in base:
        label = row.get('phase19_effective_label')
        if label not in LABELS:
            raise ValueError('Missing effective label in sampling frame')
        by_label[label].append(row['conversation_id'])
    if n_negative > len(by_label['exclude']) or n_positive > len(by_label['include']):
        raise ValueError('Sample size exceeds its source population')
    rng = random.Random(seed)
    neg = rng.sample(sorted(by_label['exclude']), n_negative)
    pos = rng.sample(sorted(by_label['include']), n_positive)
    mixed = neg + pos
    rng.shuffle(mixed)
    return mixed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', required=True)
    parser.add_argument('--overlay', required=True)
    parser.add_argument('--expected-n', type=int, default=597)
    parser.add_argument('--output')
    args = parser.parse_args()
    answer = validate_and_apply(load_csv(args.baseline),
                                load_csv(args.overlay), args.expected_n)
    payload = json.dumps(answer, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(payload + '\n', encoding='utf-8')
    else:
        print(payload)


if __name__ == '__main__':
    main()
