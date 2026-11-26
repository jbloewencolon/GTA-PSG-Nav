import asyncio,sys,os
from playwright.async_api import async_playwright
OUT=sys.argv[1]; URL="http://localhost:8765/"
G="Generative AI that writes"
async def answer(pg,clicks):
    for c in clicks:
        if isinstance(c,list):
            for t in c: await pg.locator(".opts.multi .opt",has_text=t).first.click()
            await pg.get_by_role("button",name="Continue",exact=True).click()
        else: await pg.locator(".opt",has_text=c).first.click()
        await pg.wait_for_timeout(120)
    await pg.wait_for_timeout(700)
async def shot(pg,name): await pg.screenshot(path=f"{OUT}/{name}.png"); print(name)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=os.environ.get("CHROME_PATH", "/usr/bin/google-chrome"),args=["--no-sandbox"])
        async def page(scheme="light",**kw):
            ctx=await b.new_context(viewport=dict(width=1600,height=900),device_scale_factor=2,color_scheme=scheme,reduced_motion="reduce",**kw)
            pg=await ctx.new_page(); await pg.goto(URL); await pg.wait_for_selector("#agency")
            await pg.fill("#agency","Department of Example"); await pg.click("#start"); await pg.wait_for_selector(".opt"); return pg
        # 0 title screen
        ctx=await b.new_context(viewport=dict(width=1600,height=900),device_scale_factor=2,reduced_motion="reduce")
        pg=await ctx.new_page(); await pg.goto(URL); await pg.wait_for_selector("#agency")
        await pg.fill("#agency","Department of Example"); await pg.fill("#email","name@example.ga.gov"); await pg.evaluate("document.activeElement.blur()"); await shot(pg,"00-title-screen")
        # 1 question flow: multi-select task, guardrails already rising
        pg=await page(); await pg.locator(".opt",has_text=G).first.click()
        for t in ["Writing for the public","Legal or regulatory"]: await pg.locator(".opts.multi .opt",has_text=t).first.click()
        await pg.wait_for_timeout(700); await shot(pg,"01-question")
        # 2 results with guardrail reasons
        pg=await page(); await answer(pg,[G,["Writing for the public"],"Yes, in something more official","Yes, building","No, only publicly","No"]); await shot(pg,"02-results-guardrails")
        # 3 red stop
        pg=await page(); await answer(pg,[G,["Analyzing data"],"No, it only helped","No, I only use","Yes","Yes"]); await shot(pg,"03-stop-sign")
        # 4 amber check first
        pg=await page(); await answer(pg,["Other AI that predicts","Yes, buying","Yes"]); await shot(pg,"04-check-first")
        # 5 exact wording, opened
        pg=await page(); await answer(pg,[G,["Legal or regulatory"],"No, it only helped","No, I only use","No, only publicly","No"])
        d=pg.locator(".sec .el details:not(.flags) > summary",has_text="Exact wording").first
        await d.click(); await pg.wait_for_timeout(300)
        await pg.evaluate("e=>{const r=e.closest('.el').getBoundingClientRect();window.scrollBy(0,r.top-24)}",await d.element_handle())
        await pg.wait_for_timeout(300); await shot(pg,"05-exact-wording")
        # 6 grouped by Must / Should / May
        pg=await page(); await answer(pg,[G,["members of the public interact"],"Yes, in something more official","No, I only use","No, only publicly","No"])
        await pg.get_by_role("button",name="Must / Should / May").click(); await pg.wait_for_timeout(300)
        await pg.locator(".views").scroll_into_view_if_needed(); await pg.evaluate("window.scrollBy(0,-16)"); await shot(pg,"06-grouped-by-obligation")
        # 7 next steps
        pg=await page(); await answer(pg,[G,["Writing for the public"],"Yes, in something more official","Yes, buying","No, only publicly","No"])
        await pg.get_by_role("tab",name="Next steps").click(); await pg.wait_for_timeout(400)
        await pg.evaluate("window.scrollTo(0, document.getElementById('tabpanel').getBoundingClientRect().top + scrollY - 24)"); await pg.wait_for_timeout(300); await shot(pg,"07-next-steps")
        # 8 dark mode
        pg=await page("dark"); await answer(pg,[G,["Writing for the public"],"Yes, in something more official","Yes, building","No, only publicly","No"]); await shot(pg,"08-dark-mode")
        # 9 phone
        dev=p.devices["iPhone 13"]
        ctx=await b.new_context(**dev,reduced_motion="reduce"); pg=await ctx.new_page(); await pg.goto(URL); await pg.wait_for_selector("#agency")
        await pg.fill("#agency","Department of Example"); await pg.click("#start"); await pg.wait_for_selector(".opt")
        await answer(pg,[G,["Analyzing data"],"No, it only helped","No, I only use","Yes","Yes"])
        await pg.evaluate("window.scrollTo(0, document.querySelector('.q h2').getBoundingClientRect().top + scrollY - 16)"); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f"{OUT}/09-phone.png"); print("09-phone")
        await b.close()
asyncio.run(main())
