#!/usr/bin/env python3
"""Aggregate a *private* first-pass eligibility ledger into publication-safe counts.

Usage:
 python3 scripts/phase5_adjudication_summary.py \
   --private-ledger /outside-repository/pilot_eligibility_first_pass.csv \
   --out results/phase5/eligibility_first_pass_aggregate.json

No private IDs, conversation titles, excerpts, or filenames from the source ledger
are copied to public output. First-pass labels are NOT independent human coding.
"""
import argparse
import csv
import json
from pathlib import Path

STRATA = (
    'A_core_evidence', 'B_context_review',
    'C_weak_or_ai_only', 'out_of_scope_screen',
)
DECISIONS = ('include', 'exclude', 'uncertain')
EXPECTED_SAMPLE = 25
EXPECTED_RESCUES = 5


def read_ledger(path):
    with Path(path).open(encoding='utf-8', newline='') as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        raise ValueError('Empty eligibility ledger')
    needed = {
        'conversation_id', 'decision', 'original_stratum',
        'selection_reasons', 'evidence_node_id', 'individualized_reason',
        'independent_confirmation', 'coding_status',
    }
    missing = sorted(needed - set(rows[0]))
    if missing:
        raise ValueError('Required ledger columns missing: '+', '.join(missing))
    ids = [r['conversation_id'] for r in rows]
    if len(set(ids)) != len(ids) or not all(ids):
        raise ValueError('Missing or duplicate source IDs in private ledger')
    if any(r['original_stratum'] not in STRATA for r in rows):
        raise ValueError('Unrecognized screening stratum')
    if any(r['decision'] not in DECISIONS for r in rows):
        raise ValueError('Invalid eligibility decision')
    if any(not r['evidence_node_id'] or not r['individualized_reason']
           for r in rows):
        raise ValueError('Decision without source pointer or rationale')
    if any(r['coding_status'] != 'PROVISIONAL_SOURCE_TEXT_SCREEN'
           or r['independent_confirmation'] != 'PENDING' for r in rows):
        raise ValueError('Expected nonindependent provisional first-pass data')
    return rows


def count(rows):
    return {v: sum(row['decision'] == v for row in rows)
            for v in DECISIONS}


def summarize(rows, require_design=True):
    # Reject untraceable sampling metadata before checking stratum quotas.
    if any('probability_pilot:' not in r['selection_reasons']
           and 'nontext_enrichment:' not in r['selection_reasons']
           and 'lexical_rescue_census' not in r['selection_reasons']
           for r in rows):
        raise ValueError('Review record has no known selection reason')
    strata = {}
    pilot = {}
    for stratum in STRATA:
        group = [row for row in rows if row['original_stratum']==stratum]
        strata[stratum] = {'n':len(group), 'decisions':count(group)}
        prob = [r for r in group if 'probability_pilot:' in r['selection_reasons']]
        if require_design and len(prob) != EXPECTED_SAMPLE:
            raise ValueError('Probability-pilot stratum size mismatch')
        pilot[stratum] = {'n':len(prob),'decisions':count(prob)}
    rescues = [r for r in rows if 'lexical_rescue_census' in r['selection_reasons']]
    if require_design and len(rescues)!=EXPECTED_RESCUES:
        raise ValueError('Lexical rescue count mismatch')
    results={
       'phase':'phase5_first_pass_corpus_eligibility',
       'status':'PROVISIONAL_NOT_DOUBLE_CODED',
       'basis':'single-reviewer source-text/context screening; media and alternate branches not comprehensively adjudicated',
       'total_distinct_reviewed':len(rows),
       'overall_decisions':count(rows),
       'original_screen_strata':strata,
       'probability_pilot_only':pilot,
       'enriched_review_set_not_representative':True,
       'lexical_rescue_census':{'n':len(rescues),'decisions':count(rescues)},
       'missed_inclusion_confirmed_in_probability_out_of_scope_sample':
             pilot['out_of_scope_screen']['decisions']['include']>0,
       'uncertainty_policy':'Unresolved project identity or inaccessible asset is uncertain, not imputed include/exclude',
       'exposure_E0_E5':'UNASSESSED; cannot claim absence of E5',
       'event_coding':'NOT_STARTED',
       'artifact_propagation':'NOT_ESTABLISHED',
       'independent_second_coder':'REQUIRED',
       'full_corpus_recall':'NOT_ESTABLISHED',
       'source_identifiers_published':False,
    }
    return results


def canonical_json(result):
    return json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False)+'\n'


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--private-ledger',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    rows=read_ledger(args.private_ledger)
    contents=canonical_json(summarize(rows))
    # Defensive: don't inadvertently leak user-specific metadata in JSON.
    for r in rows:
        for field in ('conversation_id','conversation_title_private',
                      'evidence_node_id','evidence_quote_private'):
            private=r.get(field,'')
            if private and private in contents:
                raise ValueError('Private value found in aggregate output')
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(contents,encoding='utf-8')
    print(f'Wrote aggregate QC report ({len(rows)} review records); no private IDs exported.')


if __name__=='__main__':
    main()
