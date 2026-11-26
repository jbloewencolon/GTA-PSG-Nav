import os as _os; ROOT = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
"""Question 2 (F_TASK) takes several answers. Checks that a multi-answer result is
exactly the union of the single-answer results for each chosen task.

Part 1 (data): mirrors the page's rules in Python and checks every route with one or
two tasks chosen, plus a random sample of larger sets, for elements, pointers,
provisions and next steps.
Part 2 (page): drives the real page for a few combinations and compares what it shows
with the Part 1 expectation. Needs the site served on localhost:8765.
"""
import asyncio, itertools, json, random, sys
from playwright.async_api import async_playwright

D = json.load(open(sys.argv[1] if len(sys.argv) > 1 else _os.path.join(ROOT, "site", "data.json"), encoding='utf-8'))
META = [r for r in D if r["k"] == "meta"][0]
Q = [r for r in D if r["k"] == "q"]
EL = [r for r in D if r["k"] == "el"]
PT = [r for r in D if r["k"] == "ptr"]
STEPS = [r for r in D if r["k"] == "step"]
QF = {q["fact"]: q for q in Q}


def has(lst, v):
    return any(x in lst for x in v) if isinstance(v, list) else v in lst


def match(c, f):
    return c == "always" or any(all(has(a[k], f.get(k)) for k in a) for a in c)


def asked(q, f):
    return q["ask_if"] == "always" or match([q["ask_if"]], f)


def prune(f):
    f = dict(f)
    changed = True
    while changed:
        changed = False
        for q in Q:
            if q["fact"] in f and not asked(q, f):
                del f[q["fact"]]; changed = True
    return f


def shown(f):
    """Topic cards, pointer cards, provisions and steps the page shows for facts f."""
    if match(META["gate"]["when"], f):
        return dict(el=set(), pt=set(), prov=set(), steps=set())
    oth = match(META["when_other"], f)
    sts = lambda e: e["other"] if oth else e["statements"]
    els = [e for e in EL if sts(e) and (e["tier"] == "umbrella" or match(e["when"], f))]
    pts = [p for p in PT if match(p["when"], f) and (not oth or p["o_as_written"])]
    prov = {p["id"] for e in els for s in sts(e) for p in s["prov"]} | {p["id"] for q in pts for p in (q["oprov"] if oth else q["prov"])}
    return dict(el={e["id"] for e in els}, pt={p["id"] for p in pts}, prov=prov, steps={s["pid"] for s in STEPS if s["pid"] in prov})


def union_of_singles(f):
    tasks = f["F_TASK"]
    out = dict(el=set(), pt=set(), prov=set(), steps=set())
    for t in tasks:
        r = shown(prune(dict(f, F_TASK=t)))
        for k in out: out[k] |= r[k]
    return out


TASKS = [o["value"] for o in QF["F_TASK"]["options"] if not o["not_sure"]]
OTHER_Q = [q for q in Q if q["fact"] not in ("F_TYPE", "F_TASK")]


def routes(task_sets):
    seen = set()
    for ty in ("generative", "not_sure"):
        for ts in task_sets:
            for vals in itertools.product(*[[o["value"] for o in q["options"]] for q in OTHER_Q]):
                f = prune(dict({"F_TYPE": ty, "F_TASK": list(ts)}, **{q["fact"]: v for q, v in zip(OTHER_Q, vals)}))
                key = json.dumps(f, sort_keys=True)
                if key not in seen:
                    seen.add(key); yield f


def part1():
    small = [(t,) for t in TASKS] + list(itertools.combinations(TASKS, 2))
    rnd = random.Random(7)
    big = {tuple(sorted(rnd.sample(TASKS, rnd.randint(3, len(TASKS))), key=TASKS.index)) for _ in range(120)}
    big.add(tuple(TASKS))
    n = bad = 0
    for f in itertools.chain(routes(small), routes(sorted(big))):
        n += 1
        a, b = shown(f), union_of_singles(f)
        if a != b:
            bad += 1
            if bad <= 5:
                print("MISMATCH", f, {k: sorted(a[k] ^ b[k]) for k in a if a[k] != b[k]})
    print(f"part 1: {n} multi-answer routes checked against the union of single-answer routes, {bad} mismatches")
    return bad == 0


CASES = [
    # (name, F_TYPE click, task clicks, later clicks, facts)
    ("research+public", "Generative AI that writes", ["Looking up", "Writing for the public"],
     ["Yes, in something more official", "No, I only use the tool", "No, only publicly available", "No"],
     {"F_TYPE": "generative", "F_TASK": ["research", "public_comms"], "F_PRODUCT": "official", "F_ROLE": "use_only", "F_DATA": "no", "F_DECISION": "no"}),
    ("policy+meetings", "Generative AI that writes", ["Drafting policy language", "Recording, transcribing"],
     ["No, it only helped", "No, I only use the tool", "No, only publicly available", "Yes, I am the host", "No"],
     {"F_TYPE": "generative", "F_TASK": ["policy_drafting", "meetings"], "F_PRODUCT": "none", "F_ROLE": "use_only", "F_DATA": "no", "F_HOST": "host", "F_DECISION": "no"}),
    ("chatbot both+media+legal", "Generative AI that writes", ["members of the public interact", "used only by state staff", "Generating images", "Legal or regulatory"],
     ["Yes, in something more official", "No, I only use the tool", "No, only publicly available", "Yes"],
     {"F_TYPE": "generative", "F_TASK": ["chatbot_public", "chatbot_internal", "media", "legal"], "F_PRODUCT": "official", "F_ROLE": "use_only", "F_DATA": "no", "F_DECISION": "yes"}),
    ("not sure clears others", "Generative AI that writes", ["Looking up", "Writing, reviewing", ".ns"],
     ["No, it only helped", "No, I only use the tool", "No, only publicly available", "No"],
     {"F_TYPE": "generative", "F_TASK": ["not_sure"], "F_PRODUCT": "none", "F_ROLE": "use_only", "F_DATA": "no", "F_DECISION": "no"}),
    ("deselect leaves one", "Generative AI that writes", ["Looking up", "Writing, reviewing", "Looking up"],
     ["No, it only helped", "No, I only use the tool", "No, only publicly available", "No"],
     {"F_TYPE": "generative", "F_TASK": ["coding"], "F_PRODUCT": "none", "F_ROLE": "use_only", "F_DATA": "no", "F_DECISION": "no"}),
]


async def part2():
    ok = True
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=_os.environ.get("CHROME_PATH", "/usr/bin/google-chrome"), args=["--no-sandbox"])
        for name, ty, tasks, later, facts in CASES:
            pg = await b.new_page(viewport={"width": 1180, "height": 900})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto("http://localhost:8765/index.html"); await pg.wait_for_selector(".opt")
            await pg.locator(".opt", has_text=ty).first.click()
            hint = await pg.locator("#qhint").inner_text()
            help_ok = "Pick the closest" not in await pg.inner_text("#main")
            for t in tasks:
                await (pg.locator(".opts.multi .opt.ns") if t == ".ns" else pg.locator(".opts.multi .opt", has_text=t)).first.click()
                still = await pg.locator(".opts.multi").count()
                ok &= bool(still)
            pressed = await pg.locator('.opts.multi .opt[aria-pressed="true"]').count()
            focus_ok = await pg.evaluate("document.activeElement && document.activeElement.classList.contains('opt')")
            await pg.get_by_role("button", name="Continue", exact=True).click()
            for c in later:
                await pg.locator(".opt", has_text=c).first.click()
            await pg.wait_for_selector(".closing")
            titles = set(await pg.locator("#main article.el:not(.ptr) h3").all_inner_texts())
            ptrs = set(await pg.locator("#main article.el.ptr p.do").all_inner_texts())
            rail = await pg.inner_text("#answers")
            await pg.locator("#tab-steps").click()
            steps = set(await pg.locator("#main article h3").all_text_contents())
            exp = union_of_singles(prune(facts)) if facts["F_TASK"] != ["not_sure"] else shown(prune(facts))
            exp_titles = {e["title"] for e in EL if e["id"] in exp["el"]}
            exp_ptrs = {q["pointer"] for q in PT if q["id"] in exp["pt"]}
            exp_steps = {s["title"] for s in STEPS if s["pid"] in exp["steps"]}
            good = (titles == exp_titles and ptrs == exp_ptrs and exp_steps <= steps and pressed == len(facts["F_TASK"])
                    and hint == "Select all that apply." and help_ok and focus_ok and not errs)
            ok &= good
            print(f"{name}: topics {len(titles)}/{len(exp_titles)} pointers {len(ptrs)}/{len(exp_ptrs)} steps {len(exp_steps & steps)}/{len(exp_steps)} "
                  f"pressed {pressed} focus kept {focus_ok} | rail: {[l for l in rail.splitlines() if l and l != "Change"][3]!r} | {'PASS' if good else 'FAIL'} {errs}")
            if titles != exp_titles: print("  topics diff", titles ^ exp_titles)
            await pg.close()
        await b.close()
    return ok


if __name__ == "__main__":
    r1 = part1()
    r2 = asyncio.run(part2())
    print("ALL PASS" if r1 and r2 else "FAILURES")
    sys.exit(0 if r1 and r2 else 1)
