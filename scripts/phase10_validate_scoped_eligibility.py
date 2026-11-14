#!/usr/bin/env python3
"""Validate a private conversation-date census and post-cutoff screening ledger.

No private data is written to stdout, committed files, or aggregate JSON.
This checks bookkeeping, date scope, uniqueness, and label accounting—not whether
any AI or investigator classification is scientifically correct.
"""
from __future__ import annotations
import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

CUTOFF_LOCAL = datetime(2025, 10, 1, tzinfo=ZoneInfo('America/Denver'))
VALID_LABELS = {'include', 'exclude', 'uncertain'}
VALID_PHASES = {'phase5', 'phase7', 'phase8', 'phase9', 'phase10'}


def rows_from_csv(path):
    with open(path, newline='', encoding='utf-8') as handle:
        yield from csv.DictReader(handle)


def aware_date(value):
    result = datetime.fromisoformat(value)
    if result.tzinfo is None:
        raise ValueError('Timestamp must have explicit timezone')
    return result


def summarize(census_rows, ledger_rows):
    census = {}
    boundary_crossings = 0
    minor_clock_skew = 0
    for item in census_rows:
        cid = item['conversation_id']
        if not cid or cid in census:
            raise ValueError('Missing/duplicate conversation ID in census')
        created = aware_date(item['created_utc'])
        last = aware_date(item['last_message_utc'])
        if last < created:
            if (created - last).total_seconds() > 5:
                raise ValueError('Last-message timestamp precedes creation by more than 5 seconds')
            minor_clock_skew += 1
        in_scope = created >= CUTOFF_LOCAL
        if int(item['in_scope']) != int(in_scope):
            raise ValueError('Census scope flag inconsistent with cutoff')
        if not in_scope and last >= CUTOFF_LOCAL:
            boundary_crossings += 1
        census[cid] = in_scope
    ledger = {}
    by_phase = Counter()
    counts = Counter()
    overlay = 0
    for item in ledger_rows:
        cid = item['conversation_id']
        if not cid or cid in ledger:
            raise ValueError('Missing/duplicate conversation ID in scoped ledger')
        if cid not in census or not census[cid]:
            raise ValueError('Ledger contains pre-cutoff or unknown conversation')
        if aware_date(item['created_utc']) < CUTOFF_LOCAL:
            raise ValueError('Ledger source date precedes cutoff')
        if item['current_working_label'] not in VALID_LABELS:
            raise ValueError('Unknown working eligibility label')
        if item['ai_original_label'] not in VALID_LABELS:
            raise ValueError('Unknown original eligibility label')
        if item['source_phase'] not in VALID_PHASES:
            raise ValueError('Unknown source phase')
        if item['adjudication_type'] not in {'INVESTIGATOR_OVERLAY', 'AI_PROVISIONAL'}:
            raise ValueError('Unrecognized adjudication status')
        if (item['adjudication_type'] == 'AI_PROVISIONAL'
                and item['ai_original_label'] != item['current_working_label']):
            raise ValueError('AI-only row silently changed its original label')
        overlay += item['adjudication_type'] == 'INVESTIGATOR_OVERLAY'
        ledger[cid] = item
        counts[item['current_working_label']] += 1
        by_phase[item['source_phase']] += 1
    scoped = {cid for cid, eligible in census.items() if eligible}
    if set(ledger) != scoped:
        raise ValueError('Scoped ledger is incomplete or includes unexpected cases')
    return {
        'original_export_conversations': len(census),
        'pre_cutoff_removed_from_primary_scope': len(census)-len(scoped),
        'post_cutoff_in_scope': len(scoped),
        'post_cutoff_provisionally_screened': len(ledger),
        'post_cutoff_unreviewed_after_phase10': len(scoped)-len(ledger),
        'pre_created_with_post_cutoff_messages': boundary_crossings,
        'census_last_message_minor_clock_skew_cases': minor_clock_skew,
        'post_cutoff_working_labels': dict(sorted(counts.items())),
        'phase_in_scope_count': dict(sorted(by_phase.items())),
        'investigator_overlay_cases_in_scope': overlay,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--census', required=True, type=Path,
                        help='Private metadata-only census CSV (never commit)')
    parser.add_argument('--ledger', required=True, type=Path,
                        help='Private date-scoped eligibility ledger (never commit)')
    parser.add_argument('--expected', type=Path,
                        help='Optional public aggregate JSON to verify')
    args = parser.parse_args()
    result = summarize(rows_from_csv(args.census), rows_from_csv(args.ledger))
    if args.expected:
        expected = json.loads(args.expected.read_text(encoding='utf-8'))
        for key, value in result.items():
            if key not in expected:
                if key == 'phase_in_scope_count':
                    actual = {k: v['post_cutoff'] for k,v in expected['phase_distribution'].items()}
                    if value != actual:
                        raise ValueError('Public phase distribution does not match private ledger')
                elif key == 'investigator_overlay_cases_in_scope':
                    if value != 3:
                        raise ValueError('Investigator overlay count mismatch')
                else:
                    raise ValueError('Public aggregate is missing ' + key)
            elif expected[key] != value:
                raise ValueError('Public aggregate does not match private ledger: ' + key)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
