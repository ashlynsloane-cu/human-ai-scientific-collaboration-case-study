"""Synthetic tests for the first-pass eligibility aggregator."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from phase5_adjudication_summary import read_ledger, summarize, canonical_json

STRATA=('A_core_evidence','B_context_review','C_weak_or_ai_only','out_of_scope_screen')


def synthetic():
    rows=[]
    for st in STRATA:
        for i in range(25):
            rows.append({'conversation_id':f'private_{st}_{i}',
                'original_stratum':st,
                'decision':'include' if i==0 else 'exclude',
                'selection_reasons':f'probability_pilot:{st}' + (';lexical_rescue_census' if st=='out_of_scope_screen' and i<5 else ''),
                'evidence_node_id':f'private-node-{st}-{i}',
                'individualized_reason':'Example source-backed reason',
                'independent_confirmation':'PENDING',
                'coding_status':'PROVISIONAL_SOURCE_TEXT_SCREEN',
                'conversation_title_private':f'Private Title {st} {i}',
                'evidence_quote_private':'private snippet'})
    return rows


class Phase5SyntheticTests(unittest.TestCase):
    def test_count_invariants(self):
        out=summarize(synthetic())
        self.assertEqual(out['total_distinct_reviewed'],100)
        self.assertEqual(out['overall_decisions']['include'],4)
        self.assertTrue(out['missed_inclusion_confirmed_in_probability_out_of_scope_sample'])
        self.assertEqual(out['lexical_rescue_census']['n'],5)

    def test_public_does_not_leak_private(self):
        txt=canonical_json(summarize(synthetic()))
        for s in ('private_', 'Private Title', 'private-node', 'private snippet'):
            self.assertNotIn(s,txt)

    def test_no_inference_from_enrichment(self):
        rows=synthetic()
        rows.append(dict(rows[0],conversation_id='extra1',selection_reasons='nontext_enrichment:in_first_screen'))
        out=summarize(rows)
        self.assertEqual(out['total_distinct_reviewed'],101)
        self.assertEqual(out['probability_pilot_only']['A_core_evidence']['n'],25)

    def test_missing_evidence_is_rejected(self):
        rows=synthetic()
        with tempfile.TemporaryDirectory() as d:
            fp=Path(d)/'labels.csv'
            fields=sorted({k for r in rows for k in r})
            rows[0]['evidence_node_id']=''
            with fp.open('w',newline='',encoding='utf-8') as f:
                w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
            with self.assertRaisesRegex(ValueError,'source pointer'):
                read_ledger(fp)

    def test_duplicate_ids_rejected(self):
        rows=synthetic()
        rows[1]['conversation_id']=rows[0]['conversation_id']
        with tempfile.TemporaryDirectory() as d:
            fp=Path(d)/'labels.csv'
            fields=list(rows[0]);
            with fp.open('w',newline='',encoding='utf-8') as f:
                w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
            with self.assertRaisesRegex(ValueError,'duplicate'):
                read_ledger(fp)

    def test_missing_selection_reason_rejected(self):
        rows=synthetic()
        rows[4]['selection_reasons']=''
        with self.assertRaisesRegex(ValueError,'selection reason'):
            summarize(rows)


if __name__=='__main__':
    unittest.main()
