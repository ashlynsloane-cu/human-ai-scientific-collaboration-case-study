#!/usr/bin/env python3
"""Corpus-completeness *discovery* after Phase 5 eligibility adjudication.

Reads an owner-restricted ChatGPT export and private review ledger. Produces
private case-level review queues and a public aggregate only. Similarity is a
review-priority statistic, NEVER a conversation eligibility decision.

This is an explicitly post-pilot retrieval expansion; do not use its scores as
independent validation of the Phase 5 pilot or as scientific impact scores.
"""
import argparse
import collections
import csv
import hashlib
import json
import math
import re
import statistics
from pathlib import Path

STOP = set('''the and for that with this from have would were while when which what
about into onto over under out our your their they them then there these
those also only like more very because just really could should need want
now can please using use its each same been being will does did done not
are has had some get got was too how why who you she he his her where do
is to of in it a an at by or on as if be we me my i us they am so but
up all one two three four any new than other results result analysis data
work working help make change update figure figures file files code script
plots plot paper manuscript review reviewer responses research study project
science scientist protein gene cells cell experiment experiments method methods
figure supplemental supplementary did like still ok okay yes no there than
question answer here add now good best right know need thanks thank ago
etc first second stage since across run running want try would like
'''.split())
WORD = re.compile(r"[a-z][a-z0-9_]{2,34}")
CONV_FILE = re.compile(r"conversations-\d{3}\.json$")
GAP_REGEX = re.compile(
    r"(?i)\b(?:figure\s*S?\d+|table\s*S?\d+|44[ -]marker|supplementary|"
    r"Braak|CERAD|MSBB|AGORA|ROSMAP|chaperonin|Hsp\s*[/ -]?\s*(?:60|10)|"
    r"HSPE1|HSPD1|MIC|DLD|DLST|TMT|MitoCarta)\b")
GROUPS = ('A_core_evidence', 'B_context_review', 'C_weak_or_ai_only',
          'out_of_scope_screen')


def read_csv(path):
    with Path(path).open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


def walk_current_branch(conversation):
    mapping = conversation.get('mapping') or {}
    current = conversation.get('current_node')
    visited, nodes = set(), []
    while current and current in mapping:
        if current in visited:
            raise ValueError('Cycle in source mapping')
        visited.add(current)
        nodes.append(mapping[current])
        current = mapping[current].get('parent')
    return list(reversed(nodes))


def text_from_message(message):
    parts = (message.get('content') or {}).get('parts')
    return '\n'.join(p for p in parts if isinstance(p, str)) if isinstance(parts, list) else ''


def token_counts(title, user, assistant):
    """Emphasize author-supplied text while using assistant text as context."""
    bag = collections.Counter()
    for source, weight, cap in ((title, 4, 300), (user, 2, 35000),
                                (assistant, 1, 16000)):
        for t in WORD.findall(source[:cap].lower()):
            if t not in STOP:
                bag[t] += weight
    return bag


def make_vectors(bags):
    """Standard-library TF-IDF; no fitted labels or outside model services."""
    n = len(bags)
    df = collections.Counter()
    for bag in bags.values():
        df.update(bag)
    weights = {}
    for key, bag in bags.items():
        vec = {token: (1 + math.log1p(freq)) *
               math.log(1 + (n + 1) / (count + 1))
               for token, freq in bag.items()
               if (count := df[token]) >= 2}
        norm = math.sqrt(sum(v*v for v in vec.values()))
        weights[key] = {k: v/norm for k, v in vec.items()} if norm else {}
    return weights


def cosine(v1, v2):
    return sum(value*v2.get(key, 0.0) for key, value in v1.items())


def neighbor_stats(vec, seed_vectors, self_key=None):
    pairs = sorted((cosine(vec, seed_vec), key)
                   for key, seed_vec in seed_vectors.items()
                   if key != self_key)
    best = pairs[-3:]
    return (round(best[-1][0], 6) if best else 0.0,
            round(statistics.mean(x[0] for x in best), 6) if best else 0.0)


def deterministic_sample(rows, n, seed, stratum):
    return sorted(rows, key=lambda r: (
        hashlib.sha256((seed+':'+stratum+':'+r['conversation_id'])
                       .encode('utf-8')).hexdigest(),
        r['conversation_id']))[:n]


def stratified_audit(rows, per_quartile, seed):
    """Equal-probability sample within deterministic priority-score quartiles."""
    ranked = sorted(rows, key=lambda r: (float(r['included_sim_max']),
                                         r['conversation_id']))
    n = len(ranked)
    result = []
    sizes = {}
    for group in range(4):
        chunk = ranked[(group*n)//4:((group+1)*n)//4]
        if len(chunk) < per_quartile:
            raise ValueError('Insufficient records for quartile sample')
        label = 'Q'+str(group+1)
        sizes[label] = len(chunk)
        for row in deterministic_sample(chunk, per_quartile, seed, label):
            rec = dict(row)
            rec['audit_probability_stratum'] = label
            rec['sampling_probability'] = f'{per_quartile}/{len(chunk)}'
            result.append(rec)
    return sorted(result, key=lambda r: r['conversation_id']), sizes


def source_excerpt(user_messages):
    if not user_messages:
        return ''
    # Favor user evidence: an assistant alone cannot establish original intent.
    msg = max(user_messages, key=lambda v: (min(len(GAP_REGEX.findall(v)), 4)*25 +
                                                  min(len(v), 700)/700))
    return re.sub(r'\s+', ' ', msg[:850]).strip()


def build(export, phase4_index, phase4_digests, pilot_file, overlay_file,
          out_private, out_public, per_quartile=20,
          seed='20261113-phase6-prospective'):
    if per_quartile < 1:
        raise ValueError('Per-quartile sample size must be positive')
    idx_rows = read_csv(phase4_index)
    idx = {r['conversation_id']: r for r in idx_rows}
    if len(idx) != len(idx_rows):
        raise ValueError('Duplicate identifiers in Phase 4 universe')
    digest_rows = read_csv(phase4_digests)
    expected_digests = {r['filename']:r['sha256'] for r in digest_rows}
    if len(expected_digests) != len(digest_rows):
        raise ValueError('Duplicate Phase 4 source digest entry')
    pilot_hash = hashlib.sha256(Path(pilot_file).read_bytes()).hexdigest()
    pilot_rows = read_csv(pilot_file)
    pilot = {r['conversation_id']: r for r in pilot_rows}
    if len(pilot) != len(pilot_rows):
        raise ValueError('Duplicate Phase 5 review identifiers')
    overlays = read_csv(overlay_file)
    revised = {}
    for r in overlays:
        cid = r['conversation_id']
        if cid not in pilot or cid in revised:
            raise ValueError('Unknown/duplicate overlay source')
        if r.get('first_pass_csv_sha256') != pilot_hash:
            raise ValueError('Overlay references a different first-pass ledger')
        if pilot[cid]['decision'] != r['locked_ai_label']:
            raise ValueError('Overlay does not match locked first-pass label')
        if r['final_label'] not in ('include', 'exclude', 'uncertain'):
            raise ValueError('Unknown overlay decision')
        revised[cid] = r['final_label']
    decisions = {cid: revised.get(cid, r['decision']) for cid, r in pilot.items()}
    filenames = sorted(p for p in export.iterdir() if CONV_FILE.fullmatch(p.name))
    manifest = json.loads((export/'export_manifest.json').read_text())
    expected = {r['path']: r['size_bytes'] for r in manifest['export_files']
                if CONV_FILE.fullmatch(r['path'])}
    if set(expected) != {p.name for p in filenames}:
        raise ValueError('Export files do not match original manifest')
    if set(expected_digests) != set(expected):
        raise ValueError('Phase 4 hash inventory does not match export files')
    rows, bags = [], {}
    for p in filenames:
        data = p.read_bytes()
        if len(data) != expected[p.name]:
            raise ValueError('Manifest byte mismatch: '+p.name)
        if hashlib.sha256(data).hexdigest() != expected_digests[p.name]:
            raise ValueError('Source SHA-256 mismatch: '+p.name)
        for conversation in json.loads(data):
            cid = conversation.get('id') or conversation.get('conversation_id')
            if cid not in idx or idx[cid]['source_file'] != p.name:
                raise ValueError('Phase 4 index source mismatch')
            title = conversation.get('title') or ''
            users, assistants = [], []
            for node in walk_current_branch(conversation):
                msg = node.get('message') or {}
                role = (msg.get('author') or {}).get('role')
                body = text_from_message(msg)
                if role == 'user':
                    users.append(body)
                elif role == 'assistant':
                    assistants.append(body)
            user, assistant = '\n'.join(users), '\n'.join(assistants)
            bags[cid] = token_counts(title, user, assistant)
            rows.append({
                'conversation_id':cid, 'source_file':p.name,
                'title_private':title,
                'created_utc':idx[cid]['created_utc'],
                'original_stratum':idx[cid]['stratum'],
                'phase5_label_or_pending':decisions.get(cid, 'not_reviewed'),
                'needs_nontext_review':idx[cid]['needs_nontext_review'],
                'alternative_branch_nodes':idx[cid]['other_branch_user_assistant_nodes'],
                'user_text_chars':len(user), 'assistant_text_chars':len(assistant),
                'user_source_excerpt_private':source_excerpt(users),
                'project_retrieval_hits_user':len(GAP_REGEX.findall(user)),
                'project_retrieval_hits_assistant':len(GAP_REGEX.findall(assistant)),
                'manual_eligibility': '', 'manual_rationale': '',
                'attachment_review_status':'UNASSESSED',
            })
    if len(rows) != len(idx) or len(bags) != len(idx):
        raise ValueError('Conversation count or uniqueness mismatch')
    vectors = make_vectors(bags)
    positives = {cid:vectors[cid] for cid,label in decisions.items()
                 if label=='include'}
    negatives = {cid:vectors[cid] for cid,label in decisions.items()
                 if label=='exclude'}
    for row in rows:
        cid = row['conversation_id']
        inc_max, inc_top = neighbor_stats(vectors[cid], positives, cid)
        exc_max, exc_top = neighbor_stats(vectors[cid], negatives, cid)
        row['included_sim_max'] = inc_max
        row['included_sim_top3'] = inc_top
        row['excluded_sim_max'] = exc_max
        row['excluded_sim_top3'] = exc_top
        row['priority_score_discovery_only'] = round(
            0.75*inc_max + 0.25*inc_top - 0.20*exc_max, 6)
        row['review_status'] = ('PILOT_REVIEWED' if cid in decisions else
                                'PENDING_FULL_CONVERSATION_REVIEW')
    remainder = [r for r in rows if r['conversation_id'] not in decisions]
    unflagged = [r for r in remainder if r['original_stratum']=='out_of_scope_screen']
    flagged = [r for r in remainder if r['original_stratum']!='out_of_scope_screen']
    unscreened_ranked = sorted(unflagged, key=lambda r: (
        -float(r['included_sim_max']), r['conversation_id']))
    flagged_ranked = sorted(flagged,
        key=lambda r:(GROUPS.index(r['original_stratum']),
                      -float(r['included_sim_max']), r['conversation_id']))
    audit, quartiles = stratified_audit(unflagged, per_quartile, seed)
    # Make the independently sampled audit blind to similarity scores, other
    # sources' labels, and rank. This packet still requires privacy clearance.
    blind = [{
        'blind_case_id':'P6-'+str(i+1).zfill(3),
        'conversation_id':r['conversation_id'],
        'source_file':r['source_file'],
        'conversation_title_private':r['title_private'],
        'source_excerpt_private':r['user_source_excerpt_private'],
        'has_nontext':r['needs_nontext_review'],
        'original_stratum_for_private_source_map':r['original_stratum'],
        'human_eligibility':'', 'human_reason':'', 'request_full_context':'',
    } for i,r in enumerate(audit)]
    out_private.mkdir(parents=True, exist_ok=True)
    out_public.mkdir(parents=True, exist_ok=True)
    review_fields=list(remainder[0])
    write_csv(out_private/'full_remainder_PRIVATE.csv', remainder, review_fields)
    write_csv(out_private/'originally_unscreened_PRIORITY_PRIVATE.csv',
              unscreened_ranked, review_fields)
    write_csv(out_private/'originally_screened_PENDING_PRIVATE.csv',
              flagged_ranked, review_fields)
    write_csv(out_private/'probability_audit_PRIVATE.csv',
              blind, list(blind[0]))
    # SHA-256 source-pointers deliberately do not appear in public files.
    aggregate={
        'phase':'phase6_postpilot_full_universe_retrieval_expansion',
        'status':'DISCOVERY_AND_AUDIT_SAMPLING_NOT_ELIGIBILITY_DECISIONS',
        'total_export_conversations':len(rows),
        'phase5_pilot_reviewed_n':len(decisions),
        'phase5_adjudicated_provisional':{
            k:sum(v==k for v in decisions.values())
            for k in ('include','exclude','uncertain')},
        'unreviewed_conversations':len(remainder),
        'first_screened_but_not_pilot_reviewed':len(flagged),
        'originally_unscreened_and_not_pilot_reviewed':len(unflagged),
        'unscreened_pending_nontext_count':sum(
            r['needs_nontext_review']=='True' for r in unflagged),
        'probability_audit':{
            'design':'stratified SHA256 stable-sample of previously unscreened '
                     'unreviewed corpus using post-pilot similarity quartiles',
            'seed':seed, 'per_similarity_quartile':per_quartile,
            'stratum_population_sizes':quartiles,
            'sample_n':len(audit),
            'denominator':len(unflagged),
            'results':'NOT_CODED',
            'sample_only_valid_for_its_own_prespecified_population':True,
            'estimator':'weighted within-quartile inclusion prevalence '
                        'and exact/binomial intervals to be designed '
                        'before interpreting sampled outcomes',
        },
        'review_prioritization':{
            'type':'post-pilot project-positive TFIDF similarity '
                   'with weak negative-control penalty',
            'using_first_pass_labels_for_discovery':True,
            'not_probability_or_eligibility_classification':True,
            'reliability_evaluation_on_phase5_pilot':'NOT_INDEPENDENT',
            'full_recall_not_established':True,
        },
        'source_visuals_exposure_E5':'UNASSESSED',
        'original_31_reconstructed_seed_records':'NOT_YET_RECONCILED',
        'steering_event_coding':'NOT_STARTED',
    }
    (out_public/'corpus_completeness_design.json').write_text(
        json.dumps(aggregate, indent=2, sort_keys=True)+'\n')
    return aggregate


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--export-dir',required=True,type=Path)
    p.add_argument('--phase4-index',required=True,type=Path)
    p.add_argument('--phase4-digests',required=True,type=Path)
    p.add_argument('--pilot-ledger',required=True,type=Path)
    p.add_argument('--adjudication-overlay',required=True,type=Path)
    p.add_argument('--out-private',required=True,type=Path)
    p.add_argument('--out-public',required=True,type=Path)
    p.add_argument('--per-quartile',type=int,default=20)
    p.add_argument('--seed',default='20261113-phase6-prospective')
    a=p.parse_args()
    print(json.dumps(build(a.export_dir,a.phase4_index,a.phase4_digests,a.pilot_ledger,
            a.adjudication_overlay,a.out_private,a.out_public,
            a.per_quartile,a.seed),indent=2))


if __name__=='__main__':
    main()
