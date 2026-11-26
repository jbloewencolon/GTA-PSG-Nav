import os as _os; ROOT = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
import asyncio, json, sys
from playwright.async_api import async_playwright
O = json.load(open(_os.path.join(ROOT, "data", "stage3_triage.json"), encoding='utf-8'))["outcomes"]

async def adv(pg):
    """Question 2 allows several answers, so it waits for Continue."""
    if await pg.locator('.opts.multi .opt[aria-pressed="true"]').count():
        await pg.get_by_role("button", name="Continue", exact=True).click()

def match(c, f): return c == "always" or any(all(f.get(k) in v for k, v in a.items()) for a in c)
def expected(f):
    oth = match(O["type_rule"]["when_other"], f); key = "other_ai_statements" if oth else "statements"
    els = O["always"]["umbrella_elements"] + [b["element"] for b in O["blocks"] if match(b["when"], f)]
    ps = O["always"]["indirect_pointers"] + [b["pointer"] for b in O["conditional_pointers"] if match(b["when"], f)]
    n = sum(len(s["provision_ids"]) for e in els for s in e[key])
    n += sum(len(p["other_ai_provision_ids"] if oth else p["provision_ids"]) for p in ps)
    return n
CASES = [("public_chatbot", ["Generative AI that writes", "members of the public interact", "Yes, in something more official", "No, I only use the tool", "No, only publicly available", "No"],
          {"F_TYPE": "generative", "F_TASK": "chatbot_public", "F_PRODUCT": "official", "F_ROLE": "use_only", "F_DATA": "no", "F_DECISION": "no"}),
         ("other_ai_both", ["Other AI that predicts", "Both buying and building", "Yes"], {"F_TYPE": "other", "F_ROLE": "both", "F_DATA": "yes"})]
async def main():
    ok = True
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=_os.environ.get("CHROME_PATH", "/usr/bin/google-chrome"), args=["--no-sandbox"])
        for name, clicks, facts in CASES:
            pg = await b.new_page(viewport={"width": 1180, "height": 900}); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto("http://localhost:8765/index.html"); await pg.fill("#agency", "Test agency"); await pg.click("#start"); await pg.wait_for_selector(".opt")
            for c in clicks: await pg.locator(".opt", has_text=c).first.click(); await adv(pg)
            await pg.wait_for_selector(".closing")
            exp = expected(facts)
            for label in ["Must / Should / May", "Policy, standard or guideline", "Document"]:
                await pg.locator(".views button", has_text=label).click()
                n = await pg.locator(".row").count()
                heads = await pg.locator(".sec > h2").all_inner_texts()
                good = n == exp and not errs; ok &= good
                print(f"{name} | {label}: rows {n} expected {exp} | {'PASS' if good else 'FAIL'} | groups: {heads}")
                if name == "public_chatbot" and label == "Document": await pg.screenshot(path=_os.path.join(ROOT, "tests", "screenshots", "v3_by_doc.png"))
            await pg.locator(".views button", has_text="Topic").click()
            print(f"{name} | Topic: cards {await pg.locator('.el').count()} | errors {errs}")
            await pg.close()
        await b.close()
    sys.exit(0 if ok else 1)
asyncio.run(main())
