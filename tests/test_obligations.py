"""'Rules that apply to you': the count and its obligation breakdown must match the data after every
answer, rise when an answer adds rules, and leave out Notes and agency-only rules. Needs the site
served on localhost:8765.
"""
import asyncio, json, os, sys
from playwright.async_api import async_playwright

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
D = json.load(open(os.path.join(ROOT, "site", "data.json"), encoding="utf-8"))
META = [r for r in D if r["k"] == "meta"][0]
Q = [r for r in D if r["k"] == "q"]
EL = [r for r in D if r["k"] == "el"]
OBL = ["must", "must_not", "should", "should_not", "may"]
NAME = {"must": "Must", "must_not": "Must not", "should": "Should", "should_not": "Should not", "may": "May"}


def has(l, v): return any(x in l for x in v) if isinstance(v, list) else v in l
def match(c, f): return c == "always" or any(all(k in f and has(a[k], f[k]) for k in a) for a in c)


def expected(f):
    """Independent count: provisions in always-shown topics plus topics the answers trigger, by modality."""
    c = {m: 0 for m in OBL + ["informational"]}
    if match(META["gate"]["when"], f): return c, 0
    oth = match(META["when_other"], f)
    added = 0
    for e in EL:
        if e["tier"] != "umbrella" and not match(e["when"], f): continue
        for s in (e["other"] if oth else e["statements"]):
            c[s["m"]] += len(s["prov"])
            if e["tier"] == "conditional" and s["m"] != "informational": added += len(s["prov"])
    return c, added


G = "Generative AI that writes"
ROUTES = [
    ("coding, nothing sensitive", [("F_TYPE", "generative", G), ("F_TASK", ["coding"], ["Writing, reviewing"]), ("F_PRODUCT", "none", "No, it only helped"),
                                   ("F_ROLE", "use_only", "No, I only use"), ("F_DATA", "no", "No, only publicly"), ("F_DECISION", "no", "No")]),
    ("public writing with personal data", [("F_TYPE", "generative", G), ("F_TASK", ["public_comms"], ["Writing for the public"]), ("F_PRODUCT", "official", "Yes, in something more official"),
                                           ("F_ROLE", "build", "Yes, building"), ("F_DATA", "yes", "Yes"), ("F_DECISION", "yes", "Yes")]),
    ("other AI, buying", [("F_TYPE", "other", "Other AI that predicts"), ("F_ROLE", "procure", "Yes, buying"), ("F_DATA", "yes", "Yes")]),
    ("no AI", [("F_TYPE", "none", "It does not use AI")]),
]


async def main():
    ok = True
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get("CHROME_PATH", "/usr/bin/google-chrome"), args=["--no-sandbox"])
        for name, steps in ROUTES:
            pg = await b.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto("http://localhost:8765/index.html"); await pg.fill("#agency", "Test agency"); await pg.click("#start"); await pg.wait_for_selector(".opt")
            facts, trail, bad, totals = {}, [], [], []
            for fact, value, click in steps:
                if isinstance(click, list):
                    for t in click: await pg.locator(".opts.multi .opt", has_text=t).first.click()
                    await pg.get_by_role("button", name="Continue", exact=True).click()
                else:
                    await pg.locator(".opt", has_text=click).first.click()
                await pg.wait_for_timeout(80)
                facts[fact] = value
                c, added = expected(facts)
                total = sum(c[m] for m in OBL)
                got = int(await pg.inner_text("#obltotal"))
                legend = dict(zip([t.strip() for t in await pg.locator("#obllegend span").all_inner_texts()],
                                  [int(t) for t in await pg.locator("#obllegend b").all_inner_texts()]))
                want_legend = {NAME[m]: c[m] for m in OBL if c[m]}
                delta = await pg.inner_text("#obldelta")
                want_delta = f"+{added} from your answers" if added else ""
                if got != total or legend != want_legend or delta != want_delta:
                    bad.append(dict(after=fact, got=(got, legend, delta), want=(total, want_legend, want_delta)))
                totals.append(got)
            status = await pg.inner_text("#status")
            note = await pg.inner_text("#oblnote")
            moved = len(set(totals)) > 1 or name == "no AI"
            good = not bad and moved and not errs and ("rules apply to you" in status)
            ok &= good
            print(f"{name}: totals {' → '.join(map(str, totals))} | note: {note!r} | {'PASS' if good else 'FAIL'} {bad[:2]} {errs}")
            await pg.close()
        await b.close()
    print("ALL PASS" if ok else "FAILED")
    sys.exit(0 if ok else 1)

asyncio.run(main())
