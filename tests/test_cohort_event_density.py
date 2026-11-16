"""Synthetic-only tests for cohort event density; no project records."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from cohort_event_density import summarize

class CohortTests(unittest.TestCase):
    def test_counts_conversation_start_not_message_time(self):
        turns = [{'message_id':'a','conversation_id':'c1','created_utc':'2026-01-01T01:00:00Z'},
                 {'message_id':'b','conversation_id':'c1','created_utc':'2026-01-01T01:00:00Z'},
                 {'message_id':'c','conversation_id':'c2','created_utc':'2026-02-01T01:00:00Z'}]
        events = [{'event_id':'x','conversation_id':'c1'}, {'event_id':'y','conversation_id':'c1'}]
        res=summarize(events, turns)
        self.assertEqual(res[0]['provisional_events'],2)
        self.assertEqual(res[0]['events_per_100_user_turns'],100.0)
        self.assertEqual(res[1]['provisional_events'],0)
    def test_repeat_event_rejected(self):
        turns=[{'message_id':'a','conversation_id':'c','created_utc':'2026-01-01'}]
        events=[{'event_id':'x','conversation_id':'c'},{'event_id':'x','conversation_id':'c'}]
        with self.assertRaises(ValueError):summarize(events,turns)
    def test_unknown_conversation_rejected(self):
        turns=[{'message_id':'a','conversation_id':'c','created_utc':'2026-01-01'}]
        with self.assertRaises(ValueError):summarize([{'event_id':'x','conversation_id':'nope'}],turns)
    def test_duplicate_message_rejected(self):
        turns=[{'message_id':'a','conversation_id':'c','created_utc':'2026-01-01'}]*2
        with self.assertRaises(ValueError):summarize([],turns)
    def test_inconsistent_conversation_date_rejected(self):
        turns=[{'message_id':'a','conversation_id':'c','created_utc':'2026-01-01'},
               {'message_id':'b','conversation_id':'c','created_utc':'2026-02-01'}]
        with self.assertRaises(ValueError):summarize([],turns)
if __name__=='__main__':unittest.main()
