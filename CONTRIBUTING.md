# Contributing

## Set up

1. Clone the repository and change into it.
2. The pipeline in `scripts/` uses only the Python standard library (Python 3.11 or later), so it needs no install.
3. For the browser tests, create a virtual environment and install Playwright:

   ```bash
   python3 -m venv .venv
   . .venv/bin/activate
   python3 -m pip install -r requirements-dev.txt
   ```

   The tests launch Chrome or Chromium from `/usr/bin/google-chrome`. Set `CHROME_PATH` to use another executable.

## Rebuild and test

1. Rebuild the data with the five commands under "Rebuild the data" in the README, in order.
2. Run `git diff --stat`. If you did not change `data/stage1_inventory.json` or a script, nothing under `data/` or `site/` should change.
3. Serve the page and run the tests from the repository root:

   ```bash
   python3 -m http.server 8765 --directory site &
   python3 tests/test_decisions.py
   python3 tests/test_employee.py
   python3 tests/test_multi.py
   python3 tests/test_score.py
   python3 tests/test_steps.py
   python3 tests/test_v2.py
   python3 tests/test_views.py
   python3 tests/a11y_audit.py report.json
   ```

   Each test script prints one line per route and exits with status 1 if any line says `FAIL`. `test_multi.py` also prints a summary line for the data check.

## Changing policy content

The page is meant to be used for compliance, so content changes follow these rules:
- **Citations:** every provision cites its document title, identifier (if it has one), and section or page.
- **Modal verbs:** keep them exactly as written (must, shall, should, may). Don't make a requirement stronger or weaker.
- **Outside references:** if a document refers to something not in the source set, record it as an unresolved reference. Don't describe it.
- **Insufficient evidence:** where the evidence doesn't settle a question, add an open question rather than choosing an answer.

## Changing the guardrails or the signs

The rules live in `scripts/gen_site.py` (`FACTORS` and `SIGNS`) and reach the page as `factor` and `sign` records in `site/data.json`:
- **Factors:** each adds posts once, from what the user described, not from how many provisions match. Each variant names the answers that set it off, the reason shown, and the provision it quotes on the generative and the other-AI branch (`None` if it does not apply there). Count a Not sure answer as yes.
- **Levels:** the cut-offs (1, 3 and 5 posts; the bar's top is 8) appear in `levelOf()` and `PMAX` in `site/index.html`, in the tick marks and band colours of the bar, in the "How this count works" note, and in `tests/test_score.py`.
- **Red stop:** add one only where a provision says GTA approval is required or the use is prohibited, and cite it by ID. If another document disagrees, say so in the title and the note.
- **Amber Check first:** add one only where a provision requires a review or an authorization before the use, and cite it by ID.

After a change, update `expected()` in `tests/test_score.py` to match, and run it. It checks every route, and fails if a factor or sign quotes a provision the page does not show on that route.

## Pull requests

1. Create a branch from the default branch.
2. Make focused commits with imperative messages (for example, "Fix citation for SS-25-001 1.3").
3. Rebuild the data and run all tests before opening the pull request.
4. In the description, say what changed, which commands you ran and their results, and which provisions or questions are affected.
