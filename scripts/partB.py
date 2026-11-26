import json, sys, collections, itertools
MAP, OUTJ, MAXQ = sys.argv[1], sys.argv[2], int(sys.argv[3])
m = json.load(open(MAP, encoding='utf-8'))
EL = {e['id']: e for e in m['elements']}
FACT = {f['id']: f for f in m['facts']}
PTR = {p['id']: p for p in m['indirect_pointers']}

def match(cond, facts):
    if cond == "always": return True
    if cond == "not_applicable": return False
    return any(all(facts.get(f) in vals for f, vals in c.items()) for c in cond)

# ---------- ordering ----------
def ruleout(fid):
    dep = [e for e in m['elements'] if e['tier'] == 'conditional' and any(fid in c for c in e['activated_by'])]
    vals = [v['value'] for v in FACT[fid]['values']]
    tot = 0
    for v in vals:
        tot += sum(1 for e in dep if not any(v in c.get(fid, []) for c in e['activated_by']))
    return round(tot / len(vals), 2), len(dep)
GATES = [f for f in FACT if FACT[f].get('gate')]
scores = {f: ruleout(f) for f in FACT if f not in GATES}
order = GATES + sorted(scores, key=lambda f: -scores[f][0])
RULE = m['ai_type_rule']
GENLIKE = ["generative", "not_sure"]; ALLTYPES = [v['value'] for v in FACT['F_TYPE']['values'] if v['value'] != "none"]

TEXT = {
 "F_TYPE": ("What kind of AI is it?", "SS-25-001 defines generative AI as “tools or systems used to create models that can generate new and original content, such as images, music, or text, based on patterns and examples from existing data.” SS-23-002 also defines machine learning and deep learning. None of the documents mentions AI agents; they are grouped with “Other AI”, but if an agent creates new content, choose Generative AI. If you are asking about something with no AI in it, such as an ordinary cloud application, choose “It does not use AI”."),
 "F_TASK": ("What best describes what you are using the generative AI tool for this time?", "“Generative AI” means tools “that can generate new and original content, such as images, music, or text” (SS-25-001), for example ChatGPT, Gemini, Claude or Copilot."),
 "F_PRODUCT": ("Will anything the AI wrote or came up with appear in what you finally produce?", "GS-25-001 counts AI content as part of your product “when a substantial portion of the content is featured in the final product, even if the user extensively edits it.” If it only helped you develop your own content and ideas, answer No. The documents give “an email” as the example of an informal document and do not define “more official documents”."),
 "F_ROLE": ("Besides using the tool yourself, are you also helping to buy an AI tool or to build one?", "Buying includes licensing, contracting, an RFP, or a paid or premium version. Building includes configuring, piloting or deploying an AI tool, or developing one with an outside partner."),
 "F_DATA": ("Will you type, paste or upload into the tool any information about identifiable people, health information, personal records, or confidential or private state information?", "The documents speak of “Personally identifiable information (PII), protected health information (PHI), or other regulated data”, “confidential or private state information, or personal records”, and give “biometrics and financial data” as examples. They do not define these terms."),
 "F_DECISION": ("Will what the AI produces be used to make, or help make, a decision about a specific person?", "Examples the documents name: hiring, legal, disciplinary or eligibility decisions, and assessing employee performance. SS-25-001 calls a use high-risk when it has “potential impact on legal rights, access to benefits, public safety, or public trust.”"),
 "F_HOST": ("Are you the host of the virtual meeting?", "The host is the person running the meeting, who admits participants."),
}
CONFIRM = {
 "F_TYPE": "Treated as generative AI, which shows every provision that could apply. The documents name no contact for this question; ask your agency.",
 "F_TASK": "Treated as if any of the listed tasks could apply. To confirm, ask your agency: SS-25-001 (3.0, p.6) says “Agencies should conduct their own risk assessments and consult with the Georgia Technology Authority (GTA) Office of Artificial Intelligence for novel, high-risk, or ambiguous use cases not represented here.”",
 "F_PRODUCT": "Treated as if AI content appears in a more official document. To confirm, see GS-25-001, How to Properly Cite AI-Generated Content, p.9; the documents name no contact for citation questions, so ask your agency.",
 "F_ROLE": "Treated as if you are both buying and building. To confirm, ask your agency: PS-23-001 (Policy, p.3) says “Agencies shall submit all software, applications, tools, and services utilizing AI for business operations to GTA for review prior to procurement.”",
 "F_DATA": "Treated as if you will enter such information. To confirm: GS-25-001 (p.2) says employees “should first consult with their department's data privacy officer or designated compliance authority to clarify.”",
 "F_DECISION": "Treated as if the output feeds a decision about a person. To confirm, ask your agency: SS-25-001 (3.0, p.6) says agencies should “consult with the Georgia Technology Authority (GTA) Office of Artificial Intelligence for novel, high-risk, or ambiguous use cases”.",
 "F_HOST": "Treated as if you are the host. The documents name no contact for this; ask your agency.",
}
TASK_VALUES = [v['value'] for v in FACT['F_TASK']['values']]
ASK_IF = {"F_TASK": {"F_TYPE": GENLIKE}, "F_PRODUCT": {"F_TYPE": GENLIKE},
          "F_ROLE": {"F_TYPE": ALLTYPES}, "F_DATA": {"F_TYPE": ALLTYPES},
          "F_HOST": {"F_TASK": ["meetings", "not_sure"], "F_TYPE": GENLIKE},
          "F_DECISION": {"F_TASK": [v for v in TASK_VALUES if v not in ("policy_drafting", "education_training", "not_sure")], "F_TYPE": GENLIKE}}
ASK_WHY = {"F_TASK": "On the 'other AI' branch every element this answer activates holds only generative-AI provisions (ai_type_rule), so it cannot change the result.",
           "F_PRODUCT": "On the 'other AI' branch every element this answer activates holds only generative-AI provisions (ai_type_rule), so it cannot change the result.",
           "F_ROLE": "Not asked when the tool does not use AI: nothing is shown then.", "F_DATA": "Not asked when the tool does not use AI: nothing is shown then.",
           "F_HOST": "Only the meeting-host element depends on this answer, and it requires the meetings task (or Not sure).",
           "F_DECISION": "Skipped when the task is policy drafting, education and training, or Not sure: those answers already activate the decisions-about-people element and its pointer, which are all this question can affect."}
QID = {f: "Q_" + f[2:] for f in FACT}
questions = []
for k, f in enumerate(order):
    nxt = QID[order[k + 1]] if k + 1 < len(order) else "END"
    opts = []
    for v in FACT[f]['values']:
        o = collections.OrderedDict(label=v['label'], sets_fact={f: v['value']}, next=nxt)
        if v['value'] == 'not_sure':
            o['not_sure'] = True; o['confirm_pointer'] = CONFIRM[f]
        opts.append(o)
    questions.append(collections.OrderedDict(id=QID[f], fact_id=f, text=TEXT[f][0], help_text=TEXT[f][1], ask_if=ASK_IF.get(f, "always"), ask_if_reason=ASK_WHY.get(f), options=opts))

# ---------- outcomes ----------
def notes_for(eids):
    cs = [dict(id=c['id'], plain=c['plain_statement']) for c in m['conflicts'] if set(c['affected_element_ids']) & set(eids)]
    qs = [dict(id=o['id'], plain=o['question']) for o in m['open_questions'] if set(o['affected_element_ids']) & set(eids)]
    return cs, qs
def el_out(e):
    cs, qs = notes_for([e['id']])
    return collections.OrderedDict(id=e['id'], title=e['title'], tier=e['tier'],
        statements=[collections.OrderedDict(modality=s['modality'], modal_as_written=s['modal_as_written'], summary=s['summary'], citations=s['citations'], provision_ids=s['provision_ids']) for s in e['statements']],
        other_ai_statements=[collections.OrderedDict(modality=s['modality'], summary=s['other_ai_summary'], citations=s['other_ai_citations'], provision_ids=s['other_ai_provision_ids']) for s in e['statements'] if s['other_ai_provision_ids']],
        conflicts=cs, open_questions=qs)
def ptr_out(p):
    cs, qs = notes_for(p['element_ids'])
    return collections.OrderedDict(id=p['id'], as_written=p['as_written'], employee_pointer=p['employee_pointer'], citations=p['citations'], provision_ids=p['provision_ids'],
        other_ai_as_written=p['other_ai_as_written'], other_ai_citations=p['other_ai_citations'], other_ai_provision_ids=p['other_ai_provision_ids'], conflicts=cs, open_questions=qs)
CLOSING = "This tool lists which GTA policies, standards and guidelines apply to what you described. It does not say whether a specific use is permitted overall, and it is not legal advice. For decisions the documents leave to the agency, ask your agency."
outcomes = collections.OrderedDict(
    scope_gate=collections.OrderedDict(when=[{"F_TYPE": ["none"]}], outcome=RULE['not_ai_outcome']),
    type_rule=collections.OrderedDict(rule=RULE['rule'], when_other=[{"F_TYPE": ["other"]}]),
    type_notes=[collections.OrderedDict(id="NOTE_OTHER_AI", when=[{"F_TYPE": ["other"]}], note=RULE['other_note'])],
    assembly_rule="If 'scope_gate' matches, the outcome is only its 'outcome' text. Otherwise an outcome is the 'always' block, plus every block in 'blocks' and every pointer in 'conditional_pointers' whose 'when' condition matches the facts set on the path, plus the closing line. A 'when' condition is a list of alternatives; an alternative matches when every fact it names has one of the listed values. A fact that was not asked on the path matches nothing. When 'type_rule.when_other' matches, each element uses 'other_ai_statements' instead of 'statements' and each pointer uses 'other_ai_as_written' instead of 'as_written'; an element with no other_ai_statements, or a pointer whose other_ai_as_written is null, is not shown. Every 'type_notes' entry whose 'when' matches is shown before the results.",
    always=collections.OrderedDict(umbrella_elements=[el_out(e) for e in m['elements'] if e['tier'] == 'umbrella'],
                                   indirect_pointers=[ptr_out(p) for p in m['indirect_pointers'] if p['show_when'] == "always"]),
    blocks=[collections.OrderedDict(id="OUT_" + e['id'], when=e['activated_by'], element=el_out(e)) for e in m['elements'] if e['tier'] == 'conditional'],
    conditional_pointers=[collections.OrderedDict(id="OUT_" + p['id'], when=p['show_when'], pointer=ptr_out(p)) for p in m['indirect_pointers'] if p['show_when'] != "always"],
    closing_line=CLOSING)

# ---------- verification ----------
Q = {q['id']: q for q in questions}
def walk():
    paths = []
    def go(qid, facts, asked):
        if qid == "END":
            paths.append((dict(facts), list(asked))); return
        q = Q[qid]
        if q['ask_if'] != "always" and not match([q['ask_if']], facts):
            go(q['options'][0]['next'], facts, asked); return
        for o in q['options']:
            f2 = dict(facts); f2.update(o['sets_fact'])
            go(o['next'], f2, asked + [qid])
    go(questions[0]['id'], {}, [])
    return paths
def from_tree(facts):
    if match(outcomes['scope_gate']['when'], facts): return frozenset({"NOT_AI"}), frozenset()
    oth = match(outcomes['type_rule']['when_other'], facts)
    elist = outcomes['always']['umbrella_elements'] + [b['element'] for b in outcomes['blocks'] if match(b['when'], facts)]
    plist = outcomes['always']['indirect_pointers'] + [b['pointer'] for b in outcomes['conditional_pointers'] if match(b['when'], facts)]
    els = {(e['id'], i) for e in elist for s in (e['other_ai_statements'] if oth else e['statements']) for i in s['provision_ids']}
    ps = {(p['id'], i) for p in plist for i in (p['other_ai_provision_ids'] if oth else p['provision_ids'])}
    notes = {n['id'] for n in outcomes['type_notes'] if match(n['when'], facts)}
    return frozenset(els | notes), frozenset(ps)
def from_map(facts):
    if facts.get("F_TYPE") == "none": return frozenset({"NOT_AI"}), frozenset()
    oth = facts.get("F_TYPE") == "other"
    key = 'other_ai_provision_ids' if oth else 'provision_ids'
    elist = [e for e in m['elements'] if e['tier'] == 'umbrella' or (e['tier'] == 'conditional' and match(e['activated_by'], facts))]
    els = {(e['id'], i) for e in elist for s in e['statements'] for i in s[key]}
    ps = {(p['id'], i) for p in m['indirect_pointers'] if match(p['show_when'], facts) for i in p[key]}
    notes = {"NOTE_OTHER_AI"} if oth else set()
    return frozenset(els | notes), frozenset(ps)
def normalize(facts):
    f = dict(facts)
    for q in questions:
        if q['ask_if'] != "always" and not match([q['ask_if']], f): f.pop(q['fact_id'], None)
    return f
paths = walk()
mism, redundant, bad_skips = [], [], []
reached = set(); distinct = set()
for facts, asked in paths:
    a, b = from_tree(facts), from_map(facts)
    if a != b: mism.append(dict(facts=facts, tree_only=sorted((a[0] | a[1]) - (b[0] | b[1])), map_only=sorted((b[0] | b[1]) - (a[0] | a[1]))))
    reached |= {x[0] for x in a[0] if isinstance(x, tuple)}; distinct.add(a)
    for qid in asked:
        fid = Q[qid]['fact_id']
        alts = [v['value'] for v in FACT[fid]['values'] if v['value'] != facts[fid]]
        if not any(from_map(normalize(dict(facts, **{fid: v}))) != b for v in alts):
            redundant.append(dict(facts=facts, question=qid))
    for q in questions:
        if q['id'] not in asked:
            for v in FACT[q['fact_id']]['values']:
                if from_map(dict(facts, **{q['fact_id']: v['value']})) != b:
                    bad_skips.append(dict(facts=facts, skipped=q['id'], value=v['value']))
cond_ids = [e['id'] for e in m['elements'] if e['tier'] == 'conditional']
unreachable = [e for e in cond_ids if e not in reached]
lens = collections.Counter(len(a) for _, a in paths)
longest = max(lens)
tree_facts = {q['fact_id'] for q in questions}
report = collections.OrderedDict(
    method="Every path was enumerated by following 'next' from the first question and honoring 'ask_if'. For each path the outcome was assembled from this file's 'outcomes' and separately recomputed from stage2_map.json ('activated_by' for elements, 'show_when' for pointers); the two were compared. Each asked question was tested by changing only its answer and recomputing; each skipped question was tested by supplying every possible answer and recomputing.",
    number_of_paths=len(paths), longest_path_questions=longest, shortest_path_questions=min(lens), paths_by_length={str(k): v for k, v in sorted(lens.items())},
    max_questions_allowed=MAXQ, within_limit=longest <= MAXQ, distinct_outcomes=len(distinct),
    mismatches=mism, mismatch_count=len(mism),
    conditional_elements=len(cond_ids), unreachable_conditional_elements=unreachable,
    questions_whose_answer_cannot_change_the_result=redundant, skipped_questions_that_could_have_changed_the_result=bad_skips,
    all_questions_built_from_map_facts=tree_facts <= set(FACT), facts_not_used=sorted(set(FACT) - tree_facts),
    every_question_has_not_sure=all(any(o.get('not_sure') for o in q['options']) for q in questions),
    question_order=[q['id'] for q in questions],
    ordering_basis=[dict(fact=f, gate=True, note='Asked first: it decides which provisions are in scope.') if f in GATES else dict(fact=f, average_elements_ruled_out_per_answer=scores[f][0], elements_depending_on_fact=scores[f][1]) for f in order],
    ordering_note="The AI-type question comes first because it decides which provisions are in scope. The rest are ordered by the average number of fact-dependent elements an answer rules out, assuming each answer is equally likely. Only 'It does not use AI' ends the interview early; otherwise order does not change how many questions are asked, only the 'ask_if' skips do.")
out = collections.OrderedDict(
    title="GTA AI policy triage", source_map="stage2_map.json",
    questions=questions, outcomes=outcomes, verification_report=report)
json.dump(out, open(OUTJ, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.load(open(OUTJ, encoding='utf-8'))
print(json.dumps({k: v for k, v in report.items() if k not in ('method', 'mismatches', 'questions_whose_answer_cannot_change_the_result', 'skipped_questions_that_could_have_changed_the_result')}, indent=1))
print("mism", len(mism), "redundant", len(redundant), "bad_skips", len(bad_skips))
if redundant[:3]: print(redundant[:3])
if bad_skips[:3]: print(bad_skips[:3])
