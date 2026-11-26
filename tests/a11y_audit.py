import os as _os; ROOT = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
import asyncio, json, sys
from playwright.async_api import async_playwright
URL = "http://localhost:8765/index.html"
JS = r"""
() => {
 function rgb(s){const m=s.match(/[\d.]+/g);return m?m.map(Number):null}
 function lum(c){const a=c.slice(0,3).map(v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)});return 0.2126*a[0]+0.7152*a[1]+0.0722*a[2]}
 function ratio(a,b){const x=lum(a),y=lum(b);return (Math.max(x,y)+0.05)/(Math.min(x,y)+0.05)}
 function bg(el){while(el){const c=rgb(getComputedStyle(el).backgroundColor);if(c&&(c.length<4||c[3]>0.5))return c;el=el.parentElement}return [255,255,255]}
 function vis(el){const r=el.getBoundingClientRect();const s=getComputedStyle(el);return r.width>0&&r.height>0&&s.visibility!=="hidden"&&s.display!=="none"}
 const out={contrast:[],targets:[],headings:[],landmarks:[],live:[],names:[],tabs:null,reflow:null};
 const seen=new Set();
 document.querySelectorAll("body *").forEach(el=>{
  if(!vis(el))return;
  const own=[...el.childNodes].some(n=>n.nodeType===3&&n.textContent.trim());
  if(!own)return;
  const s=getComputedStyle(el);const fg=rgb(s.color),b=bg(el);const r=ratio(fg,b);
  const size=parseFloat(s.fontSize),bold=parseInt(s.fontWeight)>=700;const large=size>=24||(bold&&size>=18.66);
  const need=large?3:4.5;
  const key=el.className+"|"+s.color+"|"+b;
  if(r<need&&!seen.has(key)){seen.add(key);out.contrast.push({el:el.tagName.toLowerCase()+"."+(el.className||""),text:el.textContent.trim().slice(0,40),fg:s.color,bg:"rgb("+b.slice(0,3)+")",ratio:+r.toFixed(2),need})}
 });
 // non-text contrast: option borders, view buttons, tube, ticks
 [[".opt","borderTopColor"],[".views button","borderTopColor"],[".thermo .tube","borderTopColor"],[".thermo .tick","backgroundColor"],[".progress i","backgroundColor"],[".tabs","borderBottomColor"]].forEach(([q,p])=>{
  const el=document.querySelector(q);if(!el)return;const c=rgb(getComputedStyle(el)[p]);const b=bg(el.parentElement);out.names.push({nontext:q,ratio:+ratio(c,b).toFixed(2)})});
 document.querySelectorAll("button,a,summary,[tabindex='0']").forEach(el=>{if(!vis(el))return;const r=el.getBoundingClientRect();if(r.height<44||r.width<44)out.targets.push({el:el.tagName.toLowerCase()+"."+el.className,text:(el.textContent||"").trim().slice(0,30),w:Math.round(r.width),h:Math.round(r.height)})});
 document.querySelectorAll("h1,h2,h3,h4").forEach(h=>{if(vis(h))out.headings.push(h.tagName+": "+h.textContent.trim().slice(0,50))});
 document.querySelectorAll("header,main,aside,nav,footer,[role]").forEach(e=>out.landmarks.push(e.tagName.toLowerCase()+(e.getAttribute("role")?"[role="+e.getAttribute("role")+"]":"")));
 document.querySelectorAll("[aria-live]").forEach(e=>out.live.push(e.id+"|"+e.className+": "+e.getAttribute("aria-live")+", text length "+e.textContent.length));
 const t=document.querySelector("[role=tablist]");if(t){out.tabs={controls:[...t.querySelectorAll("[role=tab]")].map(b=>b.getAttribute("aria-controls")),panelExists:!!document.getElementById("tabpanel"),tabindex:[...t.querySelectorAll("[role=tab]")].map(b=>b.getAttribute("tabindex"))}}
 out.reflow=document.documentElement.scrollWidth>window.innerWidth+1?("horizontal scroll: "+document.documentElement.scrollWidth+" > "+window.innerWidth):"ok";
 document.querySelectorAll("a[target=_blank]").forEach(a=>{if(!/new tab|new window/i.test(a.textContent+(a.getAttribute("aria-label")||"")))out.newtab=(out.newtab||0)+1});
 return out;
}"""

async def adv(pg):
    """Question 2 allows several answers, so it waits for Continue."""
    if await pg.locator('.opts.multi .opt[aria-pressed="true"]').count():
        await pg.get_by_role("button", name="Continue", exact=True).click()

async def walk(pg, clicks):
    await pg.goto(URL); await pg.wait_for_selector(".opt")
    for c in clicks:
        await pg.locator(".opt", has_text=c).first.click(); await adv(pg)
    await pg.wait_for_timeout(700)
async def main():
    G="Generative AI that writes"
    route=[G,"Legal or regulatory analysis","No, it only helped","Yes, building","Yes","Yes"]
    res={}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=_os.environ.get("CHROME_PATH", "/usr/bin/google-chrome"), args=["--no-sandbox"])
        for scheme in ["light","dark"]:
            for name,vp in [("desktop",(1280,900)),("reflow320",(320,700)),("zoom200",(640,450))]:
                pg = await b.new_page(viewport={"width":vp[0],"height":vp[1]}, color_scheme=scheme, reduced_motion="reduce")
                await walk(pg, [])
                res[f"{scheme}/{name}/question"] = await pg.evaluate(JS)
                await walk(pg, route)
                res[f"{scheme}/{name}/results"] = await pg.evaluate(JS)
                await pg.locator("#tab-steps").click(); await pg.wait_for_timeout(300)
                res[f"{scheme}/{name}/steps"] = await pg.evaluate(JS)
                await pg.close()
        # keyboard walk
        pg = await b.new_page(viewport={"width":1280,"height":900}); await walk(pg, [])
        seq=[]
        for i in range(14):
            await pg.keyboard.press("Tab")
            seq.append(await pg.evaluate("()=>{const e=document.activeElement;const s=getComputedStyle(e);return e.tagName+'.'+e.className+' |'+(e.textContent||'').trim().slice(0,25)+'| outline '+s.outlineStyle+' '+s.outlineWidth}"))
        res["keyboard_question"]=seq
        await pg.keyboard.press("Enter"); await pg.wait_for_timeout(200)
        res["after_enter_focus"]=await pg.evaluate("()=>document.activeElement.id+'|'+document.activeElement.tagName")
        # tabs keyboard
        await walk(pg, ["Generative AI that writes","Legal or regulatory analysis","No, it only helped","Yes, building","Yes","Yes"])
        await pg.locator("#tab-applies").focus(); await pg.keyboard.press("ArrowRight"); await pg.wait_for_timeout(200)
        res["tabs_arrow"]=await pg.evaluate("()=>document.activeElement.id+'|selected '+document.activeElement.getAttribute('aria-selected')+'|panel '+(document.getElementById('tabpanel')||{}).getAttribute?.('aria-labelledby')")
        res["updated"]=await pg.inner_text("#updated")
        await b.close()
    json.dump(res, open(sys.argv[1],"w", encoding='utf-8'), indent=1)
asyncio.run(main())
