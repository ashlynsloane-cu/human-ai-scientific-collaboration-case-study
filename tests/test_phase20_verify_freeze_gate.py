import unittest
from scripts.phase20_verify_freeze_gate import (
    finite_population_upper_bound, validate_review, verify_population,
)


class Phase20GateTests(unittest.TestCase):
    def test_population(self):
        r = [{'conversation_id':str(i),'phase20_effective_label':'include'} for i in range(3)]
        self.assertEqual(verify_population(r, 3)['include'], 3)

    def test_duplicate_rejected(self):
        r = [{'conversation_id':'a','phase20_effective_label':'include'}] * 2
        with self.assertRaises(ValueError): verify_population(r, 2)

    def test_unknown_label_rejected(self):
        with self.assertRaises(ValueError):
            verify_population([{'conversation_id':'a','phase20_effective_label':'bad'}], 1)

    def test_population_mismatch_rejected(self):
        with self.assertRaises(ValueError): verify_population([], 1)

    def test_exact_upper_bound(self):
        self.assertEqual(finite_population_upper_bound(351, 60), 15)

    def test_unsupported_nonzero_observed(self):
        with self.assertRaises(NotImplementedError):
            finite_population_upper_bound(351,60,1)

    def test_review(self):
        rows=([{'review_case_id':str(i),'sampling_type':'probability'} for i in range(60)]
              +[{'review_case_id':str(i),'sampling_type':'included_control'} for i in range(60,70)]
              +[{'review_case_id':str(i),'sampling_type':'purposive_targeted'} for i in range(70,77)])
        d={str(i):'EXCLUDE' for i in range(77)}
        self.assertEqual(validate_review(rows,d)['probability']['EXCLUDE'],60)
        with self.assertRaises(ValueError): validate_review(rows,{'0':'EXCLUDE'})
        with self.assertRaises(ValueError): validate_review(rows,dict(d,**{'0':'UNCERTAIN'}))
        with self.assertRaises(ValueError): validate_review(rows+[rows[0]],d)

if __name__ == '__main__': unittest.main()
