"""Synthetic tests only; never import raw conversation data into Git."""
import importlib.util
import unittest
import tempfile
import csv
import hashlib
import json
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / 'scripts' / 'phase6_corpus_recall_audit.py'
spec = importlib.util.spec_from_file_location('phase6', MODULE)
phase6 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(phase6)


class Phase6AuditTest(unittest.TestCase):
    def test_mainline_follows_parent_and_not_unvisited_alternative(self):
        c = {'current_node':'n3', 'mapping':{
            'n1':{'parent':None, 'message':None},
            'n2':{'parent':'n1', 'message':{'author':{'role':'user'}}},
            'n3':{'parent':'n2', 'message':{'author':{'role':'assistant'}}},
            'stray':{'parent':'n1', 'message':{'author':{'role':'assistant'}}},
        }}
        path = phase6.walk_current_branch(c)
        self.assertEqual(len(path),3)
        self.assertEqual(path[0]['parent'],None)
        self.assertNotIn(c['mapping']['stray'],path)

    def test_cycle_raises(self):
        c={'current_node':'a','mapping':{'a':{'parent':'b'},'b':{'parent':'a'}}}
        with self.assertRaises(ValueError):
            phase6.walk_current_branch(c)

    def test_text_parts_only_and_no_image_content_hallucination(self):
        msg={'content':{'parts':['Text',{'content_type':'image_asset_pointer'}]}}
        self.assertEqual(phase6.text_from_message(msg),'Text')
        self.assertEqual(phase6.text_from_message({'content':{'parts':[{'image':1}]}}),'')

    def test_priority_similarity_not_a_binary_label(self):
        b={'a':phase6.token_counts('Hsp10 project','Braak client analysis',''),
           'b':phase6.token_counts('Other topic','trails shoes','')}
        v=phase6.make_vectors(b)
        self.assertTrue(0 <= phase6.cosine(v['a'],v['b'])<=1)
        self.assertEqual(phase6.neighbor_stats(v['a'],{'a':v['a']},'a'), (0.,0.))

    def test_stable_quartile_sample_without_duplicates(self):
        rows=[{'conversation_id':str(i), 'included_sim_max':str(i/101.)}
              for i in range(100)]
        a,s=phase6.stratified_audit(rows,5,'fixed')
        b,_=phase6.stratified_audit(list(reversed(rows)),5,'fixed')
        self.assertEqual(a,b)
        self.assertEqual(len(a),20)
        self.assertEqual(len(set(r['conversation_id'] for r in a)),20)
        self.assertEqual(s,{'Q1':25,'Q2':25,'Q3':25,'Q4':25})

    def test_sample_rejects_insufficient_population(self):
        rows=[{'conversation_id':str(i),'included_sim_max':'0.0'}
              for i in range(12)]
        with self.assertRaises(ValueError):
            phase6.stratified_audit(rows,4,'x')

    def test_user_excerpt_not_assistant_claim(self):
        excerpt=phase6.source_excerpt(['short','Please revise Supplementary Figure 5 for the analysis.'])
        self.assertIn('Supplementary Figure 5',excerpt)
        self.assertNotIn('short',excerpt)

    def _synthetic_inputs(self, home):
        root = Path(home)
        export = root / 'export'
        export.mkdir()
        records = []
        for i in range(10):
            records.append({
                'id':f'fake-{i}', 'title':f'Case {i}',
                'current_node':'node1',
                'mapping':{'node1':{
                    'parent':None, 'message':{
                        'author':{'role':'user'},
                        'content':{'parts':[f'hsp cohort line {i}']},
                    }}},
            })
        raw = json.dumps(records).encode('utf8')
        source = export / 'conversations-000.json'
        source.write_bytes(raw)
        (export / 'export_manifest.json').write_text(json.dumps({
            'export_files':[{'path':source.name,'size_bytes':len(raw)}]
        }))
        digests = root / 'digests.csv'
        index = root / 'index.csv'
        pilot = root / 'pilot.csv'
        overlay = root / 'overlay.csv'

        def csv_save(path, columns, rows):
            with path.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=columns)
                w.writeheader()
                w.writerows(rows)

        csv_save(digests,['filename','sha256'],[{'filename':source.name,
                 'sha256':hashlib.sha256(raw).hexdigest()}])
        csv_save(index,['conversation_id','source_file','created_utc',
                        'stratum','needs_nontext_review',
                        'other_branch_user_assistant_nodes'],[{
            'conversation_id':f'fake-{i}', 'source_file':source.name,
            'created_utc':'2026-01-01T00:00:00Z',
            'stratum':'A_core_evidence' if i < 2 else 'out_of_scope_screen',
            'needs_nontext_review':'False',
            'other_branch_user_assistant_nodes':'0'} for i in range(10)])
        csv_save(pilot,['conversation_id','decision'],[{
            'conversation_id':'fake-0','decision':'include'},
            {'conversation_id':'fake-1','decision':'exclude'}])
        csv_save(overlay,['conversation_id','locked_ai_label',
                          'final_label','first_pass_csv_sha256'],[{
            'conversation_id':'fake-0','locked_ai_label':'include',
            'final_label':'include','first_pass_csv_sha256':
            hashlib.sha256(pilot.read_bytes()).hexdigest()}])
        return export,index,digests,pilot,overlay

    def test_build_private_output_and_public_no_source_identifiers(self):
        with tempfile.TemporaryDirectory() as tmp:
            args=self._synthetic_inputs(tmp)
            private=Path(tmp)/'private'; public=Path(tmp)/'public'
            result=phase6.build(*args, private, public, per_quartile=1)
            self.assertEqual(result['unreviewed_conversations'],8)
            self.assertEqual(result['probability_audit']['sample_n'],4)
            public_text=(public/'corpus_completeness_design.json').read_text()
            self.assertNotIn('fake-0',public_text)
            self.assertNotIn('fake-9',public_text)
            self.assertIn('fake-9', (private/'full_remainder_PRIVATE.csv').read_text())

    def test_build_rejects_tampered_source_sha_even_if_size_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            args=self._synthetic_inputs(tmp)
            path=args[0]/'conversations-000.json'
            text=path.read_text().replace('hsp cohort','bad cohort')
            self.assertEqual(len(text.encode()),len(path.read_bytes()))
            path.write_text(text)
            with self.assertRaisesRegex(ValueError,'SHA-256 mismatch'):
                phase6.build(*args,Path(tmp)/'private',Path(tmp)/'public',
                             per_quartile=1)

    def test_build_rejects_overlay_wrong_fingerprint(self):
        with tempfile.TemporaryDirectory() as tmp:
            args=self._synthetic_inputs(tmp)
            overlay=args[4]
            overlay.write_text(overlay.read_text().replace(
                hashlib.sha256(args[3].read_bytes()).hexdigest(), 'x'*64))
            with self.assertRaisesRegex(ValueError,'different first-pass ledger'):
                phase6.build(*args,Path(tmp)/'private',Path(tmp)/'public',
                             per_quartile=1)

    def test_id_determinism_sha_rank(self):
        rows=[{'conversation_id':str(i)} for i in range(30)]
        a=phase6.deterministic_sample(rows,10,'123','A')
        b=phase6.deterministic_sample(list(reversed(rows)),10,'123','A')
        self.assertEqual(a,b)

if __name__=='__main__':
    unittest.main()
