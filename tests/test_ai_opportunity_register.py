import csv
import tempfile
import unittest
from pathlib import Path
from scripts.validate_ai_opportunity_register import validate

FIELDS=['opportunity_id','event_id','assistant_message_id','user_message_id','next_user_disposition_pilot']

class OpportunityRegisterTests(unittest.TestCase):
    def write(self, rows, fields=FIELDS):
        f=tempfile.NamedTemporaryFile(mode='w',suffix='.csv',delete=False,newline='')
        with f:
            writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
        self.addCleanup(lambda:Path(f.name).unlink(missing_ok=True))
        return f.name

    def record(self, identifier='o1', outcome='accept'):
        return dict(zip(FIELDS,[identifier,'e1','a1','u1',outcome]))

    def test_valid(self):
        self.assertEqual(validate(self.write([self.record()]))['opportunities'],1)
    def test_multiple_proposals_single_event(self):
        x=validate(self.write([self.record(),self.record('o2','correct')]))
        self.assertEqual(x['opportunities'],2);self.assertEqual(x['linked_events'],1)
    def test_duplicate_rejected(self):
        with self.assertRaisesRegex(ValueError,'Duplicate'):
            validate(self.write([self.record(),self.record()]))
    def test_missing_field_rejected(self):
        with self.assertRaisesRegex(ValueError,'Missing'):
            validate(self.write([{}],fields=['opportunity_id']))
    def test_blank_disposition_rejected(self):
        with self.assertRaisesRegex(ValueError,'Empty'):
            validate(self.write([self.record(outcome='')]))

if __name__=='__main__':unittest.main()
