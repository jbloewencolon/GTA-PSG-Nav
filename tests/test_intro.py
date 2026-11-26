"""Title screen: proof-of-concept notice, agency (required) and email (optional), kept in this
browser only. Checks validation and focus, pre-filling, "Forget my details", Start over (back to the first question), that
nothing is sent off the page's own origin, and that the page still works when storage is blocked.
Needs the site served on localhost:8765.
"""
import asyncio, os, sys
from playwright.async_api import async_playwright

URL = "http://localhost:8765/index.html"
KEY = "gta-ai-policy-check:profile"
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"{name}: {'PASS' if ok else 'FAIL'} {detail}")


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get("CHROME_PATH", "/usr/bin/google-chrome"), args=["--no-sandbox"])
        ctx = await b.new_context(viewport={"width": 1280, "height": 900})
        pg = await ctx.new_page()
        errs, requests = [], []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("request", lambda r: requests.append((r.method, r.url)))
        await pg.goto(URL); await pg.wait_for_selector("#agency")

        check("shows title screen first", await pg.locator(".opt").count() == 0 and await pg.locator("#qh").inner_text() != "")
        check("proof-of-concept notice", "not an official GTA tool" in await pg.locator(".pocpill").inner_text())
        check("privacy promise", "never sent anywhere" in await pg.locator(".pocnote").inner_text())
        check("header pill", await pg.locator(".pocpill").is_visible())
        check("side panel hidden until questions start", not await pg.locator("aside.rail").is_visible())
        check("noindex", await pg.locator('meta[name="robots"]').get_attribute("content") == "noindex, nofollow")
        check("fields are labelled", await pg.get_by_label("Your agency").count() == 1 and await pg.get_by_label("Work email (optional)").count() == 1)

        await pg.click("#start")
        focus = await pg.evaluate("document.activeElement.id")
        check("empty agency blocked", await pg.locator(".opt").count() == 0 and await pg.locator("#agency-err").is_visible()
              and await pg.get_attribute("#agency", "aria-invalid") == "true" and focus == "agency", f"focus={focus}")

        await pg.fill("#agency", "  Department of Example  "); await pg.fill("#email", "not-an-email"); await pg.click("#start")
        focus = await pg.evaluate("document.activeElement.id")
        check("bad email blocked", await pg.locator(".opt").count() == 0 and await pg.locator("#email-err").is_visible()
              and await pg.get_attribute("#agency", "aria-invalid") == "false" and focus == "email", f"focus={focus}")

        await pg.fill("#email", ""); await pg.click("#start"); await pg.wait_for_selector(".opt")
        saved = await pg.evaluate(f"localStorage.getItem('{KEY}')")
        check("starts with agency only; trimmed and saved locally", saved == '{"agency":"Department of Example","email":""}', saved)
        check("agency shown in Your answers", "Department of Example" in await pg.locator("#answers").inner_text())
        check("side panel shown once started", await pg.locator("aside.rail").is_visible())

        await pg.reload(); await pg.wait_for_selector("#agency")
        check("pre-filled after reload", await pg.input_value("#agency") == "Department of Example")

        await pg.get_by_role("button", name="Forget my details").click()
        gone = await pg.evaluate(f"localStorage.getItem('{KEY}')")
        check("forget clears field and storage", gone is None and await pg.input_value("#agency") == "")

        await pg.fill("#agency", "Department of Example"); await pg.fill("#email", "person@example.gov"); await pg.click("#start")
        await pg.wait_for_selector(".opt"); await pg.locator(".opt").first.click()
        await pg.get_by_role("button", name="Start over").click()
        check("start over returns to the first question, agency kept", await pg.locator("#agency").count() == 0
              and await pg.inner_text("#qh") == "What kind of AI is it?" and "Department of Example" in await pg.locator("#answers").inner_text())
        await pg.get_by_role("button", name="Change your agency").click()
        check("changing the agency returns to the title screen, pre-filled", await pg.input_value("#email") == "person@example.gov")

        off = [u for _, u in requests if not u.startswith("http://localhost:8765/")]
        posts = [u for m, u in requests if m != "GET"]
        check("nothing sent off-origin, no POSTs", not off and not posts, f"off={off} posts={posts}")
        check("no page errors", not errs, str(errs))
        await ctx.close()

        # Storage blocked (private mode, site data disabled): the page must still work.
        ctx = await b.new_context()
        await ctx.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked')}})")
        pg = await ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL); await pg.wait_for_selector("#agency")
        await pg.fill("#agency", "Department of Example"); await pg.click("#start"); await pg.wait_for_selector(".opt")
        check("works with storage blocked", not errs, str(errs))
        await b.close()
    print("ALL PASS" if all(results) else "FAILED")
    sys.exit(0 if all(results) else 1)

asyncio.run(main())
