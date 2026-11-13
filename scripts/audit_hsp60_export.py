#!/usr/bin/env python3
"""Read-only, metadata-first Hsp60/10 ChatGPT export inventory. No message bodies exported."""
import csv
import datetime as dt
import glob
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILES = sorted(ROOT.glob('conversations-[0-9][0-9][0-9].json'))
OUT = ROOT / 'hsp60_export_audit'
OUT.mkdir(exist_ok=True)
patterns = {
 'core': re.compile(r'\b(?:hsp\s*60(?:/\s*10)?|hsp\s*10|hspd1|hspe1|groel|groes|chaperonin)\b',re.I),
 'cohort': re.compile(r'\b(?:rosmap|braak|cerad|msbb|radc)\b',re.I),
 'biology': re.compile(r'\b(?:mitochondrial proteostasis|mitochondrial chaperon|mitochondrial client|uprmt|mic[- ]binding|tmt proteomics)\b',re.I),
 'artifact': re.compile(r'\b(?:supplementary figure|suppfig|manuscript|reviewer|revision|figure legend|cetsa|gsea|tufm)\b',re.I),
}

def timestamp(v):
 if isinstance(v,(int,float)):
  return dt.datetime.fromtimestamp(v,dt.timezone.utc).isoformat()
 return ''

def extract_text(m):
 co=m.get('content') or {}
 parts=co.get('parts')
 if not isinstance(parts,list):return ''
 return '\n'.join(x for x in parts if isinstance(x,str))

rows=[]; details=[]; seen=set(); role_totals={}; branch_count=0
for fp in FILES:
 contents=fp.read_bytes()
 for c in json.loads(contents):
  cid=c.get('id') or c.get('conversation_id') or ''
  if cid in seen: raise ValueError('Repeated conversation id '+cid)
  seen.add(cid)
  title=c.get('title') or ''
  mapping=c.get('mapping') or {}
  user=[]; assistant=[]; roles={}
  for node in mapping.values():
   m=node.get('message') or {}
   role=(m.get('author') or {}).get('role') or 'null'
   if not m:continue
   roles[role]=roles.get(role,0)+1
   tx=extract_text(m)
   if role=='user':user.append(tx)
   if role=='assistant':assistant.append(tx)
  def count_hits(k, texts):return sum(bool(patterns[k].search(t)) for t in texts)
  ut={k:count_hits(k,user) for k in patterns}
  at={k:count_hits(k,assistant) for k in patterns}
  core_title=bool(patterns['core'].search(title))
  core_user=ut['core']
  cohort_user=ut['cohort']
  biology_user=ut['biology']
  # Broad screening, NOT a final inclusion classification.
  if core_title or core_user>=2 or (core_user and (cohort_user or biology_user)):
   tier='A_core_evidence'
  elif core_user or cohort_user>=2 or (cohort_user and (biology_user or ut['artifact']>=2)) or biology_user>=2:
   tier='B_context_review'
  elif any(ut.values()) or any(at[k] for k in ('core','cohort','biology')):
   tier='C_weak_or_ai_only'
  else:tier='out_of_scope_screen'
  row={'conversation_id':cid,'title':title,'created_utc':timestamp(c.get('create_time')),
       'updated_utc':timestamp(c.get('update_time')),'source_file':fp.name,
       'nodes_total':len(mapping),'messages_user':len(user),'messages_assistant':len(assistant),
       'user_core_messages':ut['core'],'user_cohort_messages':ut['cohort'],
       'user_biology_messages':ut['biology'],'user_artifact_messages':ut['artifact'],
       'assistant_core_messages':at['core'],'assistant_cohort_messages':at['cohort'],
       'screening_tier':tier,'manual_review_status':'not_reviewed',
       'inclusion_decision':'undetermined','notes':''}
  rows.append(row)
  if tier!='out_of_scope_screen':details.append(row)
manifest=json.loads((ROOT/'export_manifest.json').read_text())
listed={x.get('path'):x.get('size_bytes') for x in manifest.get('export_files',[]) if isinstance(x,dict)}
checks=[]
for f in FILES:
 checks.append({'file':f.name,'expected_bytes':listed.get(f.name),'actual_bytes':f.stat().st_size,
                'byte_match':listed.get(f.name)==f.stat().st_size,
                'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})

def write_csv(name,items):
 if not items:return
 with (OUT/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(items[0]));w.writeheader();w.writerows(items)
write_csv('all_conversations_metadata.csv',rows)
write_csv('screening_candidates.csv',details)
write_csv('file_integrity.csv',checks)
counts={x:sum(r['screening_tier']==x for r in rows) for x in ('A_core_evidence','B_context_review','C_weak_or_ai_only','out_of_scope_screen')}
summary={'files':len(FILES),'records':len(rows),'unique_ids':len(seen),
         'first_created_utc':min(r['created_utc'] for r in rows if r['created_utc']),
         'last_created_utc':max(r['created_utc'] for r in rows if r['created_utc']),
         'last_updated_utc':max(r['updated_utc'] for r in rows if r['updated_utc']),
         'screening_counts':counts,'manifest_bytes_match':all(x['byte_match'] for x in checks),
         'no_message_bodies_in_outputs':True,
         'scope_note':'Automated broad screening only; human verification and artifact-level validation are not complete.'}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
print('\nHighest-priority titles:')
for r in sorted((x for x in details if x['screening_tier']=='A_core_evidence'),key=lambda x:(x['user_core_messages'],x['user_cohort_messages']),reverse=True)[:20]:
 print(r['title'],r['user_core_messages'],r['user_cohort_messages'])
