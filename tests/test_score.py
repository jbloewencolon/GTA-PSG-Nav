import os as _os; ROOT = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
"""Guardrails and signs. Posts come from what the user described, not from how many rules match:
personal or sensitive data 2, a decision about a person 2, public-facing 1, buying or building 1,
AI content in an official document 1, legal analysis or meeting note-taking 1. Not sure counts as yes.
Levels: 0 Baseline rules only, 1-2 Light, 3-4 Standard, 5+ Extra. Red stop: GTA approval required or
the use may be prohibited (generative AI). Amber check: a review or authorization first (other AI).

Part 1 (data): over every route with one or two tasks, compares the page's data-driven rules (factor and
sign records in data.json) with the independent calculation below, and checks that every quoted
provision is one the page shows on that route.
Part 2 (page): drives the page and compares the rail and banners with the independent calculation.
Needs the site served on localhost:8765.
"""
import asyncio, itertools, json, sys
from playwright.async_api import async_playwright

D = json.load(open(_os.path.join(ROOT, "site", "data.json"), encoding="utf-8"))
META = [r for r in D if r["k"] == "meta"][0]
Q = [r for r in D if r["k"] == "q"]
EL = [r for r in D if r["k"] == "el"]
PT = [r for r in D if r["k"] == "ptr"]
FACTORS = [r for r in D if r["k"] == "factor"]
SIGNS = [r for r in D if r["k"] == "sign"]
LV = ["Baseline rules only", "Light", "Standard", "Extra"]
NS = "not_sure"


def has(l, v): return any(x in l for x in v) if isinstance(v, list) else v in l
def match(c, f): return c == "always" or any(all(k in f and has(a[k], f[k]) for k in a) for a in c)
def asked(q, f): return q["ask_if"] == "always" or match([q["ask_if"]], f)
def level(n): return 0 if n == 0 else 1 if n <= 2 else 2 if n <= 4 else 3
def posts_label(n): return f"{n} post" if n == 1 else f"{n} posts"


def prune(f):
    f = dict(f)
    for q in Q:
        if q["fact"] in f and not asked(q, f): del f[q["fact"]]
    return f


# ---- independent calculation (the approved design, written without the data's 'when' conditions) ----
def expected(f):
    if f.get("F_TYPE") == "none": return 0, []
    oth = f.get("F_TYPE") == "other"
    tasks = f.get("F_TASK", [])
    tasks = tasks if isinstance(tasks, list) else [tasks]
    yes = lambda k: f.get(k) in ("yes", NS)
    buy = f.get("F_ROLE") in ("procure", "both", NS)
    n = 0
    n += 2 if yes("F_DATA") else 0
    n += 1 if f.get("F_ROLE") not in (None, "use_only") else 0
    if not oth:
        n += 2 if yes("F_DECISION") else 0
        n += 1 if set(tasks) & {"chatbot_public", "public_comms", NS} else 0
        n += 1 if f.get("F_PRODUCT") in ("official", NS) else 0
        n += 1 if set(tasks) & {"legal", "meetings", NS} else 0
        signs = [("stop", "SS-25-001-1.3-2")] * yes("F_DATA") + [("stop", "SS-25-001-1.5-1")] * buy + [("stop", "SS-25-001-3.0-TABLE-15")] * yes("F_DECISION")
    else:
        signs = [("check", "PS-23-001-POLICY-1")] * buy + [("check", "SS-23-002-6-2")] * yes("F_DATA")
    return n, sorted(signs)


# ---- the page's rules, mirrored from index.html (factorsNow / signsNow) ----
def from_data(f):
    if match(META["gate"]["when"], f): return 0, [], []
    oth = match(META["when_other"], f)
    n, quoted = 0, []
    for fa in FACTORS:
        for v in fa["variants"]:
            p = v["oprov"] if oth else v["prov"]
            if p and match(v["when"], f):
                n += fa["posts"]; quoted.append(p["id"]); break
    sg = [s for s in SIGNS if (s["branch"] == "other") == oth and match(s["when"], f)]
    return n, sorted((s["level"], s["pid"]) for s in sg), quoted + [s["pid"] for s in sg]


def shown(f):
    if match(META["gate"]["when"], f): return set()
    oth = match(META["when_other"], f)
    sts = lambda e: e["other"] if oth else e["statements"]
    els = [e for e in EL if sts(e) and (e["tier"] == "umbrella" or match(e["when"], f))]
    pts = [p for p in PT if match(p["when"], f) and (not oth or p["o_as_written"])]
    return {p["id"] for e in els for s in sts(e) for p in s["prov"]} | {p["id"] for q in pts for p in (q["oprov"] if oth else q["prov"])}


def part1():
    QF = {q["fact"]: q for q in Q}
    tasks = [o["value"] for o in QF["F_TASK"]["options"]]
    task_sets = [[t] for t in tasks] + [list(c) for c in itertools.combinations([t for t in tasks if t != NS], 2)]
    rest = [q for q in Q if q["fact"] not in ("F_TYPE", "F_TASK")]
    seen, n, bad = set(), 0, 0
    for ty in [o["value"] for o in QF["F_TYPE"]["options"]]:
        for ts in task_sets:
            for vals in itertools.product(*[[o["value"] for o in q["options"]] for q in rest]):
                f = prune(dict({"F_TYPE": ty, "F_TASK": ts}, **{q["fact"]: v for q, v in zip(rest, vals)}))
                key = json.dumps(f, sort_keys=True)
                if key in seen: continue
                seen.add(key); n += 1
                got_n, got_s, quoted = from_data(f)
                exp_n, exp_s = expected(f)
                missing = [i for i in quoted if i not in shown(f)]
                if (got_n, got_s) != (exp_n, exp_s) or missing:
                    bad += 1
                    if bad <= 5: print("MISMATCH", f, (got_n, got_s), (exp_n, exp_s), "not shown:", missing)
    print(f"part 1: {n} routes, data rules vs independent calculation and quoted provisions shown, {bad} mismatches")
    return bad == 0


G = "Generative AI that writes"
CASES = [
    ("ordinary one task", [G, ["Looking up"], "No, it only helped", "No, I only use the tool", "No, only publicly available", "No"],
     {"F_TYPE": "generative", "F_TASK": ["research"], "F_PRODUCT": "none", "F_ROLE": "use_only", "F_DATA": "no", "F_DECISION": "no"}),
    ("flashcards stay baseline", [G, ["Creating education or training"], "No, it only helped", "No, I only use the tool", "No, only publicly available"],
     {"F_TYPE": "generative", "F_TASK": ["education_training"], "F_PRODUCT": "none", "F_ROLE": "use_only", "F_DATA": "no"}),
    ("legal analysis", [G, ["Legal or regulatory"], "No, it only helped", "No, I only use the tool", "No, only publicly available", "No"],
     {"F_TYPE": "generative", "F_TASK": ["legal"], "F_PRODUCT": "none", "F_ROLE": "use_only", "F_DATA": "no", "F_DECISION": "no"}),
    ("public chatbot, official", [G, ["members of the public interact", "used only by state staff"], "Yes, in something more official", "No, I only use the tool", "No, only publicly available", "No"],
     {"F_TYPE": "generative", "F_TASK": ["chatbot_public", "chatbot_internal"], "F_PRODUCT": "official", "F_ROLE": "use_only", "F_DATA": "no", "F_DECISION": "no"}),
    ("building, public, official", [G, ["Writing for the public"], "Yes, in something more official", "Yes, building", "No, only publicly available", "No"],
     {"F_TYPE": "generative", "F_TASK": ["public_comms"], "F_PRODUCT": "official", "F_ROLE": "build", "F_DATA": "no", "F_DECISION": "no"}),
    ("data and decisions", [G, ["Analyzing data"], "Yes, in something more official", "No, I only use the tool", "Yes", "Yes"],
     {"F_TYPE": "generative", "F_TASK": ["data_analysis"], "F_PRODUCT": "official", "F_ROLE": "use_only", "F_DATA": "yes", "F_DECISION": "yes"}),
    ("not sure on data", [G, ["Looking up"], "No, it only helped", "No, I only use the tool", ".ns", "No"],
     {"F_TYPE": "generative", "F_TASK": ["research"], "F_PRODUCT": "none", "F_ROLE": "use_only", "F_DATA": NS, "F_DECISION": "no"}),
    ("buying, ordinary task", [G, ["Looking up"], "No, it only helped", "Yes, buying", "No, only publicly available", "No"],
     {"F_TYPE": "generative", "F_TASK": ["research"], "F_PRODUCT": "none", "F_ROLE": "procure", "F_DATA": "no", "F_DECISION": "no"}),
    ("other AI with data", ["Other AI that predicts", "No, I only use the tool", "Yes"],
     {"F_TYPE": "other", "F_ROLE": "use_only", "F_DATA": "yes"}),
    ("other AI, buying", ["Other AI that predicts", "Yes, buying", "No, only publicly available"],
     {"F_TYPE": "other", "F_ROLE": "procure", "F_DATA": "no"}),
    ("other AI, building only", ["Other AI that predicts", "Yes, building", "No, only publicly available"],
     {"F_TYPE": "other", "F_ROLE": "build", "F_DATA": "no"}),
]


async def part2():
    ok = True
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=_os.environ.get("CHROME_PATH", "/usr/bin/google-chrome"), args=["--no-sandbox"])
        for name, clicks, facts in CASES:
            pg = await b.new_page(viewport={"width": 1180, "height": 900})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto("http://localhost:8765/index.html"); await pg.fill("#agency", "Test agency"); await pg.click("#start"); await pg.wait_for_selector(".opt")
            for c in clicks:
                if isinstance(c, list):
                    for t in c: await pg.locator(".opts.multi .opt", has_text=t).first.click()
                    await pg.get_by_role("button", name="Continue", exact=True).click()
                elif c == ".ns":
                    await pg.locator(".opt.ns").first.click()
                    await pg.get_by_role("button", name="Continue", exact=True).click()
                else:
                    await pg.locator(".opt", has_text=c).first.click()
            await pg.wait_for_selector(".closing")
            n, signs = expected(facts)
            stops = [s for s in signs if s[0] == "stop"]; checks = [s for s in signs if s[0] == "check"]
            mode = "stop" if stops else "check" if checks else ""
            exp = "Stop and check first" if stops else "Check first" if checks else f"{LV[level(n)]} · {posts_label(n)}"
            got = await pg.inner_text("#level")
            why = await pg.locator("#stopwhy li").count()
            red = await pg.locator(".stopban:not(.check) .sreason").count()
            amber = await pg.locator(".stopban.check .sreason").count()
            reasons = await pg.locator("#drivers li").count()
            sign_ok = await pg.locator(f"#gbox.{mode}").count() == 1 if mode else await pg.locator("#gbox.stop, #gbox.check").count() == 0
            vt = await pg.get_attribute("#thermo", "aria-valuetext")
            good = (got == exp and why == len(signs) and red == len(stops) and amber == len(checks) and sign_ok
                    and vt == f"{LV[level(n)]} guardrails, {posts_label(n)}" and (reasons > 0) == (n > 0) and not errs)
            ok &= good
            print(f"{name}: page {got!r} expected {exp!r} | posts {n} | reasons {reasons} | signs {why}/{len(signs)} red {red} amber {amber} | {'PASS' if good else 'FAIL'} {errs}")
            await pg.close()
        await b.close()
    return ok


if __name__ == "__main__":
    ok = part1()
    ok = asyncio.run(part2()) and ok
    print("ALL PASS" if ok else "FAILED")
    sys.exit(0 if ok else 1)
