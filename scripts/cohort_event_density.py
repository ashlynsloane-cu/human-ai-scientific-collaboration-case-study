"""Describe event density by *conversation-opening cohort*, not event timestamp.

Inputs are sanitized, explicitly approved CSVs. Do not commit source transcripts or
participant-level biological data. The event register may be provisional/incomplete.
"""
from __future__ import annotations
import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path


def summarize(events, turns):
    """Return group summaries. Events have IDs and conversation IDs; turns have IDs.

    The ``created_utc`` column refers to when the *conversation* was created.
    This is not a message-level timestamp. Events are not independent trials.
    """
    conversations = {}
    unique_turns = set()
    counts = Counter()
    for turn in turns:
        tid = turn['message_id']
        cid = turn['conversation_id']
        month = turn['created_utc'][:7]
        if tid in unique_turns:
            raise ValueError('Duplicate user message ID')
        unique_turns.add(tid)
        if cid in conversations and conversations[cid] != month:
            raise ValueError('Inconsistent conversation opening date')
        conversations[cid] = month
        counts[month] += 1
    event_ids = set()
    by_month = Counter()
    for event in events:
        eid = event['event_id']
        cid = event['conversation_id']
        if eid in event_ids:
            raise ValueError('Duplicate contribution event ID')
        if cid not in conversations:
            raise ValueError('Event references conversation missing from turns')
        event_ids.add(eid)
        by_month[conversations[cid]] += 1
    return [dict(conversation_start_month=m, user_turns=counts[m],
                 provisional_events=by_month[m],
                 events_per_100_user_turns=round(100*by_month[m]/counts[m], 2))
            for m in sorted(counts)]


def read_csv(path):
    with open(path, encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--event-csv', type=Path, required=True)
    ap.add_argument('--user-turn-csv', type=Path, required=True)
    ap.add_argument('--output-csv', type=Path, required=True)
    args = ap.parse_args()
    records = summarize(read_csv(args.event_csv), read_csv(args.user_turn_csv))
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open('w', newline='', encoding='utf-8') as out:
        writer = csv.DictWriter(out, fieldnames=['conversation_start_month',
                              'user_turns','provisional_events','events_per_100_user_turns'])
        writer.writeheader()
        writer.writerows(records)

if __name__ == '__main__':
    main()
