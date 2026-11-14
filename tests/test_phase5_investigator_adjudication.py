"""Synthetic tests: do not use private conversations or adjudicator rationales."""
import importlib.util
import pathlib
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "phase5_apply_investigator_adjudication.py"
spec = importlib.util.spec_from_file_location("phase5_adjudicator", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def source(ident, label):
    return {"conversation_id": ident, "decision": label}


def override(case, ident, old, new):
    return {"case_id": case, "conversation_id": ident,
            "locked_ai_label": old, "final_label": new,
            "investigator_rationale": "Private verified clarification",
            "evidence_status": "INVESTIGATOR_CLARIFICATION_NOT_INDEPENDENT"}


class Phase5InvestigatorAdjudicationTests(unittest.TestCase):
    def setUp(self):
        self.baseline = [source("a", "include"), source("b", "uncertain"),
                         source("c", "uncertain"), source("d", "exclude")]
        self.overrides = [override("cal", "a", "include", "include"),
                          override("blind-a", "b", "uncertain", "exclude"),
                          override("blind-b", "c", "uncertain", "exclude")]

    def test_preserves_original_count_and_tracks_changes(self):
        out = module.summarize(self.baseline, self.overrides)
        self.assertEqual(out["first_pass"], {"include": 1, "exclude": 1, "uncertain": 2})
        self.assertEqual(out["post_adjudication"], {"include": 1, "exclude": 3, "uncertain": 0})
        self.assertEqual(out["changed_case_count"], 2)
        self.assertEqual(out["uncertain_cases_resolved"], 2)
        self.assertEqual(self.baseline[1]["decision"], "uncertain")

    def test_no_private_ids_in_public_aggregate(self):
        import json
        out = json.dumps(module.summarize(self.baseline, self.overrides))
        for phrase in ("blind-a", "blind-b", "Private verified clarification"):
            self.assertNotIn(phrase, out)

    def test_rejects_incorrect_original_label(self):
        wrong = [dict(self.overrides[1], locked_ai_label="exclude")]
        with self.assertRaises(ValueError):
            module.summarize(self.baseline, wrong)

    def test_rejects_duplicate_id(self):
        with self.assertRaises(ValueError):
            module.summarize(self.baseline, self.overrides + [self.overrides[0]])

    def test_rejects_missing_rationale(self):
        wrong = [dict(self.overrides[0], investigator_rationale="")]
        with self.assertRaises(ValueError):
            module.summarize(self.baseline, wrong)

    def test_rejects_unknown_first_pass_conversation(self):
        with self.assertRaises(ValueError):
            module.summarize(self.baseline, [override("new", "absent", "include", "exclude")])


if __name__ == "__main__":
    unittest.main()
