import os as _os; ROOT = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
"""Risk count (Model C): checks the page's score and band against an independent Python
calculation. Each rule counts once; task-only topics weigh 1, other topics 2, personal or
sensitive information and decisions about people 4 (prohibitions count double)."""
import asyncio, json, sys
from playwright.async_api import async_playwright

D = json.load(open(_os.path.join(ROOT, "site", "data.json")))
EL = [r for r in D if r["k"] == "el" and r["tier"] == "conditional"]
BANDS = ["No extra", "Light", "Standard", "Extra", "Full"]


def has(l, v): return any(x in l for x in v) if isinstance(v, list) else v in l
def match(c, f): return c == "always" or any(all(has(a[k], f.get(k)) for k in a) for a in c)


def weight(e):
    if all(set(a) <= {"F_TASK", "F_HOST"} for a in e["when"]): return 1
    return 4 if e["id"] in ("C_DATA", "C_DECISIONS") else 2


def score(f):
    oth = f["F_TYPE"] == "other"
    ids, total = [], 0
    for e in EL:
        if not match(e["when"], f): continue
        for s in (e["other"] if oth else e["statements"]):
            for p in s["prov"]:
                ids.append(p["id"]); total += weight(e) * {"must": 1, "must_not": 2}.get(s["m"], 0)
    assert len(ids) == len(set(ids)), "a rule would count twice"
    return total


def stops(f):
    """Stop sign: GenAI provisions that require GTA approval or list the use as prohibited."""
    if f["F_TYPE"] == "other": return []
    out = []
    if f.get("F_DATA") in ("yes", "not_sure"): out.append("SS-25-001-1.3-2")
    if f.get("F_ROLE") in ("procure", "both", "not_sure"): out.append("SS-25-001-1.5-1")
    if f.get("F_DECISION") in ("yes", "not_sure"): out.append("SS-25-001-3.0-TABLE-15")
    return out


def band(t): return 0 if t == 0 else 1 if t < 10 else 2 if t < 26 else 3 if t < 50 else 4


G = "Generative AI that writes"
CASES = [
    ("ordinary one task", [G, ["Looking up"], "No, it only helped", "No, I only use the tool", "No, only publicly available", "No"],
     {"F_TYPE": "generative", "F_TASK": ["research"], "F_PRODUCT": "none", "F_ROLE": "use_only", "F_DATA": "no", "F_DECISION": "no"}),
    ("ordinary three tasks", [G, ["Looking up", "Writing, reviewing", "Generating images"], "No, it only helped", "No, I only use the tool", "No, only publicly available", "No"],
     {"F_TYPE": "generative", "F_TASK": ["research", "coding", "media"], "F_PRODUCT": "none", "F_ROLE": "use_only", "F_DATA": "no", "F_DECISION": "no"}),
    ("shared chatbot rules once", [G, ["members of the public interact", "used only by state staff"], "Yes, in something more official", "No, I only use the tool", "No, only publicly available", "No"],
     {"F_TYPE": "generative", "F_TASK": ["chatbot_public", "chatbot_internal"], "F_PRODUCT": "official", "F_ROLE": "use_only", "F_DATA": "no", "F_DECISION": "no"}),
    ("personal data", [G, ["Looking up"], "No, it only helped", "No, I only use the tool", "Yes", "No"],
     {"F_TYPE": "generative", "F_TASK": ["research"], "F_PRODUCT": "none", "F_ROLE": "use_only", "F_DATA": "yes", "F_DECISION": "no"}),
    ("data and decisions", [G, ["Analyzing data"], "Yes, in something more official", "No, I only use the tool", "Yes", "Yes"],
     {"F_TYPE": "generative", "F_TASK": ["data_analysis"], "F_PRODUCT": "official", "F_ROLE": "use_only", "F_DATA": "yes", "F_DECISION": "yes"}),
    ("not sure on data", [G, ["Looking up"], "No, it only helped", "No, I only use the tool", ".ns", "No"],
     {"F_TYPE": "generative", "F_TASK": ["research"], "F_PRODUCT": "none", "F_ROLE": "use_only", "F_DATA": "not_sure", "F_DECISION": "no"}),
    ("buying, ordinary task", [G, ["Looking up"], "No, it only helped", "Yes, buying", "No, only publicly available", "No"],
     {"F_TYPE": "generative", "F_TASK": ["research"], "F_PRODUCT": "none", "F_ROLE": "procure", "F_DATA": "no", "F_DECISION": "no"}),
    ("decision only", [G, ["Analyzing data"], "No, it only helped", "No, I only use the tool", "No, only publicly available", "Yes"],
     {"F_TYPE": "generative", "F_TASK": ["data_analysis"], "F_PRODUCT": "none", "F_ROLE": "use_only", "F_DATA": "no", "F_DECISION": "yes"}),
    ("other AI with data", ["Other AI that predicts", "No, I only use the tool", "Yes"],
     {"F_TYPE": "other", "F_ROLE": "use_only", "F_DATA": "yes"}),
]


async def main():
    ok = True
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=_os.environ.get("CHROME_PATH", "/usr/bin/google-chrome"), args=["--no-sandbox"])
        for name, clicks, facts in CASES:
            pg = await b.new_page(viewport={"width": 1180, "height": 900})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto("http://localhost:8765/index.html"); await pg.wait_for_selector(".opt")
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
            got = await pg.inner_text("#level")
            t = score(facts); st = stops(facts)
            exp = "Stop and check first" if st else f"{BANDS[band(t)]} · {t}"
            why = await pg.locator("#stopwhy li").count()
            ban = await pg.locator(".stopban .sreason:visible").count()
            sign = await pg.locator("#gbox.stop").count()
            vt = await pg.get_attribute("#thermo", "aria-valuetext")
            good = got == exp and why == len(st) and ban == len(st) and sign == (1 if st else 0) and vt == f"{BANDS[band(t)]} guardrails, {t} points" and not errs
            ok &= good
            print(f"{name}: page {got!r} expected {exp!r} | score {t} | stop reasons {why}/{len(st)} banner {ban} | {'PASS' if good else 'FAIL'} {errs}")
            await pg.close()
        await b.close()
    sys.exit(0 if ok else 1)
asyncio.run(main())
