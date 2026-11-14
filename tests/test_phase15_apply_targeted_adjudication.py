import copy
import importlib.util
from pathlib import Path
import unittest

PATH=Path(__file__).resolve().parents[1]/"scripts/phase15_apply_targeted_adjudication.py"
spec=importlib.util.spec_from_file_location("phase15_mod",PATH)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class Phase15Tests(unittest.TestCase):
    def setUp(self):
        self.base=[{"conversation_id":"a","current_working_label":"uncertain","ai_original_label":"uncertain","AREA_literal_match":"FALSE","phase14_human_label":"uncertain","adjudication_type":"INVESTIGATOR_HUMAN_BLINDED_PHASE11","created_utc":"2026-01-01","source_file_private":"source.json","title_private":"An analysis"}, {"conversation_id":"b","current_working_label":"exclude","ai_original_label":"exclude","AREA_literal_match":"FALSE","phase14_human_label":"","adjudication_type":"AI_PROVISIONAL","created_utc":"2026-01-02","source_file_private":"source.json","title_private":"Other"}]
        self.cases=[{"case_id":"r1","conversation_id_PRIVATE":"a","source_file_PRIVATE":"source.json","title":"An analysis","created_utc":"2026-01-01","case_sha256":"abc"}]
        self.overlay=[{"review_case_id":"r1","conversation_id_PRIVATE":"a","source_case_text_sha256":"abc","source_file_PRIVATE":"source.json","phase14_previous_label":"uncertain","phase14_previous_adjudication_type":"INVESTIGATOR_HUMAN_BLINDED_PHASE11","original_ai_label_preserved":"uncertain","earlier_human_label_preserved":"uncertain","investigator_decision":"include","investigator_rationale":"Confirmed firsthand","basis":"INVESTIGATOR_FIRSTHAND_PROJECT_MEMBERSHIP"}]
    def runit(self):return mod.apply(self.base,self.cases,self.overlay)
    def test_success_and_preservation(self):
        out,c=self.runit();self.assertEqual(c,{"exclude":1,"include":1});self.assertEqual(out[0]["current_working_label"],"uncertain");self.assertEqual(out[0]["phase14_human_label"],"uncertain")
    def test_replay(self):self.assertEqual(self.runit(),self.runit())
    def test_missing_case_rejected(self):
        self.overlay[0]["review_case_id"]="x"
        with self.assertRaises(ValueError):self.runit()
    def test_source_hash_mismatch_rejected(self):
        self.overlay[0]["source_case_text_sha256"]="tampered"
        with self.assertRaises(ValueError):self.runit()
    def test_changed_ai_label_rejected(self):
        self.overlay[0]["original_ai_label_preserved"]="exclude"
        with self.assertRaises(ValueError):self.runit()
    def test_changed_human_label_rejected(self):
        self.overlay[0]["earlier_human_label_preserved"]=""
        with self.assertRaises(ValueError):self.runit()
    def test_overwrite_definitive_rejected(self):
        self.base[0]["current_working_label"]="exclude"
        with self.assertRaises(ValueError):self.runit()
    def test_duplicate_overlay_rejected(self):
        self.overlay.append(self.overlay[0].copy())
        with self.assertRaises(ValueError):self.runit()
    def test_area_hard_scope_rejected(self):
        self.base[0]["AREA_literal_match"]="TRUE"
        with self.assertRaises(ValueError):self.runit()
    def test_missing_rationale_rejected(self):
        self.overlay[0]["investigator_rationale"]=" "
        with self.assertRaises(ValueError):self.runit()
    def test_duplicate_base_rejected(self):
        self.base.append(self.base[0].copy())
        with self.assertRaises(ValueError):self.runit()
    def test_source_title_tamper_rejected(self):
        self.cases[0]["title"]="Altered title"
        with self.assertRaises(ValueError):self.runit()

if __name__=="__main__":unittest.main()
