import os as _os; ROOT = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
import asyncio, json, sys
from playwright.async_api import async_playwright
O = json.load(open(_os.path.join(ROOT, "data", "stage3_triage.json")))["outcomes"]
D = json.load(open(_os.path.join(ROOT, "site", "data.json")))
STEPS = [r for r in D if r.get("k") == "step"]

async def adv(pg):
    """Question 2 allows several answers, so it waits for Continue."""
    if await pg.locator('.opts.multi .opt[aria-pressed="true"]').count():
        await pg.get_by_role("button", name="Continue", exact=True).click()

def match(c, f): return c == "always" or any(all(f.get(k) in v for k, v in a.items()) for a in c)
def shown_ids(f):
    oth = match(O["type_rule"]["when_other"], f); key = "other_ai_statements" if oth else "statements"
    els = O["always"]["umbrella_elements"] + [b["element"] for b in O["blocks"] if match(b["when"], f)]
    ps = O["always"]["indirect_pointers"] + [b["pointer"] for b in O["conditional_pointers"] if match(b["when"], f)]
    ids = {i for e in els for s in e[key] for i in s["provision_ids"]}
    ids |= {i for p in ps for i in (p["other_ai_provision_ids"] if oth else p["provision_ids"])}
    return ids
CASES = [("public_chatbot", ["Generative AI that writes", "members of the public interact", "Yes, in something more official", "No, I only use the tool", "No, only publicly available", "No"],
          {"F_TYPE": "generative", "F_TASK": "chatbot_public", "F_PRODUCT": "official", "F_ROLE": "use_only", "F_DATA": "no", "F_DECISION": "no"}),
         ("gen_notsure_all", ["Generative AI that writes", ".ns", ".ns", ".ns", ".ns", ".ns"], {"F_TYPE": "generative", "F_TASK": "not_sure", "F_PRODUCT": "not_sure", "F_ROLE": "not_sure", "F_DATA": "not_sure", "F_HOST": "not_sure"}),
         ("other_both", ["Other AI that predicts", "Both buying and building", "Yes"], {"F_TYPE": "other", "F_ROLE": "both", "F_DATA": "yes"})]
async def main():
    ok = True
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=_os.environ.get("CHROME_PATH", "/usr/bin/google-chrome"), args=["--no-sandbox"])
        for name, clicks, facts in CASES:
            pg = await b.new_page(viewport={"width": 1180, "height": 900}); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto("http://localhost:8765/index.html"); await pg.wait_for_selector(".opt")
            for c in clicks:
                if c == ".ns": await pg.locator(".opt.ns").first.click()
                else: await pg.locator(".opt", has_text=c).first.click(); await adv(pg)
                if await pg.locator("text=Continue").count() and c == ".ns": await pg.locator("text=Continue").click()
            await pg.wait_for_selector(".closing")
            ids = shown_ids(facts); exp = [s for s in STEPS if s["pid"] in ids]
            await pg.locator("#tab-steps").click()
            n = await pg.locator(".step:not(.dec)").count()
            titles = await pg.locator(".step:not(.dec) h3").all_text_contents()
            good = n == len(exp) and sorted(titles) == sorted(s["title"] for s in exp) and not errs; ok &= good
            print(f"{name}: steps {n} expected {len(exp)} | {'PASS' if good else 'FAIL'} | risk {await pg.inner_text('#level')} | {titles} {errs}")
            await pg.screenshot(path=f"{ROOT}/tests/screenshots/v4_{name}.png")
            await pg.close()
        await b.close()
    sys.exit(0 if ok else 1)
asyncio.run(main())
