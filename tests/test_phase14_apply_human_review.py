import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from phase14_apply_human_review import validate_and_apply

F = 'a' * 64

def data():
    base = [dict(conversation_id=str(i), current_working_label=label,
                ai_original_label=label, source_fingerprint_private=F,
                adjudication_type='AI_PROVISIONAL')
            for i, label in enumerate(['uncertain', 'include', 'exclude', 'uncertain'])]
    reviews = [dict(case_id=f'B{i}', conversation_id=str(i), human_label=label,
                    original_ai_label=base[i]['ai_original_label'],
                    case_text_sha256=F, source_fingerprint=F,
                    human_rationale='Investigator verified')
               for i, label in enumerate(['include', 'exclude', 'exclude', 'uncertain'])]
    return base, reviews

class Phase14Tests(unittest.TestCase):
    def test_expected_overlay(self):
        before, human = data()
        after, audit, a = validate_and_apply(before, human, expected=4)
        self.assertEqual(a['changed_labels'], 2)
        self.assertEqual(a['uncertain_resolved'], 1)
        self.assertEqual(a['after'], {'exclude': 2, 'include': 1, 'uncertain': 1})
        self.assertEqual(before[0]['current_working_label'], 'uncertain')
        self.assertEqual(after[0]['ai_original_label'], 'uncertain')
        self.assertEqual(len(audit), 4)
    def test_replay(self):
        a, b = data()
        self.assertEqual(validate_and_apply(a,b,expected=4), validate_and_apply(a,b,expected=4))
    def test_count(self):
        a,b=data();self.assertRaises(ValueError,validate_and_apply,a,b[:-1],expected=4)
    def test_duplicate_case(self):
        a,b=data();b[1]['case_id']=b[0]['case_id'];self.assertRaises(ValueError,validate_and_apply,a,b,expected=4)
    def test_duplicate_conversation(self):
        a,b=data();b[1]['conversation_id']='0';self.assertRaises(ValueError,validate_and_apply,a,b,expected=4)
    def test_unknown_conversation(self):
        a,b=data();b[1]['conversation_id']='missing';self.assertRaises(ValueError,validate_and_apply,a,b,expected=4)
    def test_ai_label_mismatch(self):
        a,b=data();b[1]['original_ai_label']='uncertain';self.assertRaises(ValueError,validate_and_apply,a,b,expected=4)
    def test_evidence_mismatch(self):
        a,b=data();b[1]['source_fingerprint']='b'*64;self.assertRaises(ValueError,validate_and_apply,a,b,expected=4)
    def test_missing_rationale(self):
        a,b=data();b[1]['human_rationale']='';self.assertRaises(ValueError,validate_and_apply,a,b,expected=4)
    def test_invalid_label(self):
        a,b=data();b[1]['human_label']='yes';self.assertRaises(ValueError,validate_and_apply,a,b,expected=4)
    def test_hard_scope_conflict(self):
        a,b=data();a[0]['adjudication_type']='INVESTIGATOR_AREA_LITERAL_SCOPE_RULE';self.assertRaises(ValueError,validate_and_apply,a,b,expected=4)
    def test_hard_scope_same_label(self):
        a,b=data();a[2]['adjudication_type']='INVESTIGATOR_AREA_LITERAL_SCOPE_RULE';self.assertEqual(validate_and_apply(a,b,expected=4)[0][2]['adjudication_type'],'INVESTIGATOR_AREA_LITERAL_SCOPE_RULE')
    def test_base_duplicate(self):
        a,b=data();a[1]['conversation_id']=a[0]['conversation_id'];self.assertRaises(ValueError,validate_and_apply,a,b,expected=4)
    def test_invalid_base_label(self):
        a,b=data();a[0]['current_working_label']='unknown';self.assertRaises(ValueError,validate_and_apply,a,b,expected=4)

if __name__ == '__main__': unittest.main()
