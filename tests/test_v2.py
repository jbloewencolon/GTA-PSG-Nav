import os as _os; ROOT = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
import asyncio, json, sys
from playwright.async_api import async_playwright

TRI = json.load(open(_os.path.join(ROOT, "data", "stage3_triage.json"), encoding='utf-8'))
O = TRI["outcomes"]



async def adv(pg):
    """Question 2 allows several answers, so it waits for Continue."""
    if await pg.locator('.opts.multi .opt[aria-pressed="true"]').count():
        await pg.get_by_role("button", name="Continue", exact=True).click()

def match(c, f):
    return c == "always" or any(all(f.get(k) in v for k, v in a.items()) for a in c)


def expected(f):
    """Card count the tree says the page should show: notes + conditional + pointers + umbrella."""
    if match(O["scope_gate"]["when"], f):
        return 0
    oth = match(O["type_rule"]["when_other"], f)
    key = "other_ai_statements" if oth else "statements"
    umb = [e for e in O["always"]["umbrella_elements"] if e[key]]
    con = [b["element"] for b in O["blocks"] if match(b["when"], f) and b["element"][key]]
    ps = O["always"]["indirect_pointers"] + [b["pointer"] for b in O["conditional_pointers"] if match(b["when"], f)]
    ps = [p for p in ps if (p["other_ai_as_written"] if oth else p["as_written"])]
    notes = [n for n in O["type_notes"] if match(n["when"], f)]
    return len(umb) + len(con) + len(ps) + len(notes)


CASES = [
    ("no_ai", ["It does not use AI"], {"F_TYPE": "none"}),
    ("other_ai", ["Other AI that predicts", "No, I only use the tool", "Yes"],
     {"F_TYPE": "other", "F_ROLE": "use_only", "F_DATA": "yes"}),
    ("public_chatbot", ["Generative AI that writes", "members of the public interact", "Yes, in something more official",
                        "No, I only use the tool", "No, only publicly available", "No"],
     {"F_TYPE": "generative", "F_TASK": "chatbot_public", "F_PRODUCT": "official", "F_ROLE": "use_only", "F_DATA": "no", "F_DECISION": "no"}),
    ("agent_as_other", ["Other AI that predicts", "No, I only use the tool", "No, only publicly available"], {"F_TYPE": "other", "F_ROLE": "use_only", "F_DATA": "no"}),
    ("internal_chatbot", ["Generative AI that writes", "used only by state staff", "No, it only helped",
                                  "No, I only use the tool", "No, only publicly available", "No"],
     {"F_TYPE": "generative", "F_TASK": "chatbot_internal", "F_PRODUCT": "none", "F_ROLE": "use_only", "F_DATA": "no", "F_DECISION": "no"}),
]


async def main():
    ok = True
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=_os.environ.get("CHROME_PATH", "/usr/bin/google-chrome"), args=["--no-sandbox"])
        for name, clicks, facts in CASES:
            pg = await b.new_page(viewport={"width": 1180, "height": 900})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto("http://localhost:8765/index.html")
            await pg.fill("#agency", "Test agency"); await pg.click("#start"); await pg.wait_for_selector(".opt")
            for c in clicks:
                await pg.locator(".opt", has_text=c).first.click(); await adv(pg)
            await pg.wait_for_selector(".closing")
            n = await pg.locator(".el").count()
            body = await pg.inner_text("#main")
            exp = expected(facts)
            has_pub = "Deploy public chatbots with GenAI only after bias/safety review" in await pg.content()
            good = n == exp and not errs
            ok &= good
            print(f"{name}: cards {n} expected {exp} | level {await pg.inner_text('#level')} | public-chatbot rule present {has_pub} | errors {errs} | {'PASS' if good else 'FAIL'}")
            if name == "no_ai":
                print("   ", body[:160].replace("\n", " "))
            await pg.screenshot(path=f"{ROOT}/tests/screenshots/v2_{name}.png", full_page=False)
            await pg.close()
        await b.close()
    sys.exit(0 if ok else 1)


asyncio.run(main())
