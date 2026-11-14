"""Synthetic only: no conversation content or source IDs used in tests."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from phase10_validate_scoped_eligibility import summarize


def fixtures():
    census = [
        {'conversation_id':'pre','created_utc':'2025-09-30T05:00:00+00:00',
         'last_message_utc':'2025-09-30T06:00:00+00:00','in_scope':'0'},
        {'conversation_id':'oct1','created_utc':'2025-10-01T06:00:00+00:00',
         'last_message_utc':'2025-10-01T06:01:00+00:00','in_scope':'1'},
        {'conversation_id':'oct2','created_utc':'2025-10-02T00:00:00+00:00',
         'last_message_utc':'2025-10-02T00:01:00+00:00','in_scope':'1'},
    ]
    ledger = [
        {'conversation_id':'oct1','created_utc':census[1]['created_utc'],
         'source_phase':'phase5','current_working_label':'include',
         'ai_original_label':'include','adjudication_type':'AI_PROVISIONAL'},
        {'conversation_id':'oct2','created_utc':census[2]['created_utc'],
         'source_phase':'phase10','current_working_label':'exclude',
         'ai_original_label':'uncertain','adjudication_type':'INVESTIGATOR_OVERLAY'},
    ]
    return census,ledger

class ScopeValidationTests(unittest.TestCase):
    def test_valid_population(self):
        c,l=fixtures();a=summarize(c,l)
        self.assertEqual(a['post_cutoff_in_scope'],2)
        self.assertEqual(a['pre_cutoff_removed_from_primary_scope'],1)
        self.assertEqual(a['post_cutoff_working_labels'],{'exclude':1,'include':1})
    def test_denver_midnight_is_included(self):
        c,l=fixtures();self.assertEqual(summarize(c,l)['post_cutoff_in_scope'],2)
    def test_pre_cutoff_ledger_rejected(self):
        c,l=fixtures();l[0]['conversation_id']='pre'
        with self.assertRaises(ValueError):summarize(c,l)
    def test_duplicated_census_rejected(self):
        c,l=fixtures();c.append(copy.deepcopy(c[0]))
        with self.assertRaises(ValueError):summarize(c,l)
    def test_duplicated_ledger_rejected(self):
        c,l=fixtures();l.append(copy.deepcopy(l[0]))
        with self.assertRaises(ValueError):summarize(c,l)
    def test_missing_in_scope_ledger_rejected(self):
        c,l=fixtures();l.pop()
        with self.assertRaises(ValueError):summarize(c,l)
    def test_unrecognized_label_rejected(self):
        c,l=fixtures();l[0]['current_working_label']='maybe'
        with self.assertRaises(ValueError):summarize(c,l)
    def test_unapproved_ai_label_change_rejected(self):
        c,l=fixtures();l[0]['current_working_label']='exclude'
        with self.assertRaises(ValueError):summarize(c,l)
    def test_documented_overlay_accepted(self):
        c,l=fixtures();self.assertEqual(summarize(c,l)['investigator_overlay_cases_in_scope'],1)
    def test_boundary_crossover_detected(self):
        c,l=fixtures();c[0]['last_message_utc']='2025-10-05T00:00:00+00:00'
        self.assertEqual(summarize(c,l)['pre_created_with_post_cutoff_messages'],1)
    def test_wrong_scope_flag_rejected(self):
        c,l=fixtures();c[1]['in_scope']='0'
        with self.assertRaises(ValueError):summarize(c,l)
    def test_naive_timestamp_rejected(self):
        c,l=fixtures();c[0]['created_utc']='2025-09-30T05:00:00'
        with self.assertRaises(ValueError):summarize(c,l)
    def test_last_message_precedes_creation_rejected(self):
        c,l=fixtures();c[0]['last_message_utc']='2020-01-01T00:00:00+00:00'
        with self.assertRaises(ValueError):summarize(c,l)

if __name__=='__main__':unittest.main()
