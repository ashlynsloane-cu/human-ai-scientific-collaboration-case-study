"""Lexical rescue audit for weakly named project chats excluded by first pass."""
import argparse,csv,json,re
from pathlib import Path

TERMS={
 'MIC_compound':re.compile(r'\bMIC\b',re.I),
 'explicit_MIC_name':re.compile(r'mitophagy.inducing coumarin',re.I),
 'candidate_clients_DLD_DLST':re.compile(r'\b(?:DLD|DLST)\b',re.I),
}

def run(src,out):
 prior={r['conversation_id'] for r in csv.DictReader((src/'hsp60_export_audit/screening_candidates.csv').open())}
 rescued=[]
 for p in sorted(src.glob('conversations-[0-9][0-9][0-9].json')):
  for c in json.load(p.open()):
   cid=c.get('id') or c.get('conversation_id')
   if cid in prior:continue
   user='\n'.join(x for node in (c.get('mapping') or {}).values() for m in [node.get('message') or {}]
      if (m.get('author') or {}).get('role')=='user' for x in ((m.get('content') or {}).get('parts') or []) if isinstance(x,str))
   hits=[k for k,pat in TERMS.items() if pat.search(user)]
   if hits:rescued.append({'conversation_id':cid,'title':c.get('title') or '',
      'source_file':p.name,'created_unix':c.get('create_time') or '',
      'rescue_term_classes':';'.join(hits),'human_inclusion_review':'PENDING',
      'final_inclusion_decision':'UNASSESSED','notes':'Possible contextual/false-negative; no intervention codes assigned'})
 with out.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['conversation_id','title','source_file','created_unix','rescue_term_classes','human_inclusion_review','final_inclusion_decision','notes']);w.writeheader();w.writerows(rescued)
 print('Out-of-screen rescue candidates:',len(rescued))

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();run(Path(a.input),Path(a.out))
