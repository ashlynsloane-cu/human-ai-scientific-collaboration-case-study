"""Synthetic-data tests only; no private research data."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from recode_three_outcomes import recode


class TestRecoding(unittest.TestCase):
    def example(self, status, eid="e1"):
        return {"event_id":eid,"scientific_category":"Interpretation / claim calibration",
                "phase47_reconciled_evidence_state":status}

    def test_manuscript_boundary_counts_as_supported(self):
        result = recode([self.example("MANUSCRIPT_RETENTION_ONLY")])
        self.assertEqual(result[0]["outcome_B"], "SUPPORTED_BY_FINAL_MANUSCRIPT")

    def test_partial_is_not_rejection(self):
        result = recode([self.example("PARTIAL_OR_AMBIGUOUS")])
        self.assertEqual(result[0]["outcome_B"], "PARTIAL_OR_AMBIGUOUS")

    def test_unverified_is_not_rejection(self):
        result = recode([self.example("EXACT_IMPLEMENTATION_UNVERIFIED")])
        self.assertEqual(result[0]["outcome_B"], "NOT_ESTABLISHED")

    def test_no_causality_inferred(self):
        result = recode([self.example("IMPLEMENTATION_SUPPORTED")])
        self.assertEqual(result[0]["outcome_C"], "NOT_ESTABLISHED_FROM_CURRENT_REGISTER")

    def test_duplicate_ids_rejected(self):
        with self.assertRaises(ValueError):
            recode([self.example("IMPLEMENTATION_SUPPORTED"), self.example("IMPLEMENTATION_SUPPORTED")])

    def test_unrecognized_status_rejected(self):
        with self.assertRaises(ValueError):
            recode([self.example("UNKNOWN_STATUS")])


if __name__ == "__main__":
    unittest.main()
