"""Synthetic source-only tests: never copy private reviewer data into tests."""
import csv
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'phase8_validate_eligibility.py'
spec = importlib.util.spec_from_file_location('validator', SCRIPT)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


def fake_conv(message='Test user text'):
    return {'current_node': 'user-node', 'mapping': {
        'user-node': {'id': 'user-node', 'parent': None,
                      'message': {'author': {'role': 'user'}, 'content': {'parts': [message]}}}}}


def make_case(text='Test user text'):
    return {'conversation_id': 'fake-1', 'source_node_id': 'user-node',
            'source_first_user_sha256': hashlib.sha256(text.encode()).hexdigest(),
            'phase8_ai_provisional_label': 'uncertain',
            'decision_status': 'NEW_PHASE8_AI_PROVISIONAL',
            'human_label': '', 'final_label': '',
            'nontext_assessment': 'NOT_ASSESSED', 'original_stratum': 'out_of_scope_screen'}


class ProvenanceTest(unittest.TestCase):
    def setUp(self):
        self.case = make_case()
        self.conv = fake_conv()
        self.prob = [{'conversation_id': 'fake-1'}]

    def ok(self, cases=None, prob=None):
        return v.verify_records(
            cases if cases is not None else [self.case], [], [],
            prob if prob is not None else self.prob, {'fake-1': self.conv})

    def test_synthetic_valid(self):
        self.assertTrue(self.ok())

    def test_invalid_hash_rejected(self):
        case = dict(self.case, source_first_user_sha256='0' * 64)
        with self.assertRaises(ValueError): self.ok([case])

    def test_incorrect_node_rejected(self):
        case = dict(self.case, source_node_id='wrong-node')
        with self.assertRaises(ValueError): self.ok([case])

    def test_invalid_label_rejected(self):
        case = dict(self.case, phase8_ai_provisional_label='confirmed')
        with self.assertRaises(ValueError): self.ok([case])

    def test_forged_human_review_rejected(self):
        case = dict(self.case, human_label='include')
        with self.assertRaises(ValueError): self.ok([case])

    def test_duplicates_rejected(self):
        with self.assertRaises(ValueError): self.ok([self.case, self.case])

    def test_prior_overlap_rejected(self):
        with self.assertRaises(ValueError):
            v.verify_records([self.case], [{'conversation_id': 'fake-1'}], [],
                             self.prob, {'fake-1': self.conv})

    def test_unreviewed_sample_case_rejected(self):
        with self.assertRaises(ValueError): self.ok(prob=[{'conversation_id':'fake-2'}])

    def test_aggregate_public_safe(self):
        pilot = [{'conversation_id':'p5','decision':'include','original_stratum':'A_core_evidence'}]
        p7 = [{'conversation_id':'p7','ai_first_pass_label':'exclude','selection_group':'B_context_review'}]
        res = v.aggregate([self.case], pilot, p7, self.prob, [])
        self.assertEqual(res['total_distinct_with_ai_review'], 3)
        self.assertEqual(res['initially_screened_total_reviewed'], 2)
        self.assertNotIn('fake-1', json.dumps(res))
        self.assertNotIn('p5', json.dumps(res))

    def test_investigator_overlay_bad_link_rejected(self):
        pilot = [{'conversation_id':'p5', 'decision':'include', 'record_no':'pilot_001',
                  'evidence_quote_sha256':'a'*64}]
        overlay = [{'conversation_id':'p5', 'locked_ai_label':'include',
                    'pilot_record_no':'pilot_999', 'final_label':'exclude',
                    'evidence_quote_sha256':'a'*64}]
        with self.assertRaises(ValueError):
            v.verify_investigator_overlay(pilot, overlay)

    def test_sha_manifest_detects_same_size_tamper(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td);f = p / 'conversations-000.json';f.write_bytes(b'abcd')
            man = p/'manifest.csv'
            with man.open('w', newline='') as out:
                w=csv.DictWriter(out,['filename','size_bytes','sha256']);w.writeheader()
                for i in range(11):
                    fn=f'conversations-{i:03d}.json';(p/fn).write_bytes(b'abcd')
                    w.writerow({'filename':fn,'size_bytes':4,
                                'sha256':hashlib.sha256(b'abcd').hexdigest()})
            v.validate_sha_manifest(p,man)
            f.write_bytes(b'abce')
            with self.assertRaises(ValueError):v.validate_sha_manifest(p,man)


if __name__ == '__main__':
    unittest.main()
