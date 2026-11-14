"""Validate private Phase 25 pilot coverage without publishing private data.

Uses CSV files in a private directory provided explicitly at runtime.
The categorization is a first-pass work queue, NOT an event-frequency estimate.
"""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def validate_inventory(message_rows, user_rows, expect_cases=15,
                       expect_messages=1031, expect_user=464):
    if len(message_rows) != expect_messages:
        raise ValueError('Message count inconsistent with frozen pilot')
    if len(user_rows) != expect_user:
        raise ValueError('User turn count inconsistent with frozen pilot')
    if len({r['message_id'] for r in message_rows}) != len(message_rows):
        raise ValueError('Duplicate message ID')
    if len({(r['case_id'], r['message_seq']) for r in message_rows}) != len(message_rows):
        raise ValueError('Duplicate case/sequence pair')
    case_set = {r['case_id'] for r in message_rows}
    if len(case_set) != expect_cases:
        raise ValueError('Wrong number of pilot conversations')
    roles = Counter(r['role'] for r in message_rows)
    if roles['user'] != expect_user or roles['assistant'] != expect_messages-expect_user:
        raise ValueError('Role counts do not reconcile')
    by_id={r['message_id']:r for r in message_rows}
    seen=set()
    for t in user_rows:
        k=t['user_message_id']
        if k in seen:
            raise ValueError('Duplicate user-turn ID')
        seen.add(k)
        if k not in by_id or by_id[k]['role'] != 'user':
            raise ValueError('User turn not linked to user message')
        if by_id[k]['case_id'] != t['case_id']:
            raise ValueError('Case pointer mismatch')
        if by_id[k]['message_seq'] != t['seq']:
            raise ValueError('Message sequence mismatch')
        if by_id[k]['text_sha256'] != t['user_text_sha256']:
            raise ValueError('Text fingerprint mismatch')
        if t['primary_steering_type'] != 'NOT_ADJUDICATED':
            raise ValueError('First-pass label illegally presented as adjudicated event')
    if seen != {r['message_id'] for r in message_rows if r['role']=='user'}:
        raise ValueError('Missing user-turn record')
    return {'pilot_conversations':len(case_set),'messages':len(message_rows),
            'user_turns':len(user_rows),'assistant_messages':roles['assistant'],
            'primary_outcome_adjudicated':False}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('private_directory', type=Path)
    a=parser.parse_args()
    p=a.private_directory
    result=validate_inventory(read_csv(p/'PHASE25_ALL_1031_MESSAGE_COVERAGE_PRIVATE.csv'),
        read_csv(p/'PHASE25_ALL_464_USER_TURN_TRIAGE_PRIVATE.csv'))
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
