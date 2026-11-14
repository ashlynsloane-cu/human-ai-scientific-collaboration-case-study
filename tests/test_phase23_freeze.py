import csv, hashlib, json, tempfile, unittest
from pathlib import Path
from scripts.phase23_verify_freeze import verify_snapshot

class FreezeTests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();p=Path(self.t.name)
  self.paths=[p/'all.csv',p/'in.csv',p/'out.csv']
  self.rows=[{'conversation_id':f'id{i:04}', 'phase20_effective_label':'include' if i<245 else 'exclude'} for i in range(597)]
  with self.paths[0].open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=['conversation_id','phase20_effective_label']);w.writeheader();w.writerows(self.rows)
  for i, subset in [(1,self.rows[:245]),(2,self.rows[245:])]:
   with self.paths[i].open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['conversation_id']);w.writeheader();w.writerows([{'conversation_id':x['conversation_id']} for x in subset])
  self.m=dict(zip(['locked_full_ledger_sha256','locked_roster_sha256','locked_exclusion_roster_sha256'],[hashlib.sha256(x.read_bytes()).hexdigest() for x in self.paths]))
 def tearDown(self):self.t.cleanup()
 def test_valid(self):self.assertEqual(verify_snapshot(*self.paths,self.m)['include'],245)
 def test_roster_tamper(self):
  self.paths[1].write_text('broken')
  with self.assertRaises(ValueError):verify_snapshot(*self.paths,self.m)
 def test_ledger_tamper(self):
  self.paths[0].write_text('broken')
  with self.assertRaises(ValueError):verify_snapshot(*self.paths,self.m)
 def test_excluded_tamper(self):
  self.paths[2].write_text('broken')
  with self.assertRaises(ValueError):verify_snapshot(*self.paths,self.m)
 def test_duplicate(self):
  r=[dict(x) for x in self.rows];r[-1]['conversation_id']=r[-2]['conversation_id']
  with self.paths[0].open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=['conversation_id','phase20_effective_label']);w.writeheader();w.writerows(r)
  self.m['locked_full_ledger_sha256']=hashlib.sha256(self.paths[0].read_bytes()).hexdigest()
  with self.assertRaises(ValueError):verify_snapshot(*self.paths,self.m)

if __name__=='__main__':unittest.main()
