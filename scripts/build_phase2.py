#!/usr/bin/env python3
"""Phase-2, read-only Hsp60/10 conversation extraction.

Design principles:
 * Parse entire ChatGPT export, preserve provenance and branch status.
 * Generate screening/review metadata only, NEVER raw message text.
 * Never infer that ROSMAP participant/raw data were uploaded.
 * Never code an intervention as final: this is a candidate queue for review.
 * Never overwrite the frozen v1.0 protocol.
 * Keep conversation IDs, node IDs, attachment names LOCAL ONLY.

Usage:
 python build_phase2.py --input /path/to/export --output /path/to/phase2
"""
import argparse
import collections
import csv
import datetime as dt
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORE = re.compile(r'(?i)\b(?:hsp\s*60(?:\s*[/+&-]\s*10)?|hsp\s*10|hspd1|hspe1|groel|groes|chaperonin(?:s)?|mic[- ]binding)\b')
COHORT = re.compile(r'(?i)\b(?:ROSMAP|RADC|CERAD|Braak|MSBB)\b')
METHOD = re.compile(r'(?i)\b(?:CETSA|TMT|AGORA|deseq2|pseudobulk|differential abundance|qPCR|western blot|immunoblot|protein client|covariate.adj|manuscript|supplement(?:ary|al)|figure legend|reviewer|Zenodo)\b')
ADJACENT = re.compile(r'(?i)\b(?:NSF|GRFP|personal statement|research statement|rotation|AREA|scholarship|fellowship|application)\b')
ALIAS = re.compile(r'(?i)\b(?:DLD|DLST|TUFM|C1QBP|α.KGDH|alpha.KGDH|MIC|mitochondrial proteostasis)\b')
CUE_GROUPS = collections.OrderedDict([
 ('reframe', re.compile(r"(?i)^.{0,100}\b(?:overhaul|reframe|rethink|change the research question|change the narrative|not force the biology|doesn't make sense as a story)\b")),
 ('correct', re.compile(r'(?i)^\s*(?:no[,! ]|wait[,! ]|that(?:\s+is|\'s)\s+(?:wrong|not right)|you(?:\'re| are)\s+wrong|actually[, ]|i (?:think|believe) (?:that )?you(?:\'re| are) wrong|this is (?:wrong|incorrect)|don\'t (?:change|do) that)')),
 ('reject', re.compile(r'(?i)^\s*(?:i (?:don\'t|do not) (?:like|think|want)|i disagree|reject |we (?:shouldn\'t|should not)|this (?:isn\'t|doesn\'t|is not) (?:useful|correct|make sense)|stop (?:doing|changing)|please (?:don\'t|do not))')),
 ('constrain', re.compile(r'(?i)\b(?:do not|don\'t|without|only if|must|make sure|keep (?:the|it|this)|preserv(?:e|ing)|not (?:remove|change)|no more than|avoid|exactly|never|always)\b')),
 ('redirect', re.compile(r'(?i)^\s*(?:instead|let\'s (?:switch|focus|change|rethink)|i (?:want|think we need) (?:to )?(?:overhaul|reframe|shift|rework)|we need (?:a new|to redo)|i(?:\'d| would) rather)')),
 ('approve', re.compile(r'(?i)^\s*(?:yes[,! ]|yep[,! ]|ok(?:ay)?[,! ]|sure[,! ]|i agree|that works|let\'s do it|perfect[,! ]|great[,! ])')),
 ('modify', re.compile(r'(?i)^\s*(?:can you (?:change|update|edit|revise|fix|make|rewrite|rework|adjust|add)|please (?:change|update|edit|revise|fix|make|rewrite|rework|adjust|add)|what if (?:we|you)|i (?:would|want to) (?:change|revise|add)|let\'s (?:add|change|update|revise))')),
 ('initiate', re.compile(r'(?i)^\s*(?:help me|i want to|let\'s (?:do|start|build|make|create|run)|how (?:do|can|should) (?:i|we)|can you (?:write|create|develop|build|run))')),
])

EVIDENCE_FLAGS = collections.OrderedDict([
 ('code_or_specification', re.compile(r'(?i)\b(?:R script|python script|script|\.R\b|\.py\b|function\(|code|github|codex|pipeline|repository|CLI)\b')),
 ('manuscript_or_literature', re.compile(r'(?i)\b(?:manuscript|revision|abstract|introduction|discussion|reviewer|paper|publication|citation|literature|reference|docx|supplement)\b')),
 ('derived_numeric_or_model', re.compile(r'(?i)(?:\bp\s*[=<]|\bp-value|\bFDR\b|\bcoefficient|\bbeta\b|\bn\s*=\s*\d|\bglm\(|\blm\(|\bcovariate|\bnumeric result|\bregression|\banalysis outputs?)')),
 ('figure_or_table', re.compile(r'(?i)\b(?:figure|plot|graph|panel|heatmap|dotplot|scatterplot|table|\.png|\.pdf|\.svg|\.tiff?)\b')),
 ('possible_participant_or_raw_access', re.compile(r'(?i)\b(?:participant.level|individual.level|patient.level|raw ROSMAP|raw proteomics|raw matrix|subject.level|individual_meta_raw|clinical metadata|sample.meta(?:data)?|controlled.access)\b')),
])

def iso(s):
 try:
  if isinstance(s,(int,float)):
   return dt.datetime.fromtimestamp(s,dt.timezone.utc).isoformat()
 except (ValueError, OSError, OverflowError):pass
 return ''

def text_of(m):
 c=m.get('content') or {}
 parts=c.get('parts') or []
 return '\n'.join(x for x in parts if isinstance(x,str)) if isinstance(parts,list) else ''

def attached(m):
 meta=m.get('metadata') or {}
 a=meta.get('attachments') or []
 return [x for x in a if isinstance(x,dict)] if isinstance(a,list) else []

def mainline_ids(c):
 mp=c.get('mapping') or {}; k=c.get('current_node'); seen=set()
 while k and k in mp and k not in seen:
  seen.add(k); k=mp[k].get('parent')
 return seen

def write_csv(path,rows,cols):
 path.parent.mkdir(exist_ok=True,parents=True)
 with path.open('w',encoding='utf-8',newline='') as fh:
  w=csv.DictWriter(fh,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(rows)

def review_group(tier,title,user_core,user_cohort,user_ali,user_methods):
 """Heuristic only. Application and other-project discussions require manual review."""
 if ADJACENT.search(title) and not re.search(r'(?i)hsp|rosmap',title):
  return 'context_or_cross_project_review'
 if re.search(r'(?i)\b(?:Hsp60|Hsp10|Hsp60/10|ROSMAP|client|CETSA|Braak|CERAD|MIC.bind|manuscript|revision|western blot|siRNA|qPCR)\b',title) and (user_core or user_cohort or user_ali):
  return 'direct_project_priority'
 if tier=='A_core_evidence' and (user_core>=2 or (user_core and user_cohort)):
  return 'direct_project_priority'
 if tier.startswith(('A_','B_')):
  return 'needs_project_identity_review'
 return 'weak_reference_review'

def main(args):
 src=Path(args.input); target=Path(args.output)
 private=target/'PRIVATE_LOCAL_ONLY'; shareable=target/'REPO_SAFE'
 private.mkdir(exist_ok=True,parents=True);shareable.mkdir(exist_ok=True,parents=True)
 files=sorted(src.glob('conversations-[0-9][0-9][0-9].json'))
 if len(files)!=11: raise RuntimeError('Expected 11 conversation files, got '+str(len(files)))
 screening_path=src/'hsp60_export_audit/screening_candidates.csv'
 if not screening_path.is_file(): screening_path=Path(__file__).resolve().parent/'PRIVATE_LOCAL_ONLY/first_pass_screening_candidates.csv'
 if not screening_path.is_file(): raise FileNotFoundError('Pass-1 screening CSV missing; run phase 1 first.')
 first={r['conversation_id']:r for r in csv.DictReader(screening_path.open(encoding='utf-8'))}
 all_recs=[]; msgs=[]; events=[]; refs=[]; alt_nodes=[]; monthly=collections.defaultdict(lambda:collections.Counter())
 counters=collections.Counter(); unique=set(); alternate=0; flagged=0
 for fp in files:
  for c in json.load(fp.open(encoding='utf-8')):
   cid=c.get('id') or c.get('conversation_id');
   if cid in unique: raise ValueError('Duplicate conversation '+cid)
   unique.add(cid)
   if cid not in first: continue
   flagged+=1
   meta=first[cid]; tier=meta['screening_tier']; mapping=c.get('mapping') or {}; ml=mainline_ids(c)
   title=c.get('title') or ''; user_core=int(meta['user_core_messages']);user_cohort=int(meta['user_cohort_messages'])
   user_alias=0; user_methods=0
   for nd in mapping.values():
    mm=nd.get('message') or {}
    if (mm.get('author') or {}).get('role')=='user':
     tx=text_of(mm);user_alias+=bool(ALIAS.search(tx));user_methods+=bool(METHOD.search(tx))
   group=review_group(tier,title,user_core,user_cohort,user_alias,user_methods)
   line=[(nd.get('message') or {},nd_id,nd) for nd_id,nd in mapping.items() if nd_id in ml]
   line.sort(key=lambda x:(x[0].get('create_time') if isinstance(x[0].get('create_time'),(int,float)) else 0))
   # Mainline follows parent links; sorting only for timestamp anomalies in downstream metadata.
   nid=c.get('current_node'); seq=[]; visited=set()
   while nid and nid in mapping and nid not in visited:
    visited.add(nid);seq.append((nid,mapping[nid]));nid=mapping[nid].get('parent')
   seq.reverse()
   localmsgs=[]
   for pos,(node_id,node) in enumerate(seq):
    m=node.get('message') or {}; role=(m.get('author') or {}).get('role')
    if role not in ('user','assistant'): continue
    if (m.get('content') or {}).get('content_type') in ('reasoning_recap','thoughts','reasoning'):continue
    tx=text_of(m);att=attached(m)
    if not tx.strip() and not att:continue
    time=iso(m.get('create_time')); month=time[:7] if time else ''
    flags=[label for label,p in EVIDENCE_FLAGS.items() if role=='user' and (p.search(tx) or any(p.search(str(a.get('name') or '')) for a in att))]
    r={'conversation_id':cid,'title':title,'screening_tier':tier,'review_group':group,'source_file':fp.name,
       'node_id':node_id,'parent_node_id':node.get('parent') or '', 'message_timestamp_utc':time,'role':role,
       'model_slug':(m.get('metadata') or {}).get('model_slug') or '',
       'is_current_branch':True,'content_type':(m.get('content') or {}).get('content_type') or '',
       'has_text':bool(tx.strip()),'text_character_count':len(tx),'attachment_count':len(att),
       'contains_core_keyword':bool(CORE.search(tx)),'contains_cohort_keyword':bool(COHORT.search(tx)),
       'exposure_evidence_flags':';'.join(flags),'exposure_code_frozen':'UNASSESSED',
       'contains_sensitive_source_text_in_export':False}
    msgs.append(r);localmsgs.append((r,tx,m,att));counters['mainline_msgs']+=1
    if month:
     monthly[month]['messages_total']+=1
     if role=='user':monthly[month]['user_messages']+=1
     if CORE.search(tx) and role=='user':monthly[month]['user_core_mention_messages']+=1
    for i,at in enumerate(att):
     refs.append({'conversation_id':cid,'node_id':node_id,'timestamp_utc':time,'source_file':fp.name,
          'attachment_index':i,'attachment_id':at.get('id') or '', 'basename':Path(str(at.get('name') or '')).name,
          'mime_type':at.get('mime_type') or '', 'declared_bytes':at.get('size') or '',
          'available_in_uploaded_json':False,'asset_binary_received':False,
          'requires_manual_exposure_review':True})
   # All alternate branches are retained as *counts* for manual reconstruction.
   other_roles=collections.Counter()
   for nn,nd in mapping.items():
    if nn in ml:continue
    m=nd.get('message') or {};role=(m.get('author') or {}).get('role') or 'other'
    if role in ('user','assistant') and (text_of(m).strip() or attached(m)):
     other_roles[role]+=1
   alternate+=sum(other_roles.values())
   for other_id,nd in mapping.items():
    if other_id in ml:continue
    mm=nd.get('message') or {};role=(mm.get('author') or {}).get('role')
    if role not in ('user','assistant') or not (text_of(mm).strip() or attached(mm)):continue
    alt_nodes.append({'conversation_id':cid,'source_file':fp.name,'node_id':other_id,
       'parent_node_id':nd.get('parent') or '', 'timestamp_utc':iso(mm.get('create_time')),
       'role':role,'text_characters':len(text_of(mm)), 'attachment_references':len(attached(mm)),
       'review_status':'UNASSESSED_BRANCH_ALTERNATIVE'})
   ai_prev=None
   for r,tx,m,att in localmsgs:
    if r['role']=='assistant':
     ai_prev=r
     continue
    # User message -> candidate decisions; use short leading text to avoid logs/comments causing false hits.
    head=tx[:360].strip()
    cues=[label for label,pat in CUE_GROUPS.items() if pat.search(head)]
    # Dedicated correction triggers for mid-sentence direct challenges.
    if not cues and re.search(r'(?i)\b(?:that\'s not (?:right|correct)|you (?:misunderstood|missed)|but (?:actually|that\'s not)|i disagree)\b',head):
     cues=['possible_correction']
    # Include human-origin entry points and redirections even without prior AI.
    no_prior_ai=ai_prev is None
    if no_prior_ai and not cues and group=='direct_project_priority' and (CORE.search(head) or COHORT.search(head) or ALIAS.search(head)):
     cues=['project_entry_point']
    if not cues:continue
    # Exclude pure acknowledgments (not intervention) but keep constraints or corrections.
    if cues==['approve'] and len(head)<32:continue
    evt={'candidate_id':'CAND-'+hashlib.sha256((cid+'|'+r['node_id']).encode()).hexdigest()[:14],
      'conversation_id':cid,'title':title,'review_group':group,'conversation_source_file':fp.name,
      'human_user_message_node_id':r['node_id'], 'preceding_ai_message_node_id':ai_prev['node_id'] if ai_prev else '',
      'interaction_context':'entry_point_no_prior_ai' if no_prior_ai else 'user_following_ai',
      'timestamp_utc':r['message_timestamp_utc'],'candidate_cues':';'.join(cues),
      'source_user_attachments':r['attachment_count'],'exposure_evidence_flags':r['exposure_evidence_flags'],
      'human_intent_status':'HEURISTIC_NOT_CODED', 'intervention_category_v1':'UNASSESSED',
      'decision_level_L0_L4':'UNASSESSED','divergence_D0_D4':'UNASSESSED',
      'exposure_E0_E5':'UNASSESSED','artifact_propagation':'UNVERIFIED',
      'persistence':'UNVERIFIED','counterfactual':'NOT_EVALUATED',
      'manual_review_status':'not_reviewed','independent_coder_1':'','independent_coder_2':'',
      'adjudication_status':'pending'}
    events.append(evt)
    if r['message_timestamp_utc']:monthly[r['message_timestamp_utc'][:7]]['heuristic_candidate_events']+=1
   all_recs.append({'conversation_id':cid,'title':title,'first_pass_tier':tier,
      'phase2_review_group':group,'created_utc':meta['created_utc'],'updated_utc':meta['updated_utc'],
      'source_json':fp.name,'mainline_messages':len(localmsgs),
      'mainline_user_messages':sum(rr['role']=='user' for rr,*_ in localmsgs),
      'alternate_user_messages':other_roles['user'],'alternate_assistant_messages':other_roles['assistant'],
      'branch_review_needed':sum(other_roles.values())>0,
      'attached_asset_references':sum(len(aa) for _,_,_,aa in localmsgs),
      'heuristic_intervention_candidates':sum(e['conversation_id']==cid for e in events),
      'source_file_matched_and_read':True,'manual_inclusion_decision':'UNASSESSED',
      'frozen_protocol_verified':'NO_FROZEN_FILES_PROVIDED'})
   if c.get('create_time'):
    monthly[iso(c['create_time'])[:7]]['flagged_conversations_created']+=1
 
 cols=lambda rr:list(rr[0]) if rr else []
 all_recs.sort(key=lambda x:(x['created_utc'],x['title']))
 msgs.sort(key=lambda x:(x['message_timestamp_utc'],x['conversation_id']))
 events.sort(key=lambda x:(x['timestamp_utc'],x['conversation_id']))
 refs.sort(key=lambda x:(x['timestamp_utc'],x['conversation_id']))
 for fn,rows in [('conversation_review_queue.csv',all_recs),('message_provenance_index.csv',msgs),
                 ('candidate_intervention_queue.csv',events),('attachment_provenance_index.csv',refs),('alternate_branch_index.csv',alt_nodes)]:
  write_csv(private/fn,rows,cols(rows))
 months=[{'month_utc':month,**{k:monthly[month].get(k,0) for k in ('flagged_conversations_created','messages_total','user_messages','user_core_mention_messages','heuristic_candidate_events')}} for month in sorted(monthly)]
 write_csv(shareable/'monthly_activity.csv',months,cols(months))
 cats=collections.Counter(r['phase2_review_group'] for r in all_recs)
 summary={'stage':'phase2_automated_provenance_not_formal_coding','source_conversations':len(unique),
   'first_pass_flagged':flagged,'prior_first_pass_A_B_C':{k:sum(r['first_pass_tier']==k for r in all_recs) for k in sorted(set(r['first_pass_tier'] for r in all_recs))},
   'review_groups':dict(cats),'mainline_user_assistant_messages':len(msgs),
   'alternate_user_assistant_messages_not_in_current_branch':alternate,
   'candidate_interaction_cues_NOT_VALIDATED':len(events),
   'attachment_references_NOT_AVAILABLE_AS_BINARIES':len(refs),
   'monthly_rows':len(months),
   'frozen_v1_protocol_files_locally_available':False,
   'baseline_31_candidate_records_file_locally_available':False,
   'raw_rosmap_data_access_proven':False,
   'findings_intervention_impact_or_persistence_proven':False,
   'substantive_cautions':['Screening reflects terms, not confirmed project membership.',
      'Candidate cues detect language, not formal acceptance/rejection or causal effects.',
      'No user/assistant bodies are included in output CSVs.',
      'E0-E5 exposure classification remains unassessed until human review.',
      'Alternate conversation branches must be reconciled before human-AI sequence coding.',
      'Artifact references do not imply artifacts were included or accessed by this pipeline.',
      'Manuscript/code artifact verification requires separate files or linked repository.',
      'Do not put PRIVATE_LOCAL_ONLY outputs into any GitHub repository.']}
 (shareable/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 (shareable/'README.md').write_text('''# Phase-2 Hsp60/10 corpus audit (metadata only)\n\nSource: 11 ChatGPT conversation JSON files in original export.\n\n**Frozen protocol V1.0 not modified or reconstructed.**\nThis is an automated candidate-queue preparation step, not final intervention coding.\nThe manifest integrity verification was completed by the prior initial audit.\n\n`monthly_activity.csv` contains only monthly counts; no conversation IDs, messages, or private filenames.\n`summary.json` contains aggregate counts and outstanding verification gaps.\n\nRun `python build_phase2.py --input /path/to/original_export --output /path/to/results`\nwith the phase-1 `hsp60_export_audit/screening_candidates.csv` present in the export root.\n\n**Never publish raw account exports, full transcripts, private source maps, participant data, controlled-access tables, credentials, or unredacted source text.**\n''')
 (target/'.gitignore').write_text('PRIVATE_LOCAL_ONLY/\nconversations-*.json\nexport_manifest.json\n*.dat\n*.zip\n')
 (private/'README_PRIVATE.md').write_text('''# LOCAL RESTRICTED SOURCE MAP — DO NOT COMMIT OR PUBLISH\n\nThis directory contains conversation IDs, message-node IDs, attachment IDs/names, and model/timestamp metadata. It does NOT contain raw message text, but is still sensitive.\n\nFiles:\n- conversation_review_queue.csv: per-thread review, includes possible unrelated conversations.\n- message_provenance_index.csv: branch-aware source locations and unvalidated exposure evidence flags.\n- candidate_intervention_queue.csv: unvalidated *language-cue* candidates, not scored or coded outcomes.\n- attachment_provenance_index.csv: recorded references only. No linked file bytes were supplied.
- alternate_branch_index.csv: unchosen branches, to avoid double counting or missed variant history.\n\nBefore independent coding: retrieve frozen protocol v1.0 and its coding manual exactly as committed, then manually label project inclusion, exposure, and evidence scope. The 31-record corpus v0.2 was not present as a separate file and cannot yet be reconciled by record ID.\n\nAutomatic cues cannot distinguish a human's independent idea from a response, and user messages can paste colleagues' text. Never present them as verified human contributions.\n''')
 print(json.dumps(summary,indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True)
 main(p.parse_args())
