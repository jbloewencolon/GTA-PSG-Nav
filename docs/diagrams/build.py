"""Builds the data, stack and architecture diagrams (images 10-15) as 1600x900 HTML pages, with every count
read from the data files. From the repository root:
  python3 docs/diagrams/build.py /tmp/diagrams
  python3 docs/diagrams/render.py /tmp/diagrams docs/images      # Playwright; set CHROME_PATH
Screenshots of the page (images 00-09): serve site/ on :8765, then python3 docs/diagrams/screenshots.py docs/images"""
import json, os, sys, collections as C, html

OUT = sys.argv[1]
inv = json.load(open('data/stage1_inventory.json', encoding='utf-8'))
mp = json.load(open('data/stage2_map.json', encoding='utf-8'))
tri = json.load(open('data/stage3_triage.json', encoding='utf-8'))
dr = json.load(open('data/decision_rights.json', encoding='utf-8'))
site = json.load(open('site/data.json', encoding='utf-8'))
E = html.escape

CSS = """
*{box-sizing:border-box}html,body{margin:0}
body{display:flex;flex-direction:column;width:1600px;height:900px;overflow:hidden;background:#eef2f1;color:#14232b;font:16px/1.4 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;padding:44px 56px}
h1{font:500 40px/1.1 Georgia,"Times New Roman",serif;margin:0}
.sub{color:#55666f;font-size:18px;margin:8px 0 0;max-width:110ch}
.top{display:flex;justify-content:space-between;align-items:flex-start;gap:24px;margin-bottom:28px}
.tag{font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#0d5a61;margin-bottom:6px}
.card{background:#fff;border:1px solid #cfd9d8;border-radius:12px;box-shadow:0 1px 2px rgba(20,35,43,.06),0 8px 20px -12px rgba(20,35,43,.18)}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.muted{color:#55666f}
.chip{display:inline-block;background:#e3e9e8;border-radius:6px;padding:4px 10px;font-size:15px;margin:0 6px 6px 0}
.chip.k{background:#d9ecec;color:#0d5a61;font-weight:600}
.ok{display:inline-flex;align-items:center;gap:6px;color:#1f6b3a;font-weight:600}
.ok::before{content:"";width:16px;height:16px;border-radius:50%;background:#dff0e3 url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M4 8.5l2.5 2.5L12 5.5' fill='none' stroke='%231f6b3a' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/16px no-repeat;flex-shrink:0}
.top+*{margin-top:auto!important}body>:nth-last-child(2){margin-bottom:auto!important}
.foot{position:absolute;left:56px;right:56px;bottom:26px;color:#55666f;font-size:13px;display:flex;justify-content:space-between}
.arrow{flex:0 0 auto;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#55666f;font-size:13px;font-weight:600;gap:4px;text-align:center}
.arrow svg{display:block}
"""
ARR = '<svg width="44" height="16" viewBox="0 0 44 16"><path d="M2 8h36M32 2l8 6-8 6" fill="none" stroke="#77878d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
DOWN = '<svg width="16" height="26" viewBox="0 0 16 26"><path d="M8 2v18M2 15l6 7 6-7" fill="none" stroke="#77878d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
FOOT = '<div class="foot"><span>GTA AI Policy Check · proof of concept · not an official GTA tool</span><span>{}</span></div>'


def page(name, body, source):
    with open(os.path.join(OUT, name + '.html'), 'w', encoding='utf-8') as f:
        f.write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{name}</title><style>{CSS}</style></head><body style="position:relative">{body}{FOOT.format(E(source))}</body></html>')


def bars(rows, color="#0d5a61", label_w=230, bar_w=300):
    """Single-series horizontal bars: one hue, thin, 4px rounded data end, value at bar end."""
    mx = max(v for _, v in rows)
    out = []
    for name, v in rows:
        w = max(2, round(v / mx * bar_w))
        out.append(f'<div style="display:grid;grid-template-columns:{label_w}px {bar_w + 60}px;align-items:center;gap:12px;margin:0 0 10px">'
                   f'<span style="font-size:15px;text-align:right">{E(name)}</span>'
                   f'<span style="display:flex;align-items:center;gap:8px"><span style="display:block;height:14px;width:{w}px;background:{color};border-radius:0 4px 4px 0"></span>'
                   f'<span style="font-size:15px;font-weight:700;font-variant-numeric:tabular-nums">{v}</span></span></div>')
    return ''.join(out)


P = inv['provisions']
docs = inv['documents']
n_prov = len(P)
tiers_prov = C.Counter(e['tier'] for e in mp['elements'] for _ in e['provision_ids'])
tiers_el = C.Counter(e['tier'] for e in mp['elements'])
kinds = C.Counter(r['k'] for r in site)
vr = tri['verification_report']

# ---------------------------------------------------------------- 10 pipeline
steps = [
    ("Source", "7 GTA PDFs", "data/Instruments_GTA Policies/", "Policies, standards, guidelines and a web page (2023–2025)", "Extracted to data/source_text/ for the quote check"),
    ("Input", "stage1_inventory.json", "provision inventory", f"{n_prov} provisions, each with exact wording, section, page, modal verb as written and its reading · {len(inv['conflicts'])} conflicts · {len(mp['open_questions'])} open questions · {len(mp['unresolved_references'])} unresolved references",
     f"verify_sources.py: {n_prov}/{n_prov} quotes match the PDFs word for word"),
    ("partA.py", "stage2_map.json", "applicability map", f"{len(mp['elements'])} topics ({tiers_el['umbrella']} always shown, {tiers_el['conditional']} conditional, {tiers_el['out_of_scope_for_employee']} agency-only) · {len(mp['facts'])} facts · {len(mp['indirect_pointers'])} agency pointers",
     "Every provision in exactly one topic"),
    ("partB.py", "stage3_triage.json", "question tree and outcomes", f"{len(tri['questions'])} questions with skips and “Not sure” answers · {vr['distinct_outcomes']:,} distinct outcomes",
     f"{vr['number_of_paths']:,} answer paths checked against the map: {vr['mismatch_count']} mismatches"),
    ("decision_rights.py", "decision_rights.json", "who decides what", f"{dr['counts']['decisions']} decision points: {dr['counts']['named']} named, {dr['counts']['documents_disagree']} where documents disagree, {dr['counts']['not_named']} not named",
     "Every role quoted verbatim from its provision"),
    ("gen_site.py", "site/data.json", "what the page loads", f"{len(site)} records: questions, topics, pointers, next steps, decisions, guardrail factors and signs",
     "Step contacts, links and sign provisions asserted against the source"),
]
rows = []
for i, (who, file, what, holds, check) in enumerate(steps):
    rows.append(f'''<div class="card" style="display:grid;grid-template-columns:170px 300px 1fr 400px;align-items:center;gap:20px;padding:13px 20px">
      <span class="mono" style="font-size:15px;color:#0d5a61;font-weight:700">{E(who)}</span>
      <span><span class="mono" style="font-weight:700;font-size:16px">{E(file)}</span><br><span class="muted" style="font-size:14px">{E(what)}</span></span>
      <span style="font-size:15px">{E(holds)}</span>
      <span class="ok" style="font-size:14px">{E(check)}</span></div>''')
    if i < len(steps) - 1:
        rows.append(f'<div style="display:flex;justify-content:flex-start;padding-left:76px;height:22px;align-items:center">{DOWN}</div>')
body = f'''<div class="top"><div><div class="tag">Data pipeline</div><h1>From GTA documents to the page, checked at every step</h1>
<p class="sub">Python standard library only. Each step reads the one before it, and a rebuild reproduces the committed files byte for byte (CI fails otherwise).</p></div></div>
<div style="display:grid;grid-template-columns:170px 300px 1fr 400px;gap:20px;padding:0 21px 8px;font-size:13px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:#55666f"><span>Step</span><span>Output</span><span>What it holds</span><span>Built-in check</span></div>
{''.join(rows)}
<div class="card" style="margin-top:14px;padding:12px 20px;display:flex;align-items:center;gap:14px;background:#0d5a61;color:#fff;border-color:#0d5a61">
<span class="mono" style="font-weight:700">site/index.html</span><span>One static page loads data.json in the browser: questionnaire, results, exact wording, guardrails and next steps. No server-side code.</span></div>'''
page('10-data-pipeline', body, 'Counts read from the data files in this repository')

# ---------------------------------------------------------------- 11 at a glance
tiles = [(f"{n_prov}", "provisions"), (f"{len(docs)}", "GTA documents"), (f"{len(mp['elements'])}", "topics"),
         (f"{vr['number_of_paths']:,}", "answer paths verified"), (f"{len(inv['conflicts'])}", "conflicts between documents"),
         (f"{len(mp['open_questions'])}", "open questions"), (f"{len(mp['unresolved_references'])}", "unresolved references"), (f"{dr['counts']['decisions']}", "decision points")]
tile_html = ''.join(f'<div class="card" style="padding:14px 18px"><div style="font:500 40px/1.05 Georgia,serif;font-variant-numeric:tabular-nums">{a}</div><div class="muted" style="font-size:15px;margin-top:4px">{E(b)}</div></div>' for a, b in tiles)
by_doc = sorted(((f"{d['doc_id']} · {d['document_type'].replace('other', 'web page')}", d['provision_count']) for d in docs), key=lambda x: -x[1])
mod = C.Counter(p['modality'] for p in P)
MODN = [("must", "Must"), ("must_not", "Must not"), ("should", "Should"), ("should_not", "Should not"), ("may", "May"), ("informational", "Note (no obligation)")]
by_mod = [(n, mod[k]) for k, n in MODN]
by_tier = [("Always shown", tiers_prov['umbrella']), ("When answers match", tiers_prov['conditional']), ("Via agency pointers", tiers_prov['out_of_scope_for_employee'])]


def chart(title, note, rows, lw):
    return f'<div class="card" style="padding:18px 20px"><div style="font-weight:700;font-size:17px">{E(title)}</div><div class="muted" style="font-size:13px;margin:2px 0 14px">{E(note)}</div>{bars(rows, label_w=lw, bar_w=150)}</div>'


body = f'''<div class="top"><div><div class="tag">The data</div><h1>What the policy data contains</h1>
<p class="sub">Seven GTA AI documents broken into {n_prov} quoted provisions. Where the documents disagree or leave something unsettled, the data records it rather than choosing an answer.</p></div></div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:20px">{tile_html}</div>
<div style="display:grid;grid-template-columns:1.25fr 1fr 1.05fr;gap:18px">
{chart("Provisions by document", "Count of quoted provisions · 5GP = 5 Guiding Principles web page", by_doc, 190)}
{chart("Provisions by obligation", "Grouping; the modal verb as written is kept", by_mod, 150)}
{chart("Who sees them", "How provisions reach an employee", by_tier, 160)}
</div>'''
page('11-data-at-a-glance', body, 'Source: data/stage1_inventory.json, stage2_map.json, stage3_triage.json, decision_rights.json')

# ---------------------------------------------------------------- 12 record anatomy
ex = next(p for p in P if p['id'] == 'SS-25-001-1.3-2')
show = ['id', 'doc_id', 'section', 'page', 'lead_in_excerpt', 'text_excerpt', 'modality', 'modal_as_written', 'trigger_conditions']
NOTE = {'id': 'Stable ID: document · section · number', 'section': 'Citation: section and page', 'text_excerpt': 'Exact wording, checked against the PDF',
        'modality': 'Grouping used on the page', 'modal_as_written': 'The verb exactly as written', 'trigger_conditions': 'When it applies'}
lines = []
for k in show:
    v = ex[k]
    val = json.dumps(v, ensure_ascii=False)
    if len(val) > 74: val = val[:72] + '…"'
    note = f'<span style="color:#b86e00;font-family:system-ui;font-size:13px;font-weight:600;white-space:nowrap">← {E(NOTE[k])}</span>' if k in NOTE else ''
    lines.append(f'<div style="display:flex;justify-content:space-between;gap:12px;align-items:baseline"><span><span style="color:#0d5a61">"{k}"</span>: <span>{E(val)}</span>,</span>{note}</div>')
KIND = [("el", "Topics: summaries with their quoted provisions"), ("dec", "Decisions: who decides, quoted"), ("step", "Next steps: where to go, with links"),
        ("ptr", "Agency pointers"), ("q", "Questions and answer options"), ("factor", "Guardrail factors (posts)"), ("sign", "Stop and Check first signs"), ("meta", "Dates, notes, closing line"), ("stepgap", "Known gap in next steps")]
krows = ''.join(f'<div style="display:grid;grid-template-columns:96px 40px 1fr;gap:10px;align-items:center;margin:0 0 9px"><span class="mono chip k" style="margin:0;text-align:center">{k}</span>'
                f'<span style="font-weight:700;text-align:right;font-variant-numeric:tabular-nums">{kinds[k]}</span><span style="font-size:15px">{E(d)}</span></div>' for k, d in KIND)
body = f'''<div class="top"><div><div class="tag">Data format</div><h1>Anatomy of the JSON</h1>
<p class="sub">Every line the page shows traces back to one provision record, quoted word for word with its citation.</p></div></div>
<div style="display:grid;grid-template-columns:1.6fr 1fr;gap:22px">
<div class="card" style="padding:20px 22px"><div style="font-weight:700;margin-bottom:4px">One provision in <span class="mono">data/stage1_inventory.json</span></div>
<div class="muted" style="font-size:13px;margin-bottom:12px">1 of {n_prov} · selected fields</div>
<div class="mono" style="font-size:14px;line-height:1.75;background:#f6f8f8;border-radius:8px;padding:14px 16px">{{<div style="padding-left:18px">{''.join(lines)}</div>}}</div>
<div style="margin-top:14px;font-size:15px">Also on every record: addressee, definitions used, notes, and a <span class="mono">classification_basis</span> wherever the grouping isn’t the literal verb ({sum(1 for p in P if p.get('classification_basis'))} records).</div></div>
<div class="card" style="padding:20px 22px"><div style="font-weight:700;margin-bottom:4px"><span class="mono">site/data.json</span>: what the page loads</div>
<div class="muted" style="font-size:13px;margin-bottom:16px">{len(site)} records, one per line, keyed by <span class="mono">k</span></div>{krows}</div></div>'''
page('12-data-records', body, 'Example: SS-25-001 section 1.3, page 3')

# ---------------------------------------------------------------- 13 tech stack
LAYERS = [
    ("Content", ["7 GTA PDFs", "pdftotext (poppler)"], "Source documents and their extracted text", False),
    ("Build", ["Python 3.11+", "Standard library only", "6 pipeline scripts"], "Inventory → map → question tree → page data", False),
    ("Data", ["JSON", "Markdown renderings"], "Provisions, topics, questions, decisions, guardrail rules", False),
    ("Front end", ["One HTML file", "Vanilla JavaScript", "CSS (light, dark, print)", "System fonts"], "No framework, no build step, no third-party requests", False),
    ("Quality", ["Playwright (Python)", "Chromium", "8 browser test suites", "Accessibility audit", "Source verifier"], "WCAG 2.1 AA checks: contrast, targets, reflow, focus", False),
    ("Delivery", ["GitHub", "GitHub Actions CI", "GitHub Pages"], "Rebuild must match, then tests, then publish", False),
    ("Backend (planned)", ["Azure Static Web Apps", "Azure Functions (Python)", "Azure SQL (serverless)", "Power BI", "Key Vault", "Application Insights", "Bicep"], "Usage data and trends: see docs/backend_plan.md", True),
]
lrows = []
for name, chips, note, planned in LAYERS:
    bg = "#fdf0d5" if planned else "#fff"
    pill = '<span style="display:inline-block;margin-left:8px;font-size:12px;font-weight:700;color:#8a4f00;border:1px solid #b86e00;border-radius:999px;padding:1px 8px;vertical-align:2px">PLANNED</span>' if planned else ''
    lrows.append(f'''<div class="card" style="display:grid;grid-template-columns:210px 1fr 360px;gap:20px;align-items:center;padding:14px 20px;background:{bg}">
<span style="font-weight:700;font-size:18px">{E(name.replace(" (planned)", ""))}{pill}</span>
<span>{''.join(f'<span class="chip{" k" if not planned else ""}" style="{"background:#fff;border:1px solid #e0c48f;color:#5c3700" if planned else ""}">{E(c)}</span>' for c in chips)}</span>
<span class="muted" style="font-size:15px">{E(note)}</span></div>''')
body = f'''<div class="top"><div><div class="tag">Tech stack</div><h1>Small, static and dependency-free</h1>
<p class="sub">The running tool is one HTML file and one JSON file. Everything else exists to build that data and prove it is right.</p></div></div>
<div style="display:flex;flex-direction:column;gap:12px">{''.join(lrows)}</div>'''
page('13-tech-stack', body, 'Runtime dependencies: none · Development dependency: playwright==1.65.2')


# ---------------------------------------------------------------- 14 / 15 architecture
def box(title, items, sub="", dark=False, w=None, accent=None):
    style = f"flex:1 1 0;min-width:0;padding:18px 18px" + (f";flex:0 0 {w}px" if w else "")
    if dark: style += ";background:#0d5a61;color:#fff;border-color:#0d5a61"
    if accent: style += f";border-top:4px solid {accent}"
    li = ''.join(f'<li style="margin:0 0 6px">{x}</li>' for x in items)
    return f'<div class="card" style="{style}"><div style="font-weight:800;font-size:21px">{title}</div>{f"<div style=\'font-size:14px;margin-top:2px;opacity:.8\'>{sub}</div>" if sub else ""}<ul style="margin:14px 0 0;padding-left:18px;font-size:17px;line-height:1.4">{li}</ul></div>'


def arrow(label=""):
    return f'<div class="arrow" style="width:96px">{E(label)}{ARR}</div>'


def note(text, color="#1f6b3a", bg="#dff0e3"):
    return f'<div style="background:{bg};color:{color};border-radius:8px;padding:14px 16px;font-size:17px;font-weight:600">{text}</div>'


flow = (box("Repository", ["<span class='mono'>data/</span> source PDFs, text, JSON", "<span class='mono'>scripts/</span> Python pipeline", "<span class='mono'>site/</span> index.html + data.json", "<span class='mono'>tests/</span> browser tests"], "GitHub")
        + arrow("on push") +
        box("GitHub Actions", ["<b>CI</b>: rebuild must match, source check, 8 test suites, accessibility gate", "<b>Pages</b>: publish <span class='mono'>site/</span> from main"], "Automation")
        + arrow("deploy") +
        box("GitHub Pages", ["Static hosting, HTTPS", "Two files: index.html, data.json", "No server-side code", "noindex"], "Hosting")
        + arrow("HTTPS GET") +
        box("Visitor’s browser", ["Title screen, 7 questions, results", "All logic runs here", "Agency and email kept in localStorage only", "Sends nothing back"], "Runtime", dark=True))
body = f'''<div class="top"><div><div class="tag">Architecture · today</div><h1>Proof of concept: a static site with no backend</h1>
<p class="sub">Nothing a visitor types leaves their browser. The tests fail if any request goes off the site’s own origin.</p></div></div>
<div style="display:flex;align-items:stretch;gap:0">{flow}</div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-top:26px">
{note("No database, accounts or API to secure")}
{note("Every quote checked against the PDFs before publish")}
{note("Cost: free on GitHub Pages for a public repository")}</div>
<div class="card" style="margin-top:22px;padding:16px 20px;display:flex;gap:18px;align-items:center">
<span style="font-weight:700;white-space:nowrap">Content updates</span><span class="muted" style="font-size:15px">Add or replace a PDF → extract text → update the inventory → run the five pipeline steps → CI proves the quotes and every answer path → merge to main → Pages republishes.</span></div>'''
page('14-architecture-current', body, 'Workflows: .github/workflows/ci.yml, pages.yml')

AZ = "#0d5a61"
flow = (box("Browser", ["Same static page", "Sends enum-only events in batches (sendBeacon)", "Opt-out and Global Privacy Control respected"], "Visitor", dark=True, w=250)
        + arrow("POST /api/events") +
        box("Azure Static Web Apps", ["Hosts the page and the API on one origin", "Custom domain, HTTPS", "CORS locked to the site"], "Standard plan", accent=AZ)
        + arrow("") +
        box("Azure Functions", ["Validates against allow-lists generated from data.json", "Drops anything unknown", "Never logs request bodies"], "Python, HTTP trigger", accent=AZ)
        + arrow("managed identity") +
        box("Azure SQL", ["<b>usage</b>: sessions, events, answers", "<b>contacts</b>: opt-in emails, encrypted, separate role", "13-month raw retention, then roll-up"], "Serverless, auto-pause", accent=AZ)
        + arrow("views") +
        box("Power BI", ["Weekly trends by agency", "Counts under 5 suppressed", "Row-level security by agency"], "Dashboards", accent=AZ, w=230))
support = ''.join(f'<div class="card" style="padding:12px 16px"><div style="font-weight:700">{a}</div><div class="muted" style="font-size:14px">{b}</div></div>' for a, b in [
    ("Key Vault", "Secrets; no passwords in code"), ("Application Insights", "Health only; IP masking on; 30-day logs"),
    ("Front Door WAF", "Rate limits (hardening phase)"), ("GitHub Actions + Bicep", "OIDC deploys to dev, test, prod")])
body = f'''<div class="top"><div><div class="tag">Architecture · planned</div><h1>Usage data and trends on Microsoft Azure</h1>
<p class="sub">Collects what people ask and what the tool answers, never who they are. Emails, given only by choice, are stored apart and never joined to usage.</p></div>
<span style="flex-shrink:0;font-size:13px;font-weight:700;color:#8a4f00;border:1.5px solid #b86e00;background:#fdf0d5;border-radius:999px;padding:4px 12px">PLANNED · NOT BUILT</span></div>
<div style="display:flex;align-items:stretch">{flow}</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:22px">{support}</div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-top:20px">
{note("No free text, IP addresses or cross-visit IDs stored")}
{note("Session ID lasts one visit (sessionStorage)")}
{note("Needs sign-off: notice, agency list, retention", "#8a4f00", "#fdf0d5")}</div>'''
page('15-architecture-azure', body, 'Plan: docs/backend_plan.md')
print('built')
