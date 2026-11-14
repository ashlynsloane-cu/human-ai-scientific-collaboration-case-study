"""Synthetic tests; never use sensitive transcripts as fixtures."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from phase25_validate_pilot_coverage import validate_inventory


def good():
    m=[{'message_id':'u1','case_id':'P1','message_seq':'0','role':'user','text_sha256':'hash'},
       {'message_id':'a1','case_id':'P1','message_seq':'1','role':'assistant','text_sha256':'hash2'},
       {'message_id':'u2','case_id':'P1','message_seq':'2','role':'user','text_sha256':'hash3'}]
    t=[{'user_message_id':'u1','case_id':'P1','seq':'0','user_text_sha256':'hash','primary_steering_type':'NOT_ADJUDICATED'},
       {'user_message_id':'u2','case_id':'P1','seq':'2','user_text_sha256':'hash3','primary_steering_type':'NOT_ADJUDICATED'}]
    return m,t

class CoverageTests(unittest.TestCase):
    def chk(self,m,t):return validate_inventory(m,t,1,3,2)
    def test_valid(self):self.assertEqual(self.chk(*good())['assistant_messages'],1)
    def test_missing_message(self):
        m,t=good()
        with self.assertRaises(ValueError):self.chk(m[:-1],t)
    def test_duplicate_id(self):
        m,t=good();m[1]['message_id']='u1'
        with self.assertRaises(ValueError):self.chk(m,t)
    def test_duplicate_seq(self):
        m,t=good();m[1]['message_seq']='0'
        with self.assertRaises(ValueError):self.chk(m,t)
    def test_wrong_source_hash(self):
        m,t=good();t[0]['user_text_sha256']='tampered'
        with self.assertRaises(ValueError):self.chk(m,t)
    def test_missing_user_turn(self):
        m,t=good()
        with self.assertRaises(ValueError):self.chk(m,t[:1])
    def test_wrong_role(self):
        m,t=good();m[2]['role']='assistant'
        with self.assertRaises(ValueError):self.chk(m,t)
    def test_adjudicated_label_not_allowed(self):
        m,t=good();t[0]['primary_steering_type']='correct'
        with self.assertRaises(ValueError):self.chk(m,t)
    def test_duplicate_user_turn(self):
        m,t=good();t[1]=dict(t[0])
        with self.assertRaises(ValueError):self.chk(m,t)
    def test_wrong_case_pointer(self):
        m,t=good();t[1]['case_id']='P2'
        with self.assertRaises(ValueError):self.chk(m,t)

if __name__=='__main__':unittest.main()
