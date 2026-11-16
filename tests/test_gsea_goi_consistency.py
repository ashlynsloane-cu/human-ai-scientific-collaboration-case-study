"""Synthetic, non-research-data tests for GSEA membership/leading-edge audit."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / 'scripts' / 'check_gsea_goi_consistency.py'
spec = importlib.util.spec_from_file_location('gsea_audit', MODULE)
audit_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_module)


class GOIConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.p = root / 'paths.txt'
        self.e = root / 'edges.csv'
        self.p.write_text('NAME\tGenesInPathway\tAnyLeadingEdgeGOI\n'
                          'P1\tG1, G2\tTRUE\nP2\tG3\tFALSE\n')
        self.e.write_text('Pathway,Gene,IsLeadingEdge,IsGeneOfInterest\n'
                          'P1,G1,FALSE,TRUE\nP1,G2,TRUE,TRUE\n'
                          'P2,G3,FALSE,TRUE\nP2,G4,TRUE,FALSE\n')

    def test_consistent(self):
        res = audit_module.audit(self.p, self.e)
        self.assertEqual(res['membership_mismatches'], 0)
        self.assertEqual(res['leading_edge_mismatches'], 0)

    def test_misreported_leading_edge(self):
        self.p.write_text(self.p.read_text().replace('P2\tG3\tFALSE',
                                                      'P2\tG3\tTRUE'))
        self.assertEqual(audit_module.audit(self.p, self.e)['leading_edge_mismatches'], 1)

    def test_missing_member(self):
        self.p.write_text(self.p.read_text().replace('G1, G2', 'G1'))
        self.assertEqual(audit_module.audit(self.p, self.e)['membership_mismatches'], 1)

    def test_non_goi_not_counted(self):
        self.assertEqual(audit_module.audit(self.p, self.e)['membership_agreement'], 2)

    def test_duplicate_summary_raises(self):
        with self.p.open('a') as out:
            out.write('P1\tG1\tFALSE\n')
        with self.assertRaises(ValueError):
            audit_module.audit(self.p, self.e)


if __name__ == '__main__':
    unittest.main()
