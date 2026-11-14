"""Synthetic regression tests. Never include private conversation content."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from phase13_area_scope_rule import AREA, apply, locations, read_ledger, scan


def convo(cid, user='', assistant='', title='', alt=''):
    def node(id_, role, txt, parent):
        return (id_, {'parent': parent, 'message': {'author': {'role': role},
                                'content': {'parts': [txt]}}})
    mapping = dict([node('u','user',user,None),
                    node('a','assistant',assistant,'u'),
                    node('alt','user',alt,'u')])
    return {'id': cid, 'current_node': 'a', 'title': title, 'mapping': mapping}


class ScopeTests(unittest.TestCase):
    def test_standalone_uppercase_triggers(self):
        self.assertTrue(AREA.search('Weighted AREA versus limma'))

    def test_lowercase_does_not_trigger(self):
        self.assertIsNone(AREA.search('crop the title area'))

    def test_embedded_word_does_not_trigger(self):
        self.assertIsNone(AREA.search('CAREER'))

    def test_underscore_file_path_triggers(self):
        self.assertTrue(AREA.search('ROSMAP_AREA_normalized.csv'))

    def test_title_triggers(self):
        self.assertEqual(locations(convo('a', title='AREA analysis'))[0]['role'],'title')

    def test_assistant_only_triggers(self):
        self.assertEqual(locations(convo('a',assistant='AREA'))[0]['role'],'assistant')

    def test_alternative_branch_triggers(self):
        self.assertEqual(locations(convo('a',alt='AREA'))[0]['branch'],'alternative')

    def test_rosmap_not_an_exemption(self):
        self.assertTrue(locations(convo('a', user='ROSMAP and AREA')))

    def test_other_chats_unmodified(self):
        row={'conversation_id':'a','current_working_label':'include','adjudication_type':'AI_PROVISIONAL','title_private':'foo'}
        result, overlay=apply([row], {'a':[]},'2026-11-13')
        self.assertEqual(result[0]['current_working_label'],'include')
        self.assertEqual(overlay,[])

    def test_original_label_preserved(self):
        row={'conversation_id':'a','current_working_label':'uncertain','adjudication_type':'AI_PROVISIONAL','title_private':'foo','source_file_private':'conversations-000.json'}
        result,overlay=apply([row],{'a':[{'role':'user','branch':'mainline','context':'AREA'}]},'2026-11-13')
        self.assertEqual(result[0]['current_working_label'],'exclude')
        self.assertEqual(result[0]['pre_AREA_rule_working_label'],'uncertain')
        self.assertEqual(row['current_working_label'],'uncertain')
        self.assertEqual(overlay[0]['old_label'],'uncertain')

    def test_scan_restricts_population(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'conversations-000.json'
            path.write_text(json.dumps([convo('inside',user='foo'),convo('outside',user='AREA')]))
            rows=[{'conversation_id':'inside','source_file_private':path.name}]
            self.assertEqual(scan(rows,Path(d)),{'inside':[]})

    def test_missing_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'conversations-000.json';path.write_text('[]')
            with self.assertRaises(ValueError):scan([{'conversation_id':'missing','source_file_private':path.name}],Path(d))


if __name__=='__main__':unittest.main()

class LedgerIntegrityTests(unittest.TestCase):
    def test_duplicate_ids_rejected(self):
        import csv
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'ledger.csv'
            fields=['conversation_id','created_utc','current_working_label','adjudication_type','source_file_private','title_private']
            with path.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
                r=dict(conversation_id='a',created_utc='2026-10-01',current_working_label='exclude',adjudication_type='AI_PROVISIONAL',source_file_private='conversations-000.json',title_private='test')
                w.writerow(r);w.writerow(r)
            with self.assertRaises(ValueError):read_ledger(path)

    def test_unrecognized_label_rejected(self):
        import csv
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'ledger.csv'
            fields=['conversation_id','created_utc','current_working_label','adjudication_type','source_file_private','title_private']
            with path.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
                w.writerow(dict(conversation_id='a',created_utc='2026-10-01',current_working_label='maybe',adjudication_type='AI_PROVISIONAL',source_file_private='conversations-000.json',title_private='test'))
            with self.assertRaises(ValueError):read_ledger(path)
