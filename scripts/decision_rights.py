#!/usr/bin/env python3
"""Phase 1: decision-rights inventory from the seven GTA documents only.

Run: python3 -I decision_rights.py <stage1_inventory.json> <stage2_map.json> <out.json> <out.md>
Every role is quoted from a provision's text; the build fails if a quote is not in the provision.
"""
import json, re, sys, collections

inv = json.load(open(sys.argv[1])); mp = json.load(open(sys.argv[2]))
P = {p['id']: p for p in inv['provisions']}
norm = lambda t: re.sub(r'\s+', ' ', t or '')
EL = {i: e for e in mp['elements'] for i in e['provision_ids']}
PTR = collections.defaultdict(list)
for q in mp['indirect_pointers']:
    for i in q['provision_ids']: PTR[i].append(q)


def cite(i):
    p = P[i]
    ident = p['doc_id'] if p['doc_id'] != '5GP' else 'no identifier'
    return f"{p['doc_title']} ({ident}), {p['section']}, p.{p['page']}"


def shown(i):
    e = EL[i]
    if e['tier'] in ('umbrella', 'conditional'):
        return dict(via=e['id'], kind='topic', when=e['activated_by'])
    if PTR[i]:
        return dict(via=PTR[i][0]['id'], kind='agency pointer', when=PTR[i][0]['show_when'])
    return None


def R(kind, quote, pid):
    """kind: decides | reviews | consulted | asks"""
    src = norm((P[pid]['lead_in_excerpt'] or '') + ' ' + P[pid]['text_excerpt'])
    assert norm(quote) in src, (pid, quote)
    return collections.OrderedDict(part=kind, role_as_written=quote, provision_id=pid, modal_as_written=P[pid]['modal_as_written'],
                                   citation=cite(pid), shown_today=shown(pid))


RECS = []


def D(did, decision, dtype, roles, status, note, channel=None, timing=None, conflicts=(), oqs=(), urs=()):
    assert status in ('named', 'documents_disagree', 'not_named')
    if channel:
        q, pid = channel
        assert norm(q) in norm(P[pid]['text_excerpt']), (did, q)
        channel = dict(as_written=q, provision_id=pid)
    if timing:
        q, pid = timing
        assert norm(q) in norm((P[pid]['lead_in_excerpt'] or '') + ' ' + P[pid]['text_excerpt']), (did, q)
        timing = dict(as_written=q, provision_id=pid)
    anchors = [r['provision_id'] for r in roles]
    level = 'employee' if any(EL[i]['tier'] in ('umbrella', 'conditional') for i in anchors) else 'agency'
    RECS.append(collections.OrderedDict(id=did, decision=decision, decision_type=dtype, level=level, roles=roles,
        who_decides_status=status, status_note=note, channel=channel, timing_as_written=timing,
        conflicts=list(conflicts), open_questions=list(oqs), unresolved_references=list(urs)))


D("DR-01", "Entering PII, PHI, regulated, confidential or sensitive data into an AI tool", "approval",
  [R("decides", "GTA’s Office of Artificial Intelligence", "SS-25-001-1.3-2"),
   R("decides", "appropriate agency authority", "SS-23-002-6-2"),
   R("decides", "Georgia Technology Authority", "GS-25-001-RUBRIC-6"),
   R("consulted", "department's data privacy officer or designated compliance authority", "GS-25-001-SAFE-15")],
  "documents_disagree", "Three provisions name three different approvers. No document gives a request process.",
  conflicts=["C04"], oqs=["OQ09"], urs=["UR12", "UR27"])
D("DR-02", "Using a personal email address to access GenAI tools for state business", "authorization",
  [R("decides", "agency’s technology leadership", "SS-25-001-1.4-2")],
  "named", "The role is named but not identified; the documents do not say who holds it in an agency.", conflicts=["C05"], urs=["UR27"])
D("DR-03", "Procuring a GenAI product or service", "approval",
  [R("decides", "Georgia Technology Authority (GTA)", "SS-25-001-1.5-1"),
   R("consulted", "GTA Office of Artificial Intelligence", "SS-25-001-1.5-4")],
  "named", "GTA is named; the office within GTA that approves is not. The 2023 documents describe other review routes (DR-04).",
  channel=("https://ai.georgia.gov/ai-application-and-tool-request-form", "SS-25-001-1.5-1"),
  timing=("approved in advance", "SS-25-001-1.5-1"), conflicts=["C08"], oqs=["OQ07"], urs=["UR10"])
D("DR-04", "Review of any AI software, application, tool or service before procurement", "review",
  [R("asks", "Agencies shall submit", "PS-23-001-POLICY-1"),
   R("reviews", "GTA for review", "PS-23-001-POLICY-1"),
   R("reviews", "GTA will assess the tool for safety, privacy, and compliance", "SS-23-002-3-2"),
   R("decides", "The State CIO will provide a response to the senior executive of the requesting agency", "SS-23-002-3-3")],
  "named", "The documents describe a review and a response from the State CIO. They do not call the response an approval.",
  channel=("Business Solutions Review (BSR) Request form to GTA via email", "SS-23-002-3-1"),
  timing=("prior to procurement", "PS-23-001-POLICY-1"), conflicts=["C02", "C03", "C08"], oqs=["OQ01", "OQ17", "OQ29"], urs=["UR11"])
D("DR-05", "Purchasing a premium version of a GenAI tool", "discretion",
  [R("decides", "Individual agencies", "SS-25-001-STD-3")],
  "named", "Agencies 'retain discretion'. How this fits with GTA's advance approval of any GenAI procurement (DR-03) is not stated.",
  oqs=["OQ07"])
D("DR-06", "Setting additional agency restrictions on GenAI use", "determination",
  [R("decides", "Agencies", "SS-25-001-STD-4"),
   R("consulted", "Georgia Technology Authority (GTA)", "SS-25-001-STD-5")],
  "named", "Agencies set the restrictions and 'should first consult' GTA.", oqs=["OQ08"], urs=["UR31"])
D("DR-07", "Conditional Approval for a specific use case of a GenAI tool", "approval",
  [R("asks", "can be requested", "SS-25-001-3.0-APPROVAL-1")],
  "not_named", "The provision gives where to send the request. It does not say who grants it, or which uses need it.",
  channel=("ai.georgia.gov or email ai@gta.georgia.gov", "SS-25-001-3.0-APPROVAL-1"), oqs=["OQ10"], urs=["UR13"])
D("DR-08", "Reviewing AI-generated content before it is used", "review",
  [R("decides", "qualified personnel", "SS-25-001-1-1"),
   R("decides", "business owner or designated personnel", "SS-23-002-5-4")],
  "documents_disagree", "SS-25-001 defines Qualified Personnel as the subject-matter employee who would otherwise be responsible for the content; SS-23-002 names the business owner or designated personnel, and a different trigger.",
  timing=("before being used in any official capacity", "SS-25-001-1-1"), conflicts=["C13"], oqs=["OQ09", "OQ25"])
D("DR-09", "Which AI tools, vendors and versions employees may use", "vetting",
  [R("decides", "GTA has vetted", "GS-25-001-SAFE-1"),
   R("consulted", "consult with GTA", "GS-25-001-SAFE-4")],
  "named", "GTA vets tools and vendors. Approval is per version and 'can always' be revoked; who revokes is not stated. No list of vetted tools is in the document set.",
  oqs=["OQ07"], urs=["UR14"])
D("DR-10", "Admitting a project to the Horizons Innovation Lab sandbox", "approval",
  [R("asks", "agencies shall", "SS-25-001-2.2-1")],
  "not_named", "Agencies submit a proposal. The documents do not say who accepts or declines it.",
  channel=("https://ai.georgia.gov/innovation-lab/how-do-i-submit-project-innovation-lab", "SS-25-001-2.2-1"), urs=["UR17"])
D("DR-11", "Security vetting of a tool tested in the sandbox", "vetting",
  [R("decides", "GTA Office of Information Security or the agency’s Information Security Officer", "SS-25-001-2.3-1")],
  "named", "Either of two roles may vet; the documents do not say which one applies when.", urs=["UR17", "UR27"])
D("DR-12", "Using sensitive or PII datasets in the sandbox", "approval",
  [R("asks", "unless otherwise approved", "SS-25-001-2.3-2")],
  "not_named", "The provision allows an exception 'unless otherwise approved' and names no approver.", conflicts=["C04"], urs=["UR17"])
D("DR-13", "Moving a sandbox project into pilot or production", "approval",
  [R("asks", "agencies shall seek approval", "SS-25-001-2.5-1"),
   R("reviews", "Review Sandbox reports and risk assessments", "SS-25-001-2.5-2")],
  "not_named", "Agencies 'shall seek approval'; the approver is not named. The next lines say GTA will review Sandbox reports and risk assessments.",
  timing=("Following successful sandbox evaluation", "SS-25-001-2.5-1"), urs=["UR17"])
D("DR-14", "Going ahead with a novel, high-risk or ambiguous use case", "consultation",
  [R("reviews", "Agencies should conduct their own risk assessments", "SS-25-001-3.0-4"),
   R("consulted", "Georgia Technology Authority (GTA) Office of Artificial Intelligence", "SS-25-001-3.0-4")],
  "not_named", "Agencies assess the risk and consult the Office of AI. The documents do not say who decides whether the use goes ahead.",
  oqs=["OQ09", "OQ10"])
D("DR-15", "Recording or transcribing a virtual meeting", "determination",
  [R("decides", "Meeting hosts", "GS-25-001-MEET-11")],
  "named", "Meeting hosts are 'responsible for determining the need for recordings and automated transcriptions'.", oqs=["OQ12"])
D("DR-16", "Legal or regulatory analysis with GenAI", "oversight",
  [R("decides", "legal staff", "SS-25-001-3.0-TABLE-29")],
  "named", "The table's Conditional cell requires 'legal staff oversight'; it does not say which legal staff.", oqs=["OQ10"])
D("DR-17", "Ordering an AI tool to stop being used", "order",
  [R("decides", "The State CIO or GTA OIS", "SS-23-002-10-1")],
  "named", "Either may order termination of use.", urs=["UR27"])
D("DR-18", "Further investigation of reported misuse, and deviation from corrective action", "determination",
  [R("decides", "GTA OIS determines", "SS-23-002-8-4"),
   R("decides", "subject to GTA OIS’s approval", "SS-23-002-8-6")],
  "named", "GTA OIS decides whether further investigation is warranted and approves any deviation.", conflicts=["C10"], oqs=["OQ19"], urs=["UR27"])
D("DR-19", "Revoking tool access for not following SS-25-001 requirements", "order",
  [R("decides", "revocation of tool access and additional oversight actions by GTA", "SS-25-001-1.7-5")],
  "named", "GTA is named for oversight actions; which requirements the sentence covers is an open question.", oqs=["OQ18"])

EXCLUDED = [
 "Reporting duties (incidents, misuse, development risks, inventories) are routes for information, not decisions; see next_steps_scan.md.",
 "The guiding-principle items and GS-25-002 name no decider for any step.",
 "Roles, bodies and documents outside the seven documents (for example SM-14-008, the State CTO, EPMO, DOAS, OPB, an Executive Decision-Making Board) are not included.",
]
counts = collections.Counter(r['who_decides_status'] for r in RECS)
out = collections.OrderedDict(
    title="Decision rights in the GTA AI documents",
    scope="Built only from the seven documents in the project. Roles are quoted as written and are not mapped to named people.",
    status_values={"named": "A provision names who decides.", "documents_disagree": "Provisions name different deciders.", "not_named": "A decision or approval is required or offered, and no provision names who makes it."},
    counts=dict(decisions=len(RECS), **counts, employee_level=sum(r['level'] == 'employee' for r in RECS), agency_level=sum(r['level'] == 'agency' for r in RECS),
                not_reached_by_any_question=sum(all(x['shown_today'] is None for x in r['roles']) for r in RECS)),
    decisions=RECS, excluded=EXCLUDED)
json.dump(out, open(sys.argv[3], 'w'), indent=1, ensure_ascii=False)

ST = {"named": "Named", "documents_disagree": "Documents disagree", "not_named": "Not named"}
L = ["# Decision rights in the GTA AI documents (Phase 1 inventory, for review)", "",
     "Rendered from `decision_rights.json`. Built only from the seven documents. Roles are quoted as written.", "",
     f"{len(RECS)} decision points: {counts['named']} named, {counts['documents_disagree']} where the documents disagree, {counts['not_named']} not named.", ""]
for r in RECS:
    L += [f"## {r['id']}: {r['decision']}", "", f"- **Who decides:** {ST[r['who_decides_status']]}. {r['status_note']}",
          f"- **Type:** {r['decision_type']}; **level:** {r['level']}"]
    for x in r['roles']:
        sh = x['shown_today']
        L.append(f"- {x['part'].capitalize()}: “{x['role_as_written']}” ({x['citation']}; modal as written: {x['modal_as_written']}). " +
                 (f"Shown today via `{sh['via']}`." if sh else "Not shown by the tool today."))
    if r['channel']: L.append(f"- Channel: “{r['channel']['as_written']}”")
    if r['timing_as_written']: L.append(f"- Timing: “{r['timing_as_written']['as_written']}”")
    refs = r['conflicts'] + r['open_questions'] + r['unresolved_references']
    if refs: L.append(f"- See: {', '.join(refs)}")
    L.append("")
L += ["## Left out", ""] + [f"- {e}" for e in EXCLUDED]
open(sys.argv[4], 'w').write("\n".join(L) + "\n")
print(json.dumps(out['counts']))
for r in RECS: print(r['id'], r['who_decides_status'], r['level'], [x['shown_today']['via'] if x['shown_today'] else None for x in r['roles']])
