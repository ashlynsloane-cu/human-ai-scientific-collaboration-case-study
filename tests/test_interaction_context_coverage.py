import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from interaction_context_coverage import ancestor_with_role, context_status, match_source_text

class ContextCoverageTests(unittest.TestCase):
    def setUp(self):
        self.c = {'x': {'mapping': {
            'a': {'parent': None, 'message': {'author': {'role':'assistant'}, 'content': {'parts':['Analyze with model A']}}},
            't': {'parent': 'a', 'message': {'author': {'role':'tool'}, 'content': {'parts':['tool']}}},
            'u': {'parent': 't', 'message': {'author': {'role':'user'}, 'content': {'parts':['Instead use model B']}}},
        }}}

    def test_parent_traversal_skips_tool(self):
        k, m = ancestor_with_role(self.c['x']['mapping'], 'u')
        self.assertEqual(k, 'a')

    def test_full_context(self):
        self.assertEqual(context_status(self.c, 'x', 'u'), 'user_and_preceding_assistant_recovered')

    def test_missing_conversation(self):
        self.assertEqual(context_status(self.c, 'missing', 'u'), 'conversation_unavailable')

    def test_missing_anchor(self):
        self.assertEqual(context_status(self.c, 'x', 'unknown'), 'anchor_unavailable')

    def test_no_ai_predecessor(self):
        self.assertEqual(context_status({'y': {'mapping': {'u': {'parent':None, 'message':{'author':{'role':'user'},'content':{'parts':['new idea']}}}}}}, 'y','u'), 'no_preceding_assistant')

    def test_exact_text(self):
        self.assertTrue(match_source_text('x', 'x'))
        self.assertFalse(match_source_text('x', ' x '))

if __name__ == '__main__':
    unittest.main()
