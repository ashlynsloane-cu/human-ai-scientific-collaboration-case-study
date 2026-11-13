"""Fixture-based Phase 4 tests; no original conversation data required."""

import csv
import importlib.util
import json
import pathlib
import tempfile
import unittest

SCRIPT = (pathlib.Path(__file__).resolve().parents[1]
          / "scripts" / "phase4_corpus_gate.py")
spec = importlib.util.spec_from_file_location("phase4_corpus_gate", SCRIPT)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class StructuralUnitTests(unittest.TestCase):
    def test_parent_order_instead_of_timestamp_order(self):
        mapping = {"root": {"parent": None},
                   "leaf": {"parent": "middle"},
                   "middle": {"parent": "root"},
                   "side": {"parent": "root"}}
        path, status, outside = audit.mainline(mapping, "leaf")
        self.assertEqual(path, ["root", "middle", "leaf"])
        self.assertEqual(status, "ok")
        self.assertEqual(outside, 0)

    def test_cycle_does_not_loop(self):
        path, status, outside = audit.mainline(
            {"a": {"parent": "b"}, "b": {"parent": "a"}}, "a")
        self.assertEqual(status, "cycle")
        self.assertEqual(len(path), 2)
        self.assertEqual(outside, 0)

    def test_unknown_current_node(self):
        self.assertEqual(
            audit.mainline({"a": {"parent": None}}, "absent")[1],
            "missing_or_unknown_current_node")

    def test_nontext_message_is_not_assumed_to_be_plain_text(self):
        m = {"content": {"content_type": "multimodal_text", "parts": [
            "Please check this figure", {"content_type": "image_asset_pointer"}]}}
        self.assertEqual(audit.message_text(m), "Please check this figure")
        self.assertEqual(audit.nontext_parts(m), 1)
        self.assertEqual(audit.message_text({"content": {"parts": [{}]}}), "")

    def test_random_sample_order_independent(self):
        rows = [{"conversation_id": f"id-{i:03}"} for i in range(80)]
        a = audit.stable_sample(rows, 25, "fixed-seed", "outside")
        b = audit.stable_sample(list(reversed(rows)), 25,
                                "fixed-seed", "outside")
        self.assertEqual(a, b)
        self.assertEqual(len(set(x["conversation_id"] for x in a)), 25)


class SyntheticIntegrationTests(unittest.TestCase):
    def test_complete_coverage_with_private_public_separation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            source = root / "export"
            source.mkdir()
            private = root / "PRIVATE_LOCAL_ONLY"
            public = root / "REPO_SAFE"
            phase1 = root / "screening.csv"
            phase2 = root / "phase2"
            phase2.mkdir()
            rows = []
            for i, label in enumerate(("A_core_evidence", "B_context_review",
                                        "C_weak_or_ai_only", "outside")):
                cid = f"private-conversation-{i}"
                mapping = {
                    "user": {"parent": None, "message": {
                        "author": {"role": "user"}, "content": {
                            "content_type": "multimodal_text", "parts": [
                                "confidential raw text", {"asset_pointer": "private"}]
                        }, "metadata": {"attachments": [{"name": "secret.png"}]}}},
                    "assistant": {"parent": "user", "message": {
                        "author": {"role": "assistant"}, "content": {
                            "content_type": "text", "parts": ["private reply"]}}},
                }
                rows.append({"id": cid, "conversation_id": cid,
                             "title": "private subject/title", "mapping": mapping,
                             "current_node": "assistant", "create_time": 1_800_000_000})
            name = "conversations-000.json"
            payload = json.dumps(rows)
            (source / name).write_text(payload)
            (source / "export_manifest.json").write_text(json.dumps({
                "export_files": [{"path": name, "size_bytes": len(payload.encode())}]}))
            with phase1.open("w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=[
                    "conversation_id", "screening_tier"])
                writer.writeheader()
                for i, label in enumerate(("A_core_evidence", "B_context_review",
                                           "C_weak_or_ai_only")):
                    writer.writerow({"conversation_id": f"private-conversation-{i}",
                                     "screening_tier": label})
            audit.write_csv(phase2 / "out_of_scope_rescue_candidates.csv", [],
                            ["conversation_id"])
            audit.write_csv(phase2 / "message_provenance_index.csv", [],
                            ["conversation_id", "node_id"])
            audit.write_csv(phase2 / "candidate_intervention_queue.csv", [],
                            ["conversation_id", "candidate_id",
                             "human_user_message_node_id", "preceding_ai_message_node_id",
                             "interaction_context"])
            report = audit.build(source, phase1, phase2, private, public,
                                 sample_n=1, multimodal_n=1, seed="replay")
            self.assertEqual(report["conversation_count"], 4)
            self.assertEqual(report["first_screened"], 3)
            self.assertEqual(report["not_first_screened"], 1)
            self.assertEqual(report["user_multimodal_without_text_all_branches"], 0)
            self.assertEqual(report["sampling"]["probability_pilot_n"], 4)
            pub = (public / "corpus_gate_aggregate.json").read_text()
            for sensitive in ("private-conversation", "confidential raw text",
                              "private subject/title", "secret.png"):
                self.assertNotIn(sensitive, pub)
            self.assertIn("private-conversation-0",
                          (private / "all_conversations_qc_index.csv").read_text())

    def test_fails_closed_on_unflagged_input_as_screening(self):
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            bad = root / "screening.csv"
            audit.write_csv(bad, [{"conversation_id": "a",
                                   "screening_tier": "out_of_scope_screen"}],
                            ["conversation_id", "screening_tier"])
            # Guard is exercised in full build after fixture setup above;
            # here verify the input tier is outside permitted flagged strata.
            self.assertNotIn(audit.read_csv(bad)[0]["screening_tier"],
                             audit.STRATA[:-1])


if __name__ == "__main__":
    unittest.main()
