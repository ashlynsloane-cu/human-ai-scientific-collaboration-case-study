"""Phase 20 reproducibility checks. Private inputs are not committed."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from math import comb

VALID = {'include', 'exclude', 'uncertain'}


def verify_population(rows, expected_n=597):
    if len(rows) != expected_n:
        raise ValueError('Population size mismatch')
    ids = [r['conversation_id'] for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate conversation')
    labels = [r['phase20_effective_label'] for r in rows]
    if any(x not in VALID for x in labels):
        raise ValueError('Unknown label')
    return dict(Counter(labels))


def validate_review(cases, final_decisions):
    ids = [c['review_case_id'] for c in cases]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate case')
    if set(ids) != set(final_decisions):
        raise ValueError('Case decision mismatch')
    if any(v not in ('INCLUDE', 'EXCLUDE') for v in final_decisions.values()):
        raise ValueError('Unresolved final decisions')
    if Counter(c['sampling_type'] for c in cases) != {
        'probability': 60, 'included_control': 10, 'purposive_targeted': 7
    }:
        raise ValueError('Sample design mismatch')
    result = {}
    for t in ('probability', 'included_control', 'purposive_targeted'):
        result[t] = dict(Counter(final_decisions[c['review_case_id']]
                                 for c in cases if c['sampling_type'] == t))
    return result


def finite_population_upper_bound(population_size, sample_size,
                                  observed_false_exclusions=0, alpha=0.05):
    """Exact one-sided hypergeometric bound for zero observed misses."""
    if observed_false_exclusions != 0:
        raise NotImplementedError('This exact implementation covers zero misses only')
    denom = comb(population_size, sample_size)
    return max(m for m in range(population_size + 1)
               if (comb(population_size - m, sample_size) / denom
                   if population_size - m >= sample_size else 0) >= alpha)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--ledger', required=True)
    p.add_argument('--crosswalk', required=True)
    p.add_argument('--decisions', required=True)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    with open(a.ledger, newline='') as f:
        rows = list(csv.DictReader(f))
    with open(a.crosswalk, newline='') as f:
        cases = list(csv.DictReader(f))
    with open(a.decisions, newline='') as f:
        ds = list(csv.DictReader(f))
    final = {r['case_id']:r['final_investigator_label'] for r in ds}
    if len(final) != len(ds):
        raise ValueError('Duplicate decision')
    counts = verify_population(rows)
    samples = validate_review(cases, final)
    bound = finite_population_upper_bound(351, 60)
    result = {'population':counts, 'sample_results':samples,
              'finite_population_one_sided_95pct_upper_count':bound}
    Path(a.output).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
