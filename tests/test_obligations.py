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
            if await pg.inner_text("#obltotal") != "0" or await pg.locator("#obllegend li").count():
                bad.append("count is not 0 before the first answer")
            prev = 0
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
                legend = dict(zip([t.strip() for t in await pg.locator("#obllegend button span:first-child").all_inner_texts()],
                                  [int(t) for t in await pg.locator("#obllegend b").all_inner_texts()]))
                want_legend = {NAME[m]: c[m] for m in OBL if c[m]}
                delta = await pg.inner_text("#obldelta")
                d = total - prev; prev = total
                want_delta = f"+{d} from your last answer" if d > 0 else f"−{-d} from your last answer" if d < 0 else "No new rules from your last answer"
                if got != total or legend != want_legend or delta != want_delta:
                    bad.append(dict(after=fact, got=(got, legend, delta), want=(total, want_legend, want_delta)))
                totals.append(got)
            # each legend row opens the results grouped by obligation, at a section whose count matches the panel
            rows = await pg.locator("#obllegend button").count()
            for i in range(rows):
                label = (await pg.locator("#obllegend button span:first-child").nth(i).inner_text()).strip()
                n = (await pg.locator("#obllegend b").nth(i).inner_text()).strip()
                await pg.locator("#obllegend button").nth(i).click(); await pg.wait_for_timeout(60)
                head = await pg.evaluate("document.activeElement.textContent")
                if head != f"{label} ({n})": bad.append(dict(legend=(label, n), landed_on=head))
            # every result page ends with Start over, which returns to the first question with the count at 0
            if rows or name == "no AI":
                if name != "no AI": await pg.get_by_role("tab", name="What applies").click()
                await pg.locator("#main button", has_text="Start over").click(); await pg.wait_for_timeout(60)
                if await pg.inner_text("#qh") != "What kind of AI is it?" or await pg.inner_text("#obltotal") != "0":
                    bad.append("Start over did not return to the first question with 0 rules")
            status = await pg.inner_text("#status")
            note = await pg.inner_text("#oblnote")
            moved = len(set(totals)) > 1 or name == "no AI"
            good = not bad and moved and not errs and ("rules apply to you" in status or not any(totals))  # an unchanged 0 is not re-announced
            if not good: print("   debug:", dict(moved=moved, status=status))
            ok &= good
            print(f"{name}: totals {' → '.join(map(str, totals))} | note: {note!r} | {'PASS' if good else 'FAIL'} {bad[:2]} {errs}")
            await pg.close()
        await b.close()
    print("ALL PASS" if ok else "FAILED")
    sys.exit(0 if ok else 1)

asyncio.run(main())
