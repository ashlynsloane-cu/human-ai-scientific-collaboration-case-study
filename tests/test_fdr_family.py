"""Synthetic validation cases: no research data."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_fdr_family import benjamini_hochberg, check_rows


class FdrFamilyTests(unittest.TestCase):
    def test_bh_monotone(self):
        result = benjamini_hochberg([0.03, 0.01, 0.2])
        for observed, expected in zip(result, [0.045, 0.03, 0.2]):
            self.assertAlmostEqual(observed, expected)

    def test_separate_families(self):
        data = [{'family': 'A', 'p': '.01', 'q': '.02'},
                {'family': 'A', 'p': '.04', 'q': '.04'},
                {'family': 'B', 'p': '.8', 'q': '.8'}]
        result = check_rows(data, 'p', 'q', 'family')
        self.assertTrue(all(row['matches_exported_family'] for row in result))

    def test_filtered_subset_mismatch(self):
        data = [{'p': '.01', 'q': '.05'}, {'p': '.04', 'q': '.10'}]
        result = check_rows(data, 'p', 'q')
        self.assertFalse(result[0]['matches_exported_family'])

    def test_invalid_p(self):
        with self.assertRaises(ValueError):
            benjamini_hochberg([1.2])


if __name__ == '__main__':
    unittest.main()
