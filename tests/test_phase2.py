"""Offline unit tests for public, metadata-only Hsp60/10 screening code."""
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_phase2 as audit  # noqa: E402


class Phase2Tests(unittest.TestCase):
    def test_exposure_e5_never_auto_assigned(self):
        self.assertNotIn('E5', ';'.join(audit.EVIDENCE_FLAGS))

    def test_mainline_excludes_other_branches(self):
        conversation = {
            'current_node': 'final',
            'mapping': {
                'root': {'parent': None},
                'first': {'parent': 'root'},
                'final': {'parent': 'first'},
                'alternative': {'parent': 'root'},
            },
        }
        self.assertEqual(audit.mainline_ids(conversation),
                         {'root', 'first', 'final'})

    def test_cross_project_title_not_direct(self):
        group = audit.review_group(
            'A_core_evidence', 'Personal Statement Condensation',
            4, 1, 1, 1,
        )
        self.assertEqual(group, 'context_or_cross_project_review')

    def test_marker_recognition(self):
        self.assertTrue(audit.CORE.search('Hsp60/10 clients'))
        self.assertTrue(audit.COHORT.search('ROSMAP'))

    def test_published_summary_is_unvalidated(self):
        summary = json.loads(
            (ROOT / 'results/phase2/summary.json').read_text()
        )
        self.assertEqual(summary['source_conversations'], 1049)
        self.assertFalse(summary['findings_intervention_impact_or_persistence_proven'])
        self.assertEqual(summary['candidate_interaction_cues_NOT_VALIDATED'], 2028)


if __name__ == '__main__':
    unittest.main()
