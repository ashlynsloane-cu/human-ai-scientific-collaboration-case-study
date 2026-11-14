"""Synthetic tests for Phase 9 corpus-extension validation. No private data."""
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / 'scripts' / 'phase9_validate_coverage.py'
spec = importlib.util.spec_from_file_location('p9_validate', SOURCE)
p9 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p9)


def synth_remainder():
    return [
        {'conversation_id': f'example-{i:04d}', 'priority_score': str(1000-i)}
        for i in range(608)
    ]


def synth_ledger(source=None):
    src = source or synth_remainder()
    wanted = p9.expected_selection(src)
    return [
        {'conversation_id': key, 'selection_partition': part,
         'selection_order': str(n), 'ai_provisional_label': 'exclude',
         'ai_source_context_rationale': 'Synthetic alternative domain',
         'reviewer': 'SINGLE_AI_PROVISIONAL', 'human_blind_label': '',
         'final_adjudicated_label': '',
         'source_excerpts_reviewed': 'SELECTED_USER_MESSAGE_EXCERPTS_NOT_FULL_CONVERSATION'}
        for key, (part, n) in wanted.items()
    ]


class ValidateCoverageTests(unittest.TestCase):
    def test_exact_selection_counts_and_uniqueness(self):
        selected = p9.expected_selection(synth_remainder())
        self.assertEqual(len(selected), 200)
        self.assertEqual(sum(p == p9.PART_HIGH for p, _ in selected.values()), 120)
        self.assertEqual(sum(p == p9.PART_LOW for p, _ in selected.values()), 80)

    def test_selection_repeatable_under_row_reordering(self):
        source = synth_remainder()
        self.assertEqual(p9.expected_selection(source), p9.expected_selection(source[::-1]))

    def test_select_not_dependent_on_labels(self):
        source = synth_remainder()
        wanted = p9.expected_selection(source)
        for row in source:
            row['desired_outcome'] = 'include'
        self.assertEqual(wanted, p9.expected_selection(source))

    def test_valid_review_passes(self):
        self.assertTrue(p9.validate_selection(synth_ledger(), synth_remainder()))

    def test_duplicate_id_rejected(self):
        records = synth_ledger()
        records[-1]['conversation_id'] = records[0]['conversation_id']
        with self.assertRaises(ValueError):
            p9.validate_selection(records, synth_remainder())

    def test_moved_partition_rejected(self):
        records = synth_ledger()
        records[0]['selection_partition'] = 'OTHER'
        with self.assertRaises(ValueError):
            p9.validate_selection(records, synth_remainder())

    def test_unrecognized_label_rejected(self):
        records = synth_ledger()
        records[0]['ai_provisional_label'] = 'verified_include'
        with self.assertRaises(ValueError):
            p9.validate_selection(records, synth_remainder())

    def test_unperformed_human_review_rejected(self):
        records = synth_ledger()
        records[0]['human_blind_label'] = 'include'
        with self.assertRaises(ValueError):
            p9.validate_selection(records, synth_remainder())

    def test_missing_rationale_rejected(self):
        records = synth_ledger()
        records[0]['ai_source_context_rationale'] = ' '
        with self.assertRaises(ValueError):
            p9.validate_selection(records, synth_remainder())

    def test_cumulative_aggregation(self):
        prior = {'total_distinct_with_ai_review': 441,
                 'working_total_ai_labels_including_investigator_phase5_overlay':
                 {'include': 206, 'exclude': 163, 'uncertain': 72}}
        report = p9.aggregate(synth_ledger(), prior)
        self.assertEqual(report['working_total_distinct_assessed'], 641)
        self.assertEqual(report['still_without_source_excerpt_assessment'], 408)
        self.assertEqual(report['cumulative_provisional_labels_with_previous_investigator_overlay']['exclude'], 363)
        self.assertEqual(set(report), p9.PUBLIC_FIELDS)
        self.assertNotIn('conversation_id', json.dumps(report))
        self.assertNotIn('example-0000', json.dumps(report))

    def test_prior_phase_drift_rejected(self):
        prior = {'total_distinct_with_ai_review': 440,
                 'working_total_ai_labels_including_investigator_phase5_overlay':
                 {'include': 206, 'exclude': 163, 'uncertain': 72}}
        with self.assertRaises(ValueError):
            p9.aggregate(synth_ledger(), prior)

    def test_mainline_excludes_unselected_branch(self):
        data = {'current_node': 'u1', 'mapping': {
            'u1': {'id': 'u1', 'parent': None,
                   'message': {'author': {'role': 'user'}, 'content': {'parts': ['selected']}}},
            'u2': {'id': 'u2', 'parent': None,
                   'message': {'author': {'role': 'user'}, 'content': {'parts': ['other']}}}}}
        self.assertEqual(p9.source_user_parts(data), [('u1', 'selected')])

    def test_nontext_user_ignored_not_falsely_text_scanned(self):
        data = {'current_node': 'u1', 'mapping': {
            'u1': {'id': 'u1', 'parent': None, 'message': {
                'author': {'role': 'user'},
                'content': {'parts': [{'content_type': 'image_asset_pointer'}]}}}}}
        self.assertEqual(p9.source_user_parts(data), [])

    def test_cycle_detection(self):
        data = {'current_node': 'u1', 'mapping': {
            'u1': {'id': 'u1', 'parent': 'u1', 'message': {'author': {'role': 'user'},
                                                          'content': {'parts': ['test']}}}}}
        with self.assertRaises(ValueError):
            p9.source_user_parts(data)


if __name__ == '__main__':
    unittest.main()
