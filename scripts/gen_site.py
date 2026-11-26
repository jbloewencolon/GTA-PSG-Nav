import json, sys, os
INV, MAP, TRI, OUTDIR, DR = sys.argv[1:6]
inv = json.load(open(INV, encoding='utf-8')); mp = json.load(open(MAP, encoding='utf-8')); tri = json.load(open(TRI, encoding='utf-8'))
P = {p['id']: p for p in inv['provisions']}
URL = {d['doc_id']: d.get('source_url') for d in inv['documents']}
DT = {'policy': 'Policy', 'standard': 'Standard', 'guideline': 'Guideline', 'other': 'Web page'}
DTYPE = {d['doc_id']: DT[d['document_type']] for d in inv['documents']}
DTNOTE = {'SS-25-001': 'Shown as a standard: its body is headed STANDARD, but its header number is PS-25-001 and its Purpose calls it a policy (conflict C01).',
          '5GP': 'A GTA Office of Artificial Intelligence web page with no policy, standard or guideline label.'}
MEL = {e['id']: e for e in mp['elements']}; MPT = {p['id']: p for p in mp['indirect_pointers']}

def prov(i):
    p = P[i]
    return dict(id=i, x=p['text_excerpt'], lead=p['lead_in_excerpt'], doc=p['doc_title'], docid=(p['doc_id'] if p['doc_id'] != '5GP' else None),
                sec=p['section'], pg=p['page'], aw=p['modal_as_written'], url=URL[p['doc_id']],
                mod=p['modality'], dt=DTYPE[p['doc_id']], dtn=DTNOTE.get(p['doc_id']))
def el(e, tier, when):
    me = MEL[e['id']]
    sts = []
    for s, ms in zip(e['statements'], me['statements']):
        assert s['modality'] == ms['modality']
        sts.append(dict(m=s['modality'], summary=s['summary'], prov=[prov(i) for i in ms['provision_ids']]))
    osts = [dict(m=s['modality'], summary=s['summary'], prov=[prov(i) for i in s['provision_ids']]) for s in e['other_ai_statements']]
    return dict(k='el', id=e['id'], title=e['title'], tier=tier, when=when, statements=sts, other=osts, conflicts=e['conflicts'], oqs=e['open_questions'])
def ptr(p, when):
    return dict(k='ptr', id=p['id'], when=when, as_written=p['as_written'], pointer=p['employee_pointer'], prov=[prov(i) for i in MPT[p['id']]['provision_ids']],
                o_as_written=p['other_ai_as_written'], oprov=[prov(i) for i in p['other_ai_provision_ids']], conflicts=p['conflicts'], oqs=p['open_questions'])
oc = tri['outcomes']
import datetime as _dt
UPD = os.environ.get('NAV_UPDATED') or _dt.date.today().isoformat()
_d = _dt.date.fromisoformat(UPD)
updated = dict(iso=UPD, text=f"{_d.day} {_d.strftime('%B %Y')}", basis='Content comes from seven GTA AI policy, standard and guideline documents. Each source shows its own dates')
def _date(s):
    """'7/1/2025', '12/12/23' or '7/21/26, 6:13 PM (...)' -> ('2025-07-01', '1 July 2025'); None -> None."""
    if not s: return None
    m, d_, y = (int(x) for x in s.split(',')[0].split('/'))
    d = _dt.date(y + 2000 if y < 100 else y, m, d_)
    return dict(iso=d.isoformat(), text=f"{d.day} {d.strftime('%B %Y')}")
# Per-document dates, shown with each citation: effective date as printed, and when the copy used here was captured (where known).
DOCDATES = {d['doc_id']: dict(eff=_date(d['effective_date']), cap=_date(d['printed_or_captured'])) for d in inv['documents']}
recs = [dict(k='meta', updated=updated, docs=DOCDATES, closing=oc['closing_line'], gate=dict(when=oc['scope_gate']['when'], text=oc['scope_gate']['outcome']['text'], note=oc['scope_gate']['outcome']['unresolved_note'], cites=oc['scope_gate']['outcome']['citations']),
             when_other=oc['type_rule']['when_other'], notes=[dict(id=n['id'], when=n['when'], text=n['note']['text'], cites=n['note']['citations']) for n in oc['type_notes']])]
# F_TASK takes several answers at once; results are the union of what each chosen value triggers (see tests/test_multi.py)
MULTI = {'F_TASK'}
for q in tri['questions']:
    recs.append(dict(k='q', id=q['id'], fact=q['fact_id'], text=q['text'], help=q['help_text'], ask_if=q['ask_if'], **({'multi': True} if q['fact_id'] in MULTI else {}),
                     options=[dict(label=o['label'], value=list(o['sets_fact'].values())[0], not_sure=bool(o.get('not_sure')), confirm=o.get('confirm_pointer')) for o in q['options']]))
o = tri['outcomes']
recs += [el(e, 'umbrella', 'always') for e in o['always']['umbrella_elements']]
recs += [el(b['element'], 'conditional', b['when']) for b in o['blocks']]
recs += [ptr(p, 'always') for p in o['always']['indirect_pointers']]
recs += [ptr(b['pointer'], b['when']) for b in o['conditional_pointers']]
# ---- next steps: provisions that name an action and somewhere to take it (see next_steps_scan.md) ----
# A step is shown only when its provision is shown on the path. 'quote' must appear verbatim in the source.
import re as _re
_TXT = {'SS-23-002': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'source_text', 'SS-23-002.txt')}
def _norm(t): return _re.sub(r'\s+', ' ', t)
STEPS = [
 ('you', 'SS-25-001-3.0-APPROVAL-1', 'Request Conditional Approval for a specific use case', 'ai.georgia.gov or email ai@gta.georgia.gov', [['ai.georgia.gov', 'https://ai.georgia.gov'], ['ai@gta.georgia.gov', 'mailto:ai@gta.georgia.gov']], None, None),
 ('you', 'SS-25-001-1.5-1', 'GTA approval before buying a GenAI product or service', 'https://ai.georgia.gov/ai-application-and-tool-request-form', [['Review form', 'https://ai.georgia.gov/ai-application-and-tool-request-form']], None, 'Other documents describe other routes for pre-procurement review (conflict C08).'),
 ('you', 'SS-25-001-1.3-2', 'Approval route for entering PII, PHI or other regulated data', 'GTA’s Office of Artificial Intelligence', [], None, 'The documents give no request process (unresolved reference UR12), and other documents name other approvers (conflict C04).'),
 ('you', 'GS-25-001-SAFE-15', 'If you are unsure whether data may be entered', "department's data privacy officer or designated compliance authority", [], None, 'The documents do not say who this is in your agency (UR27).'),
 ('you', 'SS-25-001-1.4-2', 'Exception route for using a personal email address', 'agency’s technology leadership', [], None, 'The documents do not say who this is in your agency (UR27).'),
 ('you', 'GS-25-001-SAFE-4', 'Consult GTA about compliant versions of AI tools', 'consult with GTA', [], None, 'The documents give no contact for this.'),
 ('you', 'SS-23-002-9-10', 'Report risks or ethical concerns in AI development or collaboration', 'agency’s designated Ethics Officer, CIO, and State CIO', [], None, 'The documents do not say who these people are in your agency (UR27).'),
 ('agency', 'SS-25-001-2.2-1', 'Propose a project to the Horizons Innovation Lab', 'https://ai.georgia.gov/innovation-lab/how-do-i-submit-project-innovation-lab', [['Project submission form', 'https://ai.georgia.gov/innovation-lab/how-do-i-submit-project-innovation-lab']], None, 'Participation is voluntary: the requirements apply to agencies that choose to participate.'),
 ('agency', 'SS-25-001-2.5-1', 'Seek approval to move a sandbox project into pilot or production', None, [], None, 'The documents do not say whom to ask.'),
 ('agency', 'SS-25-001-1.5-4', 'Consult the GTA Office of AI before a GenAI contract', 'GTA Office of Artificial Intelligence', [], None, None),
 ('agency', 'PS-23-001-POLICY-1', 'Submit AI tools to GTA for review before procurement', 'GTA', [], None, 'No channel is given here; see conflict C08.'),
 ('agency', 'SS-23-002-3-1', 'Submit a Business Solutions Review (BSR) request before procurement', 'gta.psg@gta.ga.gov', [['gta.psg@gta.ga.gov', 'mailto:gta.psg@gta.ga.gov']], 'Artificial Intelligence Responsible Use (SS-23-002), 3. Procuring AI Solutions, p.5 (same sentence)', None),
 ('agency', 'SS-25-001-3.0-4', 'Consult the GTA Office of AI on novel, high-risk or ambiguous uses', 'Georgia Technology Authority (GTA) Office of Artificial Intelligence', [], None, None),
 ('agency', 'SS-25-001-4.0-2', 'Report significant GenAI incidents within 48 hours', 'GTA Office of AI', [], None, None),
 ('agency', 'SS-23-002-8-2', 'Report suspected misuse of AI systems', 'agency CIO or senior executive and GTA OIS', [], None, None),
]
for who, pid, title, quote, links, qcite, note in STEPS:
    p = P[pid]
    if quote:
        src = _norm(p['text_excerpt']) if not qcite else _norm(open(_TXT[p['doc_id']]).read())
        assert _norm(quote) in src, (pid, quote)
    for _, u in links:
        uu = u.replace('mailto:', '').replace('https://', '')
        assert uu in (_norm(p['text_excerpt']) + ' ' + (_norm(open(_TXT[p['doc_id']]).read()) if qcite else '')), (pid, u)
    recs.append(dict(k='step', who=who, pid=pid, title=title, quote=quote, links=links, qcite=qcite, note=note, prov=prov(pid)))

# ---- who decides: from decision_rights.json (roles already verified against their provisions) ----
dr = json.load(open(DR, encoding='utf-8'))
CF = {c['id']: c['plain_statement'] for c in mp['conflicts']}
UR = {u['id']: u['reference'] for u in mp['unresolved_references']}
PART = {'decides': 'Decides', 'consulted': 'Consulted', 'asks': 'Asks', 'reviews': 'Reviews'}
FORCE = {'DR-11': 'P_SANDBOX', 'DR-12': 'P_SANDBOX'}   # no question reaches these; shown to people who build (P_SANDBOX), generative AI only
NEVER = {'DR-17', 'DR-18'}                              # enforcement by the State CIO or GTA OIS; no answer triggers them
decs = []
for d in dr['decisions']:
    if d['id'] in NEVER: continue
    roles = []
    for r in d['roles']:
        pr = prov(r['provision_id'])
        assert r['role_as_written'].replace('’', "'") in ((P[r['provision_id']]['lead_in_excerpt'] or '') + ' ' + P[r['provision_id']]['text_excerpt']).replace('’', "'"), (d['id'], r['role_as_written'])
        roles.append(dict(part=PART[r['part']], role=r['role_as_written'], pid=r['provision_id'], prov=pr))
    decs.append(dict(k='dec', id=d['id'], decision=d['decision'], level=d['level'], status=d['who_decides_status'], note=d['status_note'], roles=roles,
                     force=FORCE.get(d['id']), conflicts=[dict(id=c, plain=CF[c]) for c in d['conflicts']],
                     urs=[dict(id=u, ref=UR[u]) for u in d['unresolved_references']]))
recs += decs
STEPDEC = {'SS-25-001-3.0-APPROVAL-1': 'DR-07', 'SS-25-001-1.5-1': 'DR-03', 'SS-25-001-1.3-2': 'DR-01', 'GS-25-001-SAFE-15': 'DR-01',
           'SS-25-001-1.4-2': 'DR-02', 'GS-25-001-SAFE-4': 'DR-09', 'SS-25-001-2.2-1': 'DR-10', 'SS-25-001-2.5-1': 'DR-13',
           'SS-25-001-1.5-4': 'DR-03', 'PS-23-001-POLICY-1': 'DR-04', 'SS-23-002-3-1': 'DR-04', 'SS-25-001-3.0-4': 'DR-14'}
DD = {x['id']: x for x in decs}
for pid, did in STEPDEC.items():
    assert any((P[r['pid']]['doc_id'], P[r['pid']]['section']) == (P[pid]['doc_id'], P[pid]['section']) for r in DD[did]['roles']), (pid, did)
for r in recs:
    if r['k'] == 'step': r['dec'] = STEPDEC.get(r['pid'])

recs.append(dict(k='stepgap', text="No document tells an individual employee whom to notify about an incident or suspected misuse. The reporting duties are written for agencies (open question OQ19)."))

# ---- guardrails: risk factors and signs (see AUDIT.md §3-4; tests/test_score.py checks every path) ----
# The post values are this tool's, not GTA's. A factor raises posts once, using the first variant whose
# 'when' matches; each variant quotes one provision per AI branch (None = not on that branch).
NS = 'not_sure'
FACTORS = [
 ('data', 2, [([{'F_DATA': ['yes', NS]}], 'You will enter personal or sensitive information', 'SS-25-001-1.3-2', 'SS-23-002-6-2')]),
 ('decision', 2, [([{'F_DECISION': ['yes', NS]}], 'The output feeds a decision about a person', 'SS-25-001-3.0-TABLE-15', None)]),
 ('public', 1, [([{'F_TASK': ['chatbot_public']}], 'Members of the public interact with it', 'SS-25-001-3.0-TABLE-5', None),
                ([{'F_TASK': ['public_comms', NS]}], 'The public will see what it produces', 'SS-25-001-3.0-TABLE-6', None)]),
 ('role', 1, [([{'F_ROLE': ['procure', 'both', NS]}], 'You are helping to buy an AI tool', 'SS-25-001-1.5-1', 'PS-23-001-POLICY-1'),
              ([{'F_ROLE': ['build']}], 'You are helping to build an AI tool', 'SS-23-002-9-7', 'SS-23-002-9-7')]),
 ('official', 1, [([{'F_PRODUCT': ['official', NS]}], 'AI content will appear in an official document', 'GS-25-001-CITE-7', None)]),
 ('oversight', 1, [([{'F_TASK': ['legal', NS]}], 'Legal or regulatory analysis needs legal staff oversight', 'SS-25-001-3.0-TABLE-29', None),
                   ([{'F_TASK': ['meetings']}], 'AI note-taking in meetings is strongly discouraged', 'GS-25-001-MEET-1', None)]),
]
HR = 'an HR department may consult with AI platforms in making hiring decisions'
assert HR in P['GS-25-001-SAFE-9']['text_excerpt']
# 'stop': a provision requires GTA approval or lists the use as prohibited. 'check': a provision requires a review
# or authorization first. Branch 'gen' is shown unless the answers take the other-AI branch; 'other' only on it.
SIGNS = [
 ('stop', 'gen', [{'F_DATA': ['yes', NS]}], 'SS-25-001-1.3-2', 'GTA approval needed: personal or regulated data', None),
 ('stop', 'gen', [{'F_ROLE': ['procure', 'both', NS]}], 'SS-25-001-1.5-1', 'GTA approval needed: buying a GenAI product or service', None),
 ('stop', 'gen', [{'F_DECISION': ['yes', NS]}], 'SS-25-001-3.0-TABLE-15', 'May be prohibited: decisions about people (the documents disagree)',
  f'SS-25-001 lists this under Prohibited in its use-case table, but GS-25-001 gives this example: “{HR}” (open question OQ13).'),
 ('check', 'other', [{'F_ROLE': ['procure', 'both', NS]}], 'PS-23-001-POLICY-1', 'GTA review needed before buying an AI tool', None),
 ('check', 'other', [{'F_DATA': ['yes', NS]}], 'SS-23-002-6-2', 'Authorization needed: personal or sensitive data',
  'The documents do not say who the “appropriate agency authority” is.'),
]
for fid, posts, variants in FACTORS:
    recs.append(dict(k='factor', id=fid, posts=posts, variants=[dict(when=w, reason=r, prov=prov(g), oprov=prov(o) if o else None) for w, r, g, o in variants]))
for level, branch, when, pid, title, note in SIGNS:
    assert level in ('stop', 'check') and branch in ('gen', 'other')
    assert (P[pid]['doc_id'] in mp['ai_type_rule']['generative_only_documents']) <= (branch == 'gen'), pid
    recs.append(dict(k='sign', level=level, branch=branch, when=when, pid=pid, title=title, note=note, prov=prov(pid)))
os.makedirs(OUTDIR, exist_ok=True)
with open(os.path.join(OUTDIR, 'data.json'), 'w', encoding='utf-8') as f:
    f.write('[\n' + ',\n'.join(json.dumps(r, ensure_ascii=False) for r in recs) + '\n]\n')
json.load(open(os.path.join(OUTDIR, 'data.json'), encoding='utf-8'))
print(len(recs), 'records', os.path.getsize(os.path.join(OUTDIR, 'data.json')), 'bytes')
