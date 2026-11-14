"""Synthetic-only tests; not research data or source transcript classifications."""
import importlib.util
import pathlib
import unittest

SPEC = importlib.util.spec_from_file_location(
    'phase19', pathlib.Path(__file__).resolve().parents[1] /
    'scripts' / 'phase19_validate_false_exclusion.py')
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class Phase19Tests(unittest.TestCase):
    def setUp(self):
        self.base = [
            {'conversation_id': 'a', 'phase18_effective_label': 'exclude'},
            {'conversation_id': 'b', 'phase18_effective_label': 'exclude'},
            {'conversation_id': 'c', 'phase18_effective_label': 'include'},
        ]
        self.correction = [{'conversation_id': 'a', 'phase18_label': 'exclude',
                            'phase19_label': 'include', 'rationale': 'confirmed'}]

    def test_overlay_replay(self):
        self.assertEqual(module.validate_and_apply(self.base, self.correction, 3),
                         {'population': 3, 'corrections': 1,
                          'after': {'exclude': 1, 'include': 2, 'uncertain': 0}})

    def test_baseline_immutable(self):
        original = [dict(x) for x in self.base]
        module.validate_and_apply(self.base, self.correction, 3)
        self.assertEqual(self.base, original)

    def test_duplicate_baseline_rejected(self):
        with self.assertRaises(ValueError):
            module.validate_and_apply(self.base + [self.base[0]], self.correction)

    def test_population_mismatch(self):
        with self.assertRaises(ValueError):
            module.validate_and_apply(self.base, self.correction, 4)

    def test_unknown_overlay(self):
        alt = [dict(self.correction[0], conversation_id='unknown')]
        with self.assertRaises(ValueError):
            module.validate_and_apply(self.base, alt)

    def test_prior_label_tamper(self):
        alt = [dict(self.correction[0], phase18_label='include')]
        with self.assertRaises(ValueError):
            module.validate_and_apply(self.base, alt)

    def test_duplicate_overlay(self):
        with self.assertRaises(ValueError):
            module.validate_and_apply(self.base, self.correction * 2)

    def test_missing_rationale(self):
        alt = [dict(self.correction[0], rationale='  ')]
        with self.assertRaises(ValueError):
            module.validate_and_apply(self.base, alt)

    def test_no_op_correction(self):
        alt = [dict(self.correction[0], phase19_label='exclude')]
        with self.assertRaises(ValueError):
            module.validate_and_apply(self.base, alt)

    def test_sample_validation(self):
        r = [dict(x, phase19_effective_label=x['phase18_effective_label'])
             for x in self.base]
        sample = [
            {'conversation_id': 'a', 'review_case_id': 'x', 'prior_label': 'exclude',
             'sampling_type': 'probability'},
            {'conversation_id': 'c', 'review_case_id': 'y', 'prior_label': 'include',
             'sampling_type': 'included_control'},
        ]
        self.assertEqual(module.validate_sample(sample, r, 1, 1),
                         {'exclude': 1, 'include': 1})

    def test_sample_label_tamper(self):
        r = [dict(x, phase19_effective_label=x['phase18_effective_label'])
             for x in self.base]
        sample = [{'conversation_id': 'a', 'review_case_id': 'x',
                   'prior_label': 'include', 'sampling_type': 'probability'}]
        with self.assertRaises(ValueError):
            module.validate_sample(sample, r, 1, 0)

    def test_sampling_replay(self):
        sample = [dict(x, phase19_effective_label=x['phase18_effective_label'])
                  for x in self.base]
        first = module.reconstruct_randomized_ids(sample, 1, 1, seed=41)
        again = module.reconstruct_randomized_ids(sample, 1, 1, seed=41)
        self.assertEqual(first, again)
        self.assertEqual(len(set(first)), 2)

    def test_sample_population_rejected(self):
        sample = [dict(x, phase19_effective_label=x['phase18_effective_label'])
                  for x in self.base]
        with self.assertRaises(ValueError):
            module.reconstruct_randomized_ids(sample, 5, 1)


if __name__ == '__main__':
    unittest.main()
