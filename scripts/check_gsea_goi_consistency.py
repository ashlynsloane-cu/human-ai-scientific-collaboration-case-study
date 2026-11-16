#!/usr/bin/env python3
"""Reconcile full gene-set membership and leading-edge flags with gene–pathway edges.

Standard-library only. Input files remain local; no input rows are copied to
stdout. This tool does not assume a particular project, gene set or organism.
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path


def _read(path: Path, delimiter: str):
    with path.open('r', newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f, delimiter=delimiter))


def _truthy(value):
    return str(value).strip().lower() in {'true', 't', '1', 'yes'}


def _genes(value):
    return {v.strip().upper() for v in str(value).split(',') if v.strip()}


def audit(pathways_path: Path, edges_path: Path):
    """Return aggregate counts and pathway discrepancies (without identifiers)."""
    paths = _read(pathways_path, '\t')
    edges = _read(edges_path, ',')
    needed_paths = {'NAME', 'GenesInPathway', 'AnyLeadingEdgeGOI'}
    needed_edges = {'Pathway', 'Gene', 'IsLeadingEdge', 'IsGeneOfInterest'}
    if paths and not needed_paths.issubset(paths[0]):
        raise ValueError('Missing required pathway columns')
    if edges and not needed_edges.issubset(edges[0]):
        raise ValueError('Missing required edge columns')
    if len({p['NAME'] for p in paths}) != len(paths):
        raise ValueError('Duplicate pathway names in summary')
    mapped = {}
    for edge in edges:
        if _truthy(edge['IsGeneOfInterest']):
            key = edge['Pathway'].strip()
            rec = mapped.setdefault(key, {'genes': set(), 'any_leading': False})
            rec['genes'].add(edge['Gene'].strip().upper())
            rec['any_leading'] |= _truthy(edge['IsLeadingEdge'])
    membership_errors = 0
    leading_errors = 0
    for path in paths:
        obs = mapped.get(path['NAME'], {'genes': set(), 'any_leading': False})
        membership_errors += (_genes(path['GenesInPathway']) != obs['genes'])
        leading_errors += (_truthy(path['AnyLeadingEdgeGOI']) != obs['any_leading'])
    return {
        'n_pathways': len(paths),
        'n_edges': len(edges),
        'membership_agreement': len(paths) - membership_errors,
        'leading_edge_agreement': len(paths) - leading_errors,
        'membership_mismatches': membership_errors,
        'leading_edge_mismatches': leading_errors,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pathways', type=Path, required=True,
                        help='Tab-separated pathway membership summary')
    parser.add_argument('--edges', type=Path, required=True,
                        help='Comma-separated gene–pathway edge table')
    parser.add_argument('--strict', action='store_true',
                        help='Exit nonzero on any mismatch')
    args = parser.parse_args()
    result = audit(args.pathways, args.edges)
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.strict and (result['membership_mismatches'] or
                        result['leading_edge_mismatches']):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
