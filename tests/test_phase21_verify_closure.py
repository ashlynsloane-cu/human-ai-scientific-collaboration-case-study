import unittest
from scripts.phase21_verify_closure import check_ledger

class ClosureTest(unittest.TestCase):
    def setUp(self):
        self.rows = ([{"conversation_id": "I" + str(i), "phase20_effective_label": "include"} for i in range(245)] + [{"conversation_id": "E" + str(i), "phase20_effective_label": "exclude"} for i in range(352)])
    def test_ok(self): self.assertEqual(check_ledger(self.rows)["include"],245)
    def test_missing(self):
        with self.assertRaises(ValueError): check_ledger(self.rows[:-1])
    def test_duplicate(self):
        bad=[dict(x) for x in self.rows];bad[0]["conversation_id"]=bad[1]["conversation_id"]
        with self.assertRaises(ValueError): check_ledger(bad)
    def test_label(self):
        bad=[dict(x) for x in self.rows];bad[0]["phase20_effective_label"]="uncertain"
        with self.assertRaises(ValueError):check_ledger(bad)

if __name__=='__main__':unittest.main()
