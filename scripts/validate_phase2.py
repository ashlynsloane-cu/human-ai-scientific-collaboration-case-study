"""Validate metadata integrity and source-pointer consistency for Phase 2."""
import argparse,csv,json
from pathlib import Path


def rows(p):
    with p.open(newline='',encoding='utf-8') as f: return list(csv.DictReader(f))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();root=Path(args.output)
    p=root/'PRIVATE_LOCAL_ONLY'; s=root/'REPO_SAFE'
    rev=rows(p/'conversation_review_queue.csv')
    msgs=rows(p/'message_provenance_index.csv')
    alts=rows(p/'alternate_branch_index.csv')
    evt=rows(p/'candidate_intervention_queue.csv')
    atts=rows(p/'attachment_provenance_index.csv')
    samples=rows(p/'manual_spot_checks_provisional.csv')
    rescues=rows(p/'out_of_scope_rescue_candidates.csv')
    summary=json.loads((s/'summary.json').read_text())
    ptr={(r['conversation_id'],r['node_id']):r for r in msgs}
    aptr={(r['conversation_id'],r['node_id']):r for r in alts}
    review={r['conversation_id'] for r in rev}
    checks={
     'source_conversations_unique':len(review)==len(rev)==291,
     'lexical_rescue_disjoint_from_first_screen':len(rescues)==5 and all(r['conversation_id'] not in review for r in rescues),
     'mainline_nodes_unique':len(ptr)==len(msgs)==14235,
     'alternate_nodes_unique':len(aptr)==len(alts)==194,
     'mainline_alt_disjoint':not (ptr.keys() & aptr.keys()),
     'every_message_source_in_review':all(r['conversation_id'] in review for r in msgs),
     'every_event_user_node_resolves':all((r['conversation_id'],r['human_user_message_node_id']) in ptr and ptr[r['conversation_id'],r['human_user_message_node_id']]['role']=='user' for r in evt),
     'every_event_ai_pointer_resolves':all(not r['preceding_ai_message_node_id'] or ((r['conversation_id'],r['preceding_ai_message_node_id']) in ptr and ptr[r['conversation_id'],r['preceding_ai_message_node_id']]['role']=='assistant') for r in evt),
     'candidate_ids_unique':len(set(r['candidate_id'] for r in evt))==len(evt),
     'event_count_matches_summary':len(evt)==summary['candidate_interaction_cues_NOT_VALIDATED'],
     'attachment_count_matches_summary':len(atts)==summary['attachment_references_NOT_AVAILABLE_AS_BINARIES'],
     'spot_check_source_nodes_resolve':len(samples)==6 and all((r['conversation_id'],r['user_node_id']) in ptr for r in samples),
     'all_codes_unassessed':all(r['intervention_category_v1']=='UNASSESSED' and r['exposure_E0_E5']=='UNASSESSED' for r in evt),
     'all_artifact_implementation_unverified':all(r['artifact_propagation']=='UNVERIFIED' for r in evt),
     'no_raw_message_body_field':not any(any(x in key.lower() for x in ('message_body','raw_excerpt','full_text','raw_message_text')) for key in msgs[0]),
    }
    output={'all_passed':all(checks.values()),'checks':checks,'counts':{
      'review_queue':len(rev),'mainline_messages':len(msgs),'alternate_messages':len(alts),
      'candidate_events':len(evt),'attachment_references':len(atts),'spot_checks':len(samples),'lexical_rescue_candidates':len(rescues)}}
    (s/'validation_report.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))
    if not output['all_passed']:raise SystemExit(1)

if __name__=='__main__':main()
