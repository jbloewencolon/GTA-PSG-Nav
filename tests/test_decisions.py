import os as _os; ROOT = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
import asyncio, json, sys
from playwright.async_api import async_playwright
O = json.load(open(_os.path.join(ROOT, "data", "stage3_triage.json"), encoding='utf-8'))["outcomes"]
D = json.load(open(_os.path.join(ROOT, "site", "data.json"), encoding='utf-8'))
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

DEC = [r for r in D if r.get("k") == "dec"]
STATUS = {"named": "The documents name who decides.", "documents_disagree": "The documents name different people for this.", "not_named": "The documents do not say who decides."}
def expect(f):
    ids = shown_ids(f); oth = match(O["type_rule"]["when_other"], f)
    ps = [p["id"] for p in O["always"]["indirect_pointers"]] + [b["pointer"]["id"] for b in O["conditional_pointers"] if match(b["when"], f)]
    sandbox = (not oth) and "P_SANDBOX" in ps
    out = {}
    for d in DEC:
        vr = d["roles"] if (d["force"] and sandbox) else [r for r in d["roles"] if r["pid"] in ids]
        if not vr: continue
        dec = []
        for r in vr:
            if r["part"] == "Decides" and r["role"] not in dec: dec.append(r["role"])
        st = ("documents_disagree" if d["status"] == "documents_disagree" and len(dec) > 1 else "named") if dec else "not_named"
        out[d["decision"]] = (STATUS[st], dec)
    return out
G = "Generative AI that writes"
CASES = [("build_legal", [G, "Legal or regulatory analysis", "No, it only helped", "Yes, building", "Yes", "No"], {"F_TYPE": "generative", "F_TASK": "legal", "F_PRODUCT": "none", "F_ROLE": "build", "F_DATA": "yes", "F_DECISION": "no"}),
 ("use_only", [G, "Summarizing or drafting internal", "No, it only helped", "No, I only use", "No, only publicly", "No"], {"F_TYPE": "generative", "F_TASK": "internal_summaries", "F_PRODUCT": "none", "F_ROLE": "use_only", "F_DATA": "no", "F_DECISION": "no"}),
 ("procure", [G, "Looking up or gathering", "No, it only helped", "Yes, buying", "No, only publicly", "No"], {"F_TYPE": "generative", "F_TASK": "research", "F_PRODUCT": "none", "F_ROLE": "procure", "F_DATA": "no", "F_DECISION": "no"}),
 ("meeting_host", [G, "Recording, transcribing", "No, it only helped", "No, I only use", "No, only publicly", "Yes, I am the host", "No"], {"F_TYPE": "generative", "F_TASK": "meetings", "F_PRODUCT": "none", "F_ROLE": "use_only", "F_DATA": "no", "F_HOST": "host", "F_DECISION": "no"}),
 ("other_build", ["Other AI that predicts", "Yes, building", "Yes"], {"F_TYPE": "other", "F_ROLE": "build", "F_DATA": "yes"}),
 ("notsure_all", [G, ".ns", ".ns", ".ns", ".ns", ".ns"], {"F_TYPE": "generative", "F_TASK": "not_sure", "F_PRODUCT": "not_sure", "F_ROLE": "not_sure", "F_DATA": "not_sure", "F_HOST": "not_sure"}),
 ("public_chatbot", [G, "members of the public interact", "Yes, in something more official", "No, I only use the tool", "No, only publicly available", "No"], {"F_TYPE": "generative", "F_TASK": "chatbot_public", "F_PRODUCT": "official", "F_ROLE": "use_only", "F_DATA": "no", "F_DECISION": "no"})]
async def main():
    ok = True
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=_os.environ.get("CHROME_PATH", "/usr/bin/google-chrome"), args=["--no-sandbox"])
        for name, clicks, facts in CASES:
            pg = await b.new_page(viewport={"width": 1180, "height": 900}); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto("http://localhost:8765/index.html#review"); await pg.wait_for_selector(".opt")
            for c in clicks:
                if c == ".ns": await pg.locator(".opt.ns").first.click()
                else: await pg.locator(".opt", has_text=c).first.click(); await adv(pg)
                if await pg.locator("text=Continue").count() and c == ".ns": await pg.locator("text=Continue").click()
            await pg.wait_for_selector(".closing")
            await pg.locator("#tab-steps").click()
            cards = pg.locator(".step.dec")
            n = await cards.count(); got = {}
            for i in range(n):
                c = cards.nth(i)
                t = await c.locator("h3").inner_text(); st = await c.locator(".where b").first.inner_text()
                roles = await c.locator(".roles li").all_inner_texts()
                got[t] = (st, [r.split("“")[1].split("”")[0] for r in roles if r.startswith("Decides")])
            exp = expect(facts)
            lines = await pg.locator(".step:not(.dec) .where b", has_text="Who decides:").count()
            ids = shown_ids(facts); expl = sum(1 for s in STEPS if s["pid"] in ids and s.get("dec") and any(d["id"] == s["dec"] and d["decision"] in exp for d in DEC))
            sc = await pg.locator(".step:not(.dec)").count(); es = sum(1 for s in STEPS if s["pid"] in ids)
            good = got == exp and lines == expl and sc == es and not errs; ok &= good
            print(f"{name}: decisions {n} expected {len(exp)} | who-decides lines {lines}/{expl} | steps {sc}/{es} | {'PASS' if good else 'FAIL'} {errs}")
            if got != exp:
                for k in set(got) | set(exp):
                    if got.get(k) != exp.get(k): print("   DIFF", k, got.get(k), exp.get(k))
            await pg.screenshot(path=f"{ROOT}/tests/screenshots/v5_{name}.png", full_page=True)
            await pg.close()
        await b.close()
    sys.exit(0 if ok else 1)
asyncio.run(main())
