"""Builds the diagrams (images 10-16) for the proposed Georgia build as 1600x900 HTML pages. Every content
count is read from the data files in this repository. From the repository root:
  python3 docs/diagrams/build.py /tmp/diagrams
  python3 docs/diagrams/render.py /tmp/diagrams docs/images      # Playwright; set CHROME_PATH
Screenshots of the page (images 00-09): serve site/ on :8765, then python3 docs/diagrams/screenshots.py docs/images
The Georgia build is a proposal: see docs/backend_plan.md. Nothing here describes a system GTA runs."""
import json, os, re, sys, collections as C, html

OUT = sys.argv[1]
inv = json.load(open('data/stage1_inventory.json', encoding='utf-8'))
mp = json.load(open('data/stage2_map.json', encoding='utf-8'))
tri = json.load(open('data/stage3_triage.json', encoding='utf-8'))
dr = json.load(open('data/decision_rights.json', encoding='utf-8'))
site = json.load(open('site/data.json', encoding='utf-8'))
E = html.escape
TEAL, INK, MUTED, AMBER, AMBER_BG, GREEN, GREEN_BG = "#0d5a61", "#14232b", "#55666f", "#8a4f00", "#fdf0d5", "#1f6b3a", "#dff0e3"

CSS = """
*{box-sizing:border-box}html,body{margin:0}
body{display:flex;flex-direction:column;width:1600px;height:900px;overflow:hidden;background:#eef2f1;color:#14232b;font:16px/1.4 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;padding:44px 56px;position:relative}
h1{font:500 40px/1.1 Georgia,"Times New Roman",serif;margin:0}
.sub{color:#55666f;font-size:18px;margin:8px 0 0;max-width:110ch}
.top{display:flex;justify-content:space-between;align-items:flex-start;gap:24px;margin-bottom:24px}
.top+*{margin-top:auto!important}body>:nth-last-child(2){margin-bottom:auto!important}
.tag{font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#0d5a61;margin-bottom:6px}
.prop{flex-shrink:0;font-size:13px;font-weight:800;letter-spacing:.04em;color:#8a4f00;border:1.5px solid #b86e00;background:#fdf0d5;border-radius:999px;padding:4px 12px}
.card{background:#fff;border:1px solid #cfd9d8;border-radius:12px;box-shadow:0 1px 2px rgba(20,35,43,.06),0 8px 20px -12px rgba(20,35,43,.18)}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.muted{color:#55666f}
.chip{display:inline-block;background:#d9ecec;color:#0d5a61;font-weight:600;border-radius:6px;padding:4px 10px;font-size:15px;margin:0 6px 6px 0}
.chip.az{background:#e8f0f8;color:#1d4f7a}
.chip.opt{background:#fff;border:1px dashed #9fb0b6;color:#55666f;font-weight:500}
.ok{display:inline-flex;align-items:center;gap:6px;color:#1f6b3a;font-weight:600}
.ok::before{content:"";width:16px;height:16px;border-radius:50%;background:#dff0e3 url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M4 8.5l2.5 2.5L12 5.5' fill='none' stroke='%231f6b3a' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/16px no-repeat;flex-shrink:0}
.foot{position:absolute;left:56px;right:56px;bottom:24px;color:#55666f;font-size:13px;display:flex;justify-content:space-between}
.arrow{flex:0 0 auto;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#55666f;font-size:13px;font-weight:600;gap:4px;text-align:center}
.arrow svg{display:block}
.lane{font-size:13px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#55666f;writing-mode:vertical-rl;transform:rotate(180deg);text-align:center}
"""
ARR = '<svg width="40" height="16" viewBox="0 0 44 16"><path d="M2 8h36M32 2l8 6-8 6" fill="none" stroke="#77878d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
DOWN = '<svg width="16" height="22" viewBox="0 0 16 26"><path d="M8 2v18M2 15l6 7 6-7" fill="none" stroke="#77878d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
FOOT = '<div class="foot"><span>GTA AI Policy Check · proposed build for the State of Georgia · a proposal, not an official GTA plan</span><span>{}</span></div>'


def page(name, tag, title, sub, body, source):
    head = f'<div class="top"><div><div class="tag">{E(tag)}</div><h1>{E(title)}</h1><p class="sub">{E(sub)}</p></div><span class="prop">PROPOSED · GEORGIA BUILD</span></div>'
    with open(os.path.join(OUT, name + '.html'), 'w', encoding='utf-8') as f:
        f.write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{name}</title><style>{CSS}</style></head><body>{head}{body}{FOOT.format(E(source))}</body></html>')


def bars(rows, label_w, bar_w=150):
    """Single-series horizontal bars: one hue, thin, 4px rounded data end, value at the bar end."""
    mx = max(v for _, v in rows)
    return ''.join(
        f'<div style="display:grid;grid-template-columns:{label_w}px {bar_w + 50}px;align-items:center;gap:12px;margin:0 0 9px">'
        f'<span style="font-size:15px;text-align:right">{E(n)}</span>'
        f'<span style="display:flex;align-items:center;gap:8px"><span style="display:block;height:13px;width:{max(2, round(v / mx * bar_w))}px;background:{TEAL};border-radius:0 4px 4px 0"></span>'
        f'<span style="font-size:15px;font-weight:700;font-variant-numeric:tabular-nums">{v}</span></span></div>' for n, v in rows)


ICONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons')
BRAND = {'python': '3776AB', 'html5': 'E34F26', 'css': '663399', 'javascript': 'F7DF1E'}


def logo(slug, size=64):
    """A Simple Icons logo (CC0 artwork; trademarks of their owners) in its brand colour."""
    svg = open(os.path.join(ICONS, slug + '.svg'), encoding='utf-8').read()
    title = re.search(r'<title>(.*?)</title>', svg).group(1)
    path = re.search(r'<path d="([^"]+)"', svg).group(1)
    return f'<svg role="img" aria-label="{E(title)}" viewBox="0 0 24 24" width="{size}" height="{size}"><path d="{path}" fill="#{BRAND[slug]}"/></svg>'


def glyph(kind, size=64, color=TEAL):
    """Generic line pictures for things without a usable logo."""
    d = {'doc': '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6M9 9h2"/>',
         'check': '<path d="M12 3l7 3v5c0 4.5-3 8.5-7 10-4-1.5-7-5.5-7-10V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
         'cloud': '<path d="M7 18a4.5 4.5 0 0 1-.5-9 6 6 0 0 1 11.4 1.6A3.8 3.8 0 0 1 17.5 18z"/>',
         'chart': '<path d="M4 20h16M7 16v-5M12 16V6M17 16v-8"/>',
         'lock': '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
         'people': '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c.6-3.4 3-5.5 6-5.5s5.4 2.1 6 5.5"/><circle cx="17" cy="9" r="2.6"/><path d="M15.5 14.6c2.6.2 4.6 2.1 5.1 5"/>'}[kind]
    return f'<svg aria-hidden="true" viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{d}</svg>'


def box(title, items, sub="", dark=False, w=None, accent=None, fs=16):
    style = "flex:1 1 0;min-width:0;padding:16px 16px" + (f";flex:0 0 {w}px" if w else "")
    if dark: style += f";background:{TEAL};color:#fff;border-color:{TEAL}"
    if accent: style += f";border-top:4px solid {accent}"
    li = ''.join(f'<li style="margin:0 0 5px">{x}</li>' for x in items)
    s = f"<div style='font-size:13px;margin-top:2px;opacity:.8'>{sub}</div>" if sub else ""
    return f'<div class="card" style="{style}"><div style="font-weight:800;font-size:19px;line-height:1.2">{title}</div>{s}<ul style="margin:10px 0 0;padding-left:18px;font-size:{fs}px;line-height:1.35">{li}</ul></div>'


def arrow(label="", w=78):
    return f'<div class="arrow" style="width:{w}px">{E(label)}{ARR}</div>'


def note(text, color=GREEN, bg=GREEN_BG, fs=16):
    return f'<div style="background:{bg};color:{color};border-radius:8px;padding:12px 16px;font-size:{fs}px;font-weight:600">{text}</div>'


P = inv['provisions']
docs = inv['documents']
n_prov = len(P)
tiers_el = C.Counter(e['tier'] for e in mp['elements'])
kinds = C.Counter(r['k'] for r in site)
vr = tri['verification_report']
N_SUITES = len([f for f in os.listdir('tests') if f.startswith('test_') and f.endswith('.py')])

# ---------------------------------------------------------------- 10 content pipeline
steps = [
    ("1", "GTA publishes or updates a document", "GTA policy owner", "The PDF is added to the content library and its text extracted",
     "Every quote must match this text"),
    ("2", "Analysts record each provision", "stage1_inventory.json", f"{n_prov} provisions with exact wording, citation and modal verb as written · {len(inv['conflicts'])} conflicts and {len(mp['open_questions'])} open questions recorded, not guessed",
     f"{n_prov}/{n_prov} quotes match the PDFs today"),
    ("3", "Rules mapped to situations", "stage2_map.json", f"{len(mp['elements'])} topics: {tiers_el['umbrella']} for every use, {tiers_el['conditional']} by situation, {tiers_el['out_of_scope_for_employee']} for agencies · {len(mp['facts'])} facts",
     "Every provision in exactly one topic"),
    ("4", "Questions, next steps and who decides", "stage3_triage.json · site/data.json", f"{len(tri['questions'])} questions · {vr['distinct_outcomes']:,} possible results · {dr['counts']['decisions']} decision points · {len(site)} page records",
     f"All {vr['number_of_paths']:,} answer paths proven: {vr['mismatch_count']} mismatches"),
    ("5", "Automated pipeline", "State build service", f"Rebuilds everything, runs {N_SUITES} browser test suites and an accessibility audit (WCAG 2.1 AA)",
     "Release blocked if any check fails"),
    ("6", "Approved and released", "GTA policy owner → Azure", "Approved change goes live; each citation shows its document’s effective date",
     "Staff always see a dated, sourced version"),
]
rows = []
for i, (n, what, who, holds, check) in enumerate(steps):
    rows.append(f'''<div class="card" style="display:grid;grid-template-columns:44px 330px 260px 1fr 330px;align-items:center;gap:18px;padding:11px 20px">
      <span style="width:32px;height:32px;border-radius:50%;background:{TEAL};color:#fff;font-weight:800;display:grid;place-items:center">{n}</span>
      <span style="font-weight:700;font-size:17px">{E(what)}</span>
      <span class="mono" style="font-size:14px;color:{TEAL};font-weight:700">{E(who)}</span>
      <span style="font-size:15px">{E(holds)}</span>
      <span class="ok" style="font-size:14px">{E(check)}</span></div>''')
    if i < len(steps) - 1:
        rows.append(f'<div style="display:flex;padding-left:28px;height:18px;align-items:center">{DOWN}</div>')
body = f'''<div><div style="display:grid;grid-template-columns:44px 330px 260px 1fr 330px;gap:18px;padding:0 21px 8px;font-size:13px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:{MUTED}"><span></span><span>Step</span><span>Who or what</span><span>What it produces</span><span>Built-in check</span></div>
{''.join(rows)}</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:14px">
{note("Policy staff review each change in the page’s review mode before approving")}
{note("Usage data then shows whether people find what they need (see the usage diagram)")}</div>'''
page('10-data-pipeline', 'Content pipeline', 'From a GTA document to every state employee, checked at every step',
     'How policy content would be kept current in the Georgia build. Steps 2–4 run today; steps 5–6 are the proposed production process.',
     body, 'Counts read from the data files in this repository')

# ---------------------------------------------------------------- 11 the data Georgia maintains and collects
tiles = [(f"{n_prov}", "provisions, quoted exactly"), (f"{len(docs)}", "GTA documents"), (f"{len(mp['elements'])}", "topics"),
         (f"{vr['number_of_paths']:,}", "answer paths proven"), (f"{len(inv['conflicts'])}", "conflicts recorded"), (f"{dr['counts']['decisions']}", "decision points")]
tile_html = ''.join(f'<div class="card" style="padding:12px 16px"><div style="font:500 36px/1.05 Georgia,serif;font-variant-numeric:tabular-nums">{a}</div><div class="muted" style="font-size:14px;margin-top:4px">{E(b)}</div></div>' for a, b in tiles)
by_doc = sorted(((f"{d['doc_id']} · {d['document_type'].replace('other', 'web page')}", d['provision_count']) for d in docs), key=lambda x: -x[1])
mod = C.Counter(p['modality'] for p in P)
by_mod = [(n, mod[k]) for k, n in [("must", "Must"), ("must_not", "Must not"), ("should", "Should"), ("should_not", "Should not"), ("may", "May"), ("informational", "Note")]]
USAGE = [("Use by agency, week by week", "Adoption and where to focus outreach"), ("What people use AI for", "Task and AI-type mix over time"),
         ("Where approvals will land", "Stop and Check first rates by agency"), ("Which questions confuse people", "“Not sure” rate per question"),
         ("Which rules people read closely", "Most-opened exact wording"), ("Where people give up", "Drop-off by question")]
usage_html = ''.join(f'<div style="margin:0 0 10px"><div style="font-weight:700;font-size:15px">{E(a)}</div><div class="muted" style="font-size:14px">{E(b)}</div></div>' for a, b in USAGE)
body = f'''<div><div style="display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin-bottom:16px">{tile_html}</div>
<div style="display:grid;grid-template-columns:1.15fr 0.85fr 1fr;gap:16px">
<div class="card" style="padding:16px 18px"><div style="font-weight:700;font-size:17px">Policy content by document</div><div class="muted" style="font-size:13px;margin:2px 0 12px">Quoted provisions · 5GP = 5 Guiding Principles web page</div>{bars(by_doc, 170)}</div>
<div class="card" style="padding:16px 18px"><div style="font-weight:700;font-size:17px">By obligation</div><div class="muted" style="font-size:13px;margin:2px 0 12px">The modal verb as written is kept too</div>{bars(by_mod, 90, 130)}</div>
<div class="card" style="padding:16px 18px;background:{AMBER_BG};border-color:#e0c48f"><div style="font-weight:700;font-size:17px">Usage data it would collect</div><div style="font-size:13px;margin:2px 0 12px;color:{AMBER};font-weight:600">Proposed · counts, never names or free text</div>{usage_html}</div>
</div></div>'''
page('11-data-at-a-glance', 'The data', 'The data Georgia would maintain, and what it would learn',
     f'GTA’s AI documents as {n_prov} quoted provisions, maintained by GTA, plus anonymous usage data that shows how agencies use the tool.',
     body, 'Source: data/stage1_inventory.json, stage2_map.json, stage3_triage.json, decision_rights.json · usage: docs/backend_plan.md')

# ---------------------------------------------------------------- 12 record anatomy
ex = next(p for p in P if p['id'] == 'SS-25-001-1.3-2')
NOTE = {'id': 'Stable ID', 'section': 'Citation', 'text_excerpt': 'Exact wording, checked against the PDF', 'modality': 'Grouping on the page', 'modal_as_written': 'Verb as written'}


def jsonlines(pairs, notes, maxlen=60):
    out = []
    for k, v in pairs:
        val = json.dumps(v, ensure_ascii=False)
        if len(val) > maxlen: val = val[:maxlen - 2] + '…"'
        nt = f'<span style="color:#b86e00;font-family:system-ui;font-size:13px;font-weight:600;white-space:nowrap">← {E(notes[k])}</span>' if k in notes else ''
        out.append(f'<div style="display:flex;justify-content:space-between;gap:10px;align-items:baseline"><span><span style="color:{TEAL}">"{k}"</span>: {E(val)},</span>{nt}</div>')
    return '<div class="mono" style="font-size:13.5px;line-height:1.7;background:#f6f8f8;border-radius:8px;padding:12px 14px">{<div style="padding-left:16px">' + ''.join(out) + '</div>}</div>'


prov_json = jsonlines([(k, ex[k]) for k in ['id', 'doc_id', 'section', 'page', 'text_excerpt', 'modality', 'modal_as_written']], NOTE)
event = [("type", "results_view"), ("session_id", "random, one visit"), ("agency_code", "from approved list"), ("content_version", "2026-11-25"),
         ("posts", 3), ("signs", ["SS-25-001-1.3-2"]), ("topics", ["C_DATA", "C_TASK_PUBLIC"])]
event_json = jsonlines(event, {"session_id": "Not linked to a person", "agency_code": "A pick list, not free text", "signs": "Provision IDs, from fixed lists"})
KIND = [("el", "Topics"), ("dec", "Decisions"), ("step", "Next steps"), ("ptr", "Agency pointers"), ("q", "Questions"), ("factor", "Guardrail factors"), ("sign", "Stop / Check first signs")]
krows = ''.join(f'<span class="mono chip" style="margin:0 0 6px;text-align:center">{k}</span><span style="font-weight:700;text-align:right">{kinds[k]}</span><span style="font-size:14px">{E(d)}</span>' for k, d in KIND)
body = f'''<div style="display:grid;grid-template-columns:1.25fr 1fr;gap:20px">
<div class="card" style="padding:18px 20px"><div style="font-weight:700">Policy content: one provision <span class="muted" style="font-weight:400;font-size:14px">(1 of {n_prov})</span></div>
<div class="muted" style="font-size:13px;margin:2px 0 10px">Maintained by GTA · published with the page</div>{prov_json}
<div style="margin-top:12px;font-size:14px">The page loads <span class="mono">site/data.json</span>: {len(site)} records built from these.</div>
<div style="display:grid;grid-template-columns:76px 30px 1fr 76px 30px 1fr;gap:4px 10px;align-items:center;margin-top:10px">{krows}</div></div>
<div class="card" style="padding:18px 20px;background:#fffdf7;border-color:#e0c48f"><div style="font-weight:700">Usage data: one event <span style="font-size:12px;font-weight:800;color:{AMBER};border:1.5px solid #b86e00;border-radius:999px;padding:1px 8px;margin-left:6px">PROPOSED</span></div>
<div class="muted" style="font-size:13px;margin:2px 0 10px">Sent when results appear · stored in Azure SQL</div>{event_json}
<div style="margin-top:14px;display:grid;gap:8px">{note("Only values from fixed lists are accepted", fs=15)}{note("Never stored: names, free text, IP addresses", fs=15)}{note("Emails, if given by choice, kept in a separate table", fs=15)}</div></div></div>'''
page('12-data-records', 'Data format', 'What the data looks like',
     'Every line on the page traces to a quoted provision. Usage events would record only values from fixed lists.',
     body, 'Example provision: SS-25-001 section 1.3, page 3 · event schema: docs/backend_plan.md §4')

# ---------------------------------------------------------------- 13 tech stack (detailed)
LAYERS = [
    ("Content & governance", [("GTA policy documents (PDF)", ""), ("GTA policy owner approves changes", "az"), ("Review mode for policy staff", "")], "Who owns and approves the rules"),
    ("Build & checks", [("Python 3.11+, standard library", ""), ("Source verifier", ""), ("Playwright browser tests", ""), ("Accessibility audit", "")], "Every release proves quotes, answer paths and WCAG 2.1 AA"),
    ("Delivery", [("Automated build pipeline", ""), ("Bicep (infrastructure as code)", "az"), ("dev · test · prod", "az")], "Build service is the State’s choice"),
    ("Web page", [("HTML", ""), ("JavaScript (no framework)", ""), ("CSS: light, dark, print", ""), ("System fonts", "")], "Works on any phone or computer; no app"),
    ("Hosting", [("Azure Static Web Apps", "az"), ("Azure Front Door + WAF", "az"), ("State web address (to decide)", "opt"), ("State sign-in: Microsoft Entra ID (option)", "opt")], "Page and API on one secure address"),
    ("API & data", [("Azure Functions (Python)", "az"), ("Azure SQL (serverless)", "az")], "Accepts only known values; stores no personal data in usage"),
    ("Insights", [("Power BI", "az"), ("Row-level security by agency", "az")], "Trends for GTA; each agency sees its own"),
    ("Security & operations", [("Key Vault", "az"), ("Managed identity", "az"), ("Application Insights", "az"), ("Defender for SQL", "az")], "No passwords in code; alerts on misuse"),
]
lrows = ''.join(f'''<div class="card" style="display:grid;grid-template-columns:230px 1fr 330px;gap:18px;align-items:center;padding:10px 18px">
<span style="font-weight:700;font-size:17px">{E(n)}</span><span>{''.join(f'<span class="chip {c}">{E(t)}</span>' for t, c in chips)}</span><span class="muted" style="font-size:14px">{E(why)}</span></div>''' for n, chips, why in LAYERS)
legend = f'<div style="display:flex;gap:18px;margin-top:12px;font-size:14px" class="muted"><span><span class="chip" style="margin:0 6px 0 0">Today</span>runs in the proof of concept</span><span><span class="chip az" style="margin:0 6px 0 0">Proposed</span>new for the Georgia build</span><span><span class="chip opt" style="margin:0 6px 0 0">Option</span>a State decision</span></div>'
page('13-tech-stack', 'Tech stack', 'The Georgia build, layer by layer',
     'A small, static, tested core that already exists, hosted and measured on the State’s Microsoft Azure environment.',
     f'<div><div style="display:flex;flex-direction:column;gap:9px">{lrows}</div>{legend}</div>', 'Detail: docs/backend_plan.md · runtime dependencies of the page: none')

# ---------------------------------------------------------------- 14 Georgia build, end to end
lane = lambda label, inner: f'<div style="display:grid;grid-template-columns:34px 1fr;gap:10px;align-items:stretch"><div class="lane">{E(label)}</div><div style="display:flex;align-items:stretch">{inner}</div></div>'
content = (box("GTA documents", ["Policies, standards, guidelines"], "Source", w=210, fs=15) + arrow("update") +
           box("Policy analysts", ["Record provisions with exact quotes"], "Content team", fs=15) + arrow("submit") +
           box("Automated pipeline", ["Quote check, every answer path, accessibility"], "State build service", fs=15) + arrow("passes") +
           box("GTA approval", ["Policy owner signs off", "Release goes to Static Web Apps ↓"], "Governance", fs=15, w=230))
service = (box("State employees", ["Phone or computer", "Optional State sign-in"], "Browser", dark=True, w=210, fs=15) + arrow("HTTPS") +
           box("Front Door + WAF", ["State web address", "Rate limits, protection"], "Azure", accent=TEAL, fs=15) + arrow("") +
           box("Static Web Apps", ["The page and its data", "API on the same address"], "Azure", accent=TEAL, fs=15) + arrow("events") +
           box("Functions", ["Validate against fixed lists", "Drop anything unknown"], "Azure", accent=TEAL, fs=15, w=230))
insight = (box("Azure SQL", ["Receives events from Functions", "Usage anonymous; contacts separate"], "Azure", accent=TEAL, w=210, fs=15) + arrow("views") +
           box("Power BI", ["Weekly trends by agency", "Counts under 5 hidden"], "Azure", accent=TEAL, fs=15) + arrow("informs") +
           box("GTA Office of AI", ["Guidance, outreach, policy updates"], "Decisions", fs=15) + arrow("") +
           box("Agency contacts", ["See their own agency only"], "Row-level security", fs=15, w=230))
body = f'''<div style="display:flex;flex-direction:column;gap:14px">
{lane("Content", content)}{lane("Service", service)}{lane("Insights", insight)}</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:16px">
{note("Key Vault + managed identity: no passwords in code", fs=15)}{note("Application Insights: health only, IP masking on", fs=15)}
{note("Bicep: dev, test and prod built the same way", fs=15)}{note("To decide: sign-in, web address, retention", AMBER, AMBER_BG, fs=15)}</div>'''
page('14-architecture-georgia', 'Architecture', 'The Georgia build, end to end',
     'Three loops: GTA keeps the rules current, employees get answers, and anonymous usage data shows GTA where guidance is needed.',
     body, 'Today the proof of concept runs as a static page; this is the proposed production design')

# ---------------------------------------------------------------- 15 usage data detail
flow = (box("Browser", ["Same static page", "Sends fixed-list events in batches", "Opt-out and Global Privacy Control respected"], "Employee", dark=True, w=250)
        + arrow("POST /api/events", 96) +
        box("Azure Static Web Apps", ["Hosts the page and the API on one address", "HTTPS; CORS locked to the site"], "Standard plan", accent=TEAL)
        + arrow("", 60) +
        box("Azure Functions", ["Checks every value against lists generated from data.json", "Never logs request bodies"], "Python, HTTP trigger", accent=TEAL)
        + arrow("managed identity", 96) +
        box("Azure SQL", ["<b>usage</b>: sessions, events, answers", "<b>contacts</b>: opt-in emails, encrypted, separate role", "13 months raw, then roll-up"], "Serverless, auto-pause", accent=TEAL)
        + arrow("views", 60) +
        box("Power BI", ["Weekly trends by agency", "Counts under 5 hidden", "Row-level security by agency"], "Dashboards", accent=TEAL, w=230))
support = ''.join(f'<div class="card" style="padding:12px 16px"><div style="font-weight:700">{a}</div><div class="muted" style="font-size:14px">{b}</div></div>' for a, b in [
    ("Key Vault", "Secrets; no passwords in code"), ("Application Insights", "Health only; IP masking on; 30-day logs"),
    ("Front Door WAF", "Rate limits and protection"), ("Automated pipeline + Bicep", "Same build in dev, test, prod")])
body = f'''<div><div style="display:flex;align-items:stretch">{flow}</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:18px">{support}</div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-top:16px">
{note("No free text, IP addresses or cross-visit IDs stored")}{note("Session ID lasts one visit")}{note("Needs sign-off: notice, agency list, retention", AMBER, AMBER_BG)}</div></div>'''
page('15-architecture-azure', 'Usage data', 'How usage data flows, in detail',
     'Collects what people ask and what the tool answers, never who they are. Emails, given only by choice, are stored apart and never joined to usage.',
     body, 'Plan: docs/backend_plan.md')


# ---------------------------------------------------------------- 16 simplified (non-expert audience)
def stepcard(n, title, art, names, text):
    return (f'<div class="card" style="flex:1 1 0;min-width:0;padding:24px 20px 22px;text-align:center;display:flex;flex-direction:column;align-items:center">'
            f'<div style="width:34px;height:34px;border-radius:50%;background:{TEAL};color:#fff;font-weight:800;display:grid;place-items:center;font-size:17px">{n}</div>'
            f'<div style="font:500 26px/1.15 Georgia,serif;margin:12px 0 16px">{E(title)}</div>'
            f'<div style="display:flex;gap:10px;align-items:center;justify-content:center;height:68px">{art}</div>'
            f'<div style="font-size:14px;font-weight:700;color:{MUTED};margin:12px 0 10px;letter-spacing:.02em">{E(names)}</div>'
            f'<div style="font-size:17px;line-height:1.4">{E(text)}</div></div>')


ar = '<div class="arrow" style="width:40px">' + ARR.replace('width="40"', 'width="30"') + '</div>'
cards = ar.join([
    stepcard(1, "The rules", glyph('doc', 62), "GTA’s AI documents", "Georgia’s official AI policies, standards and guidelines, kept current by GTA."),
    stepcard(2, "Turned into data", logo('python', 62), "Python", f"A small program breaks the rules into {n_prov} exact quotes, each with its source."),
    stepcard(3, "Checked first", glyph('check', 62, GREEN), "Automated checks + GTA approval", "Every update is tested: the quotes, every answer, accessibility. Then GTA signs off."),
    stepcard(4, "Used by staff", logo('html5', 46) + logo('css', 46) + logo('javascript', 46) + glyph('cloud', 50), "Web page · Microsoft Azure", "A simple page in the State’s Azure cloud. Any phone or computer, no app."),
    stepcard(5, "Insights for GTA", glyph('chart', 62), "Power BI", "Dashboards show what agencies ask about and where approvals will land."),
])
body = f'''<div><div style="display:flex;align-items:stretch">{cards}</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px">
<div class="card" style="padding:16px 22px;display:flex;align-items:center;gap:16px;background:{GREEN_BG};border-color:#b9dcc3">{glyph('lock', 40, GREEN)}<span style="font-size:17px;color:#14432a"><b>Private by design:</b> it counts how the tool is used, never who uses it.</span></div>
<div class="card" style="padding:16px 22px;display:flex;align-items:center;gap:16px;background:{AMBER_BG};border-color:#e0c48f">{glyph('people', 40, AMBER)}<span style="font-size:17px;color:#5c3700"><b>To confirm with GTA:</b> sign-in, web address and how long data is kept.</span></div>
</div></div>'''
page('16-tech-stack-simple', 'How it would be built for Georgia', 'Simple, secure, and checked at every step',
     'From GTA’s documents to a web page every state employee can use, hosted in the State’s Microsoft Azure environment.',
     body, 'Logos: Simple Icons (CC0); trademarks of their owners. Azure and Power BI shown without logos.')
print('built 10-16')
