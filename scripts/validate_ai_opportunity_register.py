"""Validate structural invariants of a private AI-proposal opportunity register.

Does not classify the science or read transcript text; accepts any CSV with
required fields. Intended for internal checks using public-safe code.
"""
import csv
from collections import Counter
from pathlib import Path

REQUIRED = ('opportunity_id', 'event_id', 'assistant_message_id',
            'user_message_id', 'next_user_disposition_pilot')

def validate(path):
    with Path(path).open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError('CSV must include header')
        missing = set(REQUIRED) - set(reader.fieldnames)
        if missing:
            raise ValueError('Missing columns: '+', '.join(sorted(missing)))
        rows = list(reader)
    seen = set()
    for row in rows:
        for field in REQUIRED:
            if not (row.get(field) or '').strip():
                raise ValueError('Empty '+field)
        if row['opportunity_id'] in seen:
            raise ValueError('Duplicate opportunity ID')
        seen.add(row['opportunity_id'])
    return {'opportunities':len(rows), 'linked_events':len(set(r['event_id'] for r in rows)),
            'dispositions':dict(Counter(r['next_user_disposition_pilot'] for r in rows))}

if __name__ == '__main__':
    import argparse,json
    parser=argparse.ArgumentParser()
    parser.add_argument('csv_path')
    print(json.dumps(validate(parser.parse_args().csv_path),indent=2))
