import json, sys
t = json.load(open(sys.argv[1], encoding='utf-8'))
L = []
def when_txt(w):
    if w == "always": return "always"
    return " OR ".join("(" + " AND ".join(f"{f} is one of: {', '.join(v)}" for f, v in alt.items()) + ")" for alt in w)
def notes(x):
    for c in x['conflicts']: L.append(f"- Conflict {c['id']}: {c['plain']}")
    for q in x['open_questions']: L.append(f"- Open question {q['id']}: {q['plain']}")
def element(e, h):
    L.append(f"{h} {e['title']} (`{e['id']}`)"); L.append("")
    for s in e['statements']:
        L.append(f"**Modality: {s['modality']}** (as written: {'; '.join(s['modal_as_written'])})"); L.append("")
        L.append(s['summary']); L.append("")
        L.append("Citations:")
        for c in s['citations']: L.append(f"- {c}")
        L.append("")
    if [x['provision_ids'] for x in e['other_ai_statements']] != [x['provision_ids'] for x in e['statements']]:
        if not e['other_ai_statements']: L.extend(["On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).", ""])
        else:
            L.extend(["On the 'other AI' branch, only:", ""])
            for x in e['other_ai_statements']: L.append(f"- **{x['modality']}**: {x['summary']} ({'; '.join(x['citations'])})")
            L.append("")
    if e['conflicts'] or e['open_questions']:
        L.append("Conflicts and open questions affecting this element:"); notes(e); L.append("")
def pointer(p, h):
    L.append(f"{h} Pointer `{p['id']}`"); L.append("")
    L.append(f"As written: {p['as_written']}"); L.append("")
    L.append(p['employee_pointer']); L.append("")
    if p['other_ai_as_written'] != p['as_written']:
        L.extend([("On the 'other AI' branch: " + p['other_ai_as_written']) if p['other_ai_as_written'] else "On the 'other AI' branch: not shown.", ""])
    L.append("Citations:")
    for c in p['citations']: L.append(f"- {c}")
    L.append("")
    if p['conflicts'] or p['open_questions']:
        L.append("Conflicts and open questions affecting this pointer:"); notes(p); L.append("")
L += [f"# {t['title']}", "", f"Generated from stage3_triage.json. Source map: {t['source_map']}.", "", "# Questions", ""]
for q in t['questions']:
    L += [f"## {q['id']}: {q['text']}", "", q['help_text'], "", f"Fact: `{q['fact_id']}`", ""]
    if q['ask_if'] == "always": L.append("Asked: always")
    else:
        L.append("Asked only when: " + when_txt([q['ask_if']])); L.append(""); L.append(q['ask_if_reason'])
    L += ["", "| Option | Sets | Next |", "|---|---|---|"]
    for o in q['options']:
        s = ", ".join(f"{k} = {v}" for k, v in o['sets_fact'].items())
        L.append(f"| {o['label']} | {s} | {o['next']} |")
    L.append("")
    for o in q['options']:
        if o.get('not_sure'): L += [f"If “{o['label']}”: {o['confirm_pointer']}", ""]
o = t['outcomes']
L += ["# Outcomes", "", o['assembly_rule'], "", "## Scope gate", "", f"Shown when: {when_txt(o['scope_gate']['when'])}", "", o['scope_gate']['outcome']['text'], "", o['scope_gate']['outcome']['unresolved_note'], ""]
L += ["Citations:"] + [f"- {c}" for c in o['scope_gate']['outcome']['citations']] + [""]
L += ["## AI-type rule", "", o['type_rule']['rule'], ""]
for n in o['type_notes']:
    L += [f"## Note {n['id']}", "", f"Shown when: {when_txt(n['when'])}", "", n['note']['text'], "", "Citations:"] + [f"- {c}" for c in n['note']['citations']] + [""]
L += ["## Outcome block: always shown (unless the scope gate matches)", ""]
for e in o['always']['umbrella_elements']: element(e, "###")
for p in o['always']['indirect_pointers']: pointer(p, "###")
for b in o['blocks']:
    L += [f"## Outcome block: {b['id']}", "", f"Shown when: {when_txt(b['when'])}", ""]
    element(b['element'], "###")
for b in o['conditional_pointers']:
    L += [f"## Outcome block: {b['id']}", "", f"Shown when: {when_txt(b['when'])}", ""]
    pointer(b['pointer'], "###")
L += ["## Closing line (every outcome)", "", o['closing_line'], ""]
v = t['verification_report']
L += ["# Verification report", "", v['method'], "",
      f"- Number of paths: {v['number_of_paths']}", f"- Longest path: {v['longest_path_questions']} questions (limit {v['max_questions_allowed']}; within limit: {v['within_limit']})",
      f"- Shortest path: {v['shortest_path_questions']} questions", f"- Paths by length: {v['paths_by_length']}", f"- Distinct outcomes: {v['distinct_outcomes']}",
      f"- Mismatches: {v['mismatch_count']}", f"- Conditional elements: {v['conditional_elements']}; unreachable: {v['unreachable_conditional_elements']}",
      f"- Asked questions whose answer cannot change the result: {len(v['questions_whose_answer_cannot_change_the_result'])}",
      f"- Skipped questions that could have changed the result: {len(v['skipped_questions_that_could_have_changed_the_result'])}",
      f"- Every question has a Not sure option: {v['every_question_has_not_sure']}", f"- Question order: {', '.join(v['question_order'])}", "", v['ordering_note'], ""]
for b in v['ordering_basis']:
    if b.get('gate'): L.append(f"- {b['fact']}: {b['note']}"); continue
    L.append(f"- {b['fact']}: rules out {b['average_elements_ruled_out_per_answer']} elements per answer on average; {b['elements_depending_on_fact']} elements depend on it")
open(sys.argv[2], 'w', encoding='utf-8').write("\n".join(L) + "\n")
print(len(L), "lines")
