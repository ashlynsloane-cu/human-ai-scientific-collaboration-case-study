#!/usr/bin/env python3
"""Check whether reported adjusted p-values match BH within a stated family.

This tool does not identify the *correct* FDR family. A mismatch may mean the
export is a filtered subset of the tests, not necessarily an analysis error.
"""
import argparse
import csv
import json
import math
from collections import defaultdict


def as_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return float('nan')


def benjamini_hochberg(pvalues):
    """BH step-up adjustment, omitting nonfinite p-values from the family."""
    sorted_pairs = sorted((p, i) for i, p in enumerate(pvalues)
                          if math.isfinite(p))
    m = len(sorted_pairs)
    results = [float('nan')] * len(pvalues)
    smallest = 1.0
    for index in range(m - 1, -1, -1):
        p, original_index = sorted_pairs[index]
        if p < 0 or p > 1:
            raise ValueError('p-values must be between 0 and 1')
        smallest = min(smallest, p * m / (index + 1), 1.0)
        results[original_index] = smallest
    return results


def check_rows(rows, p_column, q_column, family_column=None,
               tolerance=1e-9):
    groups = defaultdict(list)
    for row in rows:
        group = row[family_column] if family_column else 'all'
        groups[group].append(row)
    out = []
    for family, entries in sorted(groups.items()):
        expected = benjamini_hochberg([as_float(x[p_column])
                                       for x in entries])
        observed = [as_float(x[q_column]) for x in entries]
        pairs = [(a, b) for a, b in zip(expected, observed)
                 if math.isfinite(a) and math.isfinite(b)]
        matches = sum(abs(a - b) <= tolerance for a, b in pairs)
        out.append({'family': family, 'n_rows': len(entries),
                    'n_comparable': len(pairs), 'n_matches': matches,
                    'max_abs_difference': max(
                        (abs(a - b) for a, b in pairs), default=None),
                    'matches_exported_family': bool(pairs) and matches == len(pairs)})
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv_file')
    parser.add_argument('--p-column', required=True)
    parser.add_argument('--adjusted-column', required=True)
    parser.add_argument('--family-column')
    args = parser.parse_args()
    with open(args.csv_file, newline='', encoding='utf-8-sig') as f:
        data = list(csv.DictReader(f))
    print(json.dumps(check_rows(data, args.p_column,
                                args.adjusted_column, args.family_column),
                     indent=2))


if __name__ == '__main__':
    main()
