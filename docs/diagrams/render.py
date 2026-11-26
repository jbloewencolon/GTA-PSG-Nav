import asyncio,sys,glob,os
from playwright.async_api import async_playwright
SRC,OUT=sys.argv[1],sys.argv[2]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=os.environ.get("CHROME_PATH", "/usr/bin/google-chrome"),args=["--no-sandbox"])
        ctx=await b.new_context(viewport=dict(width=1600,height=900),device_scale_factor=2)
        for f in sorted(glob.glob(SRC+"/*.html")):
            pg=await ctx.new_page(); await pg.goto("file://"+f); await pg.wait_for_timeout(150)
            over=await pg.evaluate("document.documentElement.scrollHeight>900||document.documentElement.scrollWidth>1600")
            await pg.screenshot(path=os.path.join(OUT,os.path.basename(f)[:-5]+".png")); print(os.path.basename(f),"OVERFLOW" if over else "fits")
        await b.close()
asyncio.run(main())
