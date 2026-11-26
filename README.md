```
   ____ _____  _        _    ___
  / ___|_   _|/ \      / \  |_ _|
 | |  _  | | / _ \    / _ \  | |
 | |_| | | |/ ___ \  / ___ \ | |
  \____| |_/_/   \_\/_/   \_\___|
     p o l i c y   n a v i g a t o r
```

# gta-ai-policy-navigator

Answer a few questions and see which Georgia Technology Authority (GTA) AI policies, standards and guidelines apply, with their exact source wording.

## Features

**The navigator page** (`site/`) is a single static HTML page that reads `site/data.json` in the browser. It needs no server-side code.
- **Questions:** up to seven plain-language questions, starting with what kind of AI is used. Every question has a "Not sure" answer. A "Your answers" panel lets you change any answer.
- **Several tasks at once:** the second question (what the tool is used for) accepts several answers. The results are everything any chosen task triggers on its own, and follow-up questions appear if any chosen task needs them. Choosing "Not sure" clears the other choices.
- **Results:** only the provisions that apply, shown by topic or grouped by modal verb (must, must not, should, may), by document type (policy, standard, guideline) or by document.
- **Exact wording:** each line opens to the quoted source text with the document title, identifier, section, page and the modal verb as written. The page also flags where the documents disagree or leave something open. In the grouped views, the citation sits in a collapsed "Source" line under each quote.
- **Next steps tab:**
  - steps the documents name, with any contact given in the source and a "Decides" line naming who makes the call;
  - decisions with no step card, as one-line rows;
  - items written for agencies, in one closed "For your agency" panel.
- **Review details switch:** at the bottom of Next steps (or open the page with `#review`). It restores the full view for policy staff: the modal verb as written, analyst notes, unresolved references and the panels on where the documents disagree.
- **Guardrails:** a road picture whose guardrail posts rise as your answers trigger more rules (No extra, Light 1-9, Standard 10-25, Extra 26-49, Full 50 or more). Each rule counts once. Rules for the chosen tasks count 1 point (2 for a prohibition), other rules 2 (4), and rules on personal or sensitive information and on decisions about people 4 (8). The weights are this tool's, not GTA's.
- **Stop sign:** replaces the guardrails, with the source wording at the top of the results, when the documents require GTA approval for what you described (personal or regulated data, SS-25-001 1.3; buying a GenAI product or service, SS-25-001 1.5) or list it as prohibited (decisions about people, SS-25-001 3.0 table). A Not sure answer to those questions also shows it.
- **Explanations on request:** each question's help text, the note on how the count works and the longer result notes are collapsed under links such as "About this question".
- **Display:** light and dark themes, reduced-motion support, and a print style sheet that expands every source quotation.

**The build pipeline** (`scripts/`) uses only the Python standard library.
- `partA.py` builds the applicability map (`data/stage2_map.json`) from the provision inventory.
- `partB.py` builds the question tree (`data/stage3_triage.json`). It checks every answer path against the map and reports mismatches, redundant questions and bad skips.
- `render_md.py` renders the tree as Markdown (`data/stage3_triage.md`).
- `decision_rights.py` lists who decides what (`data/decision_rights.json`, `data/decision_rights.md`).
- `gen_site.py` assembles `site/data.json`. It checks that each step's quoted contact and link appear in the source text.

**Browser tests** (`tests/`) click through routes with Playwright. They check results, groupings, next steps, decisions, multi-task answers, the guardrail count and the stop sign against the data files, and run an automated accessibility check.

## Requirements

- **Pipeline:** Python 3.11 or later. It was run on 3.11, 3.12 and 3.13 and not tested on earlier versions. It has no third-party packages.
- **Navigator page:** a modern web browser. To open it locally, use any static file server; the commands below use Python's built-in one. The page loads its fonts from `fonts.googleapis.com` and falls back to system fonts when that is unreachable.
- **Tests only:**
  - Playwright for Python (`requirements-dev.txt`; run with Playwright 1.63.0).
  - A Chrome or Chromium executable. The tests use `/usr/bin/google-chrome` unless `CHROME_PATH` is set.
  - The navigator page served at `http://localhost:8765`.

## Installation

```bash
git clone <repository-url>
cd gta-ai-policy-navigator
```

The pipeline and the page need nothing else. To run the tests, install the development dependency in a virtual environment:

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
```

## Usage

### Open the navigator

```bash
python3 -m http.server 8765 --directory site
```

Expected output (the server keeps running until you press Ctrl+C):

```
Serving HTTP on 0.0.0.0 port 8765 (http://0.0.0.0:8765/) ...
```

Then open <http://localhost:8765/> in a browser.

### Rebuild the data from the provision inventory

`data/stage1_inventory.json` is the input to the pipeline. Run the steps in order from the repository root. With the committed inventory, each step reproduces the committed output files byte for byte.

```bash
python3 scripts/partA.py data/stage1_inventory.json data/stage2_map.json
```
Last line of output: `pointers 12 conflicts 13 unres 31 oq 30`

```bash
python3 scripts/partB.py data/stage2_map.json data/stage3_triage.json 8
```
The last argument is the maximum number of questions allowed on the longest path. The command prints a JSON report (`"number_of_paths": 6016`, `"longest_path_questions": 7`, `"within_limit": true`, among others) and ends with `mism 0 redundant 0 bad_skips 0`. It takes a few seconds.

```bash
python3 scripts/render_md.py data/stage3_triage.json data/stage3_triage.md
```
Output: `1517 lines`

```bash
python3 scripts/decision_rights.py data/stage1_inventory.json data/stage2_map.json data/decision_rights.json data/decision_rights.md
```
First line of output: `{"decisions": 19, "documents_disagree": 2, "named": 12, "not_named": 5, "employee_level": 9, "agency_level": 10, "not_reached_by_any_question": 4}`

```bash
NAV_UPDATED=2026-11-25 python3 scripts/gen_site.py data/stage1_inventory.json data/stage2_map.json data/stage3_triage.json site data/decision_rights.json
```
Output: `93 records 298209 bytes`

`NAV_UPDATED` sets the "Last updated" date shown on the page. Without it, the script uses today's date, and the byte count changes with the length of the date.

### Run the tests

With the server from "Open the navigator" running in another terminal:

```bash
python3 tests/test_decisions.py
```

Expected output: seven lines ending in `PASS`, for example:

```
build_legal: decisions 12 expected 12 | who-decides lines 6/6 | steps 9/9 | PASS []
```

The other test scripts work the same way. Each exits with status 1 if any check fails.
- `tests/test_employee.py`: 7 routes. Checks the employee view of Next steps, and that review-only items stay hidden.
- `tests/test_score.py`: 9 routes. Checks the guardrail count, level and stop sign on the page against an independent calculation.
- `tests/test_steps.py`: 3 routes.
- `tests/test_v2.py`: 5 routes.
- `tests/test_views.py`: 6 checks.
- `tests/test_multi.py`: checks that a result with several tasks chosen is exactly the union of the single-task results. It covers 125,280 answer combinations in the data, then clicks 5 routes in the page, and ends with `ALL PASS`.

`tests/test_decisions.py` opens the page in Review mode (`#review`).

`python3 tests/a11y_audit.py report.json` writes accessibility findings (contrast, target sizes, headings, live regions, reflow) to `report.json`, with no console output. Screenshots from the tests go to `tests/screenshots/`.

## Project structure

```
gta-ai-policy-navigator/
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── requirements-dev.txt
├── data/
│   ├── stage1_inventory.json     provision inventory (pipeline input)
│   ├── stage2_map.json           applicability map
│   ├── stage3_triage.json        question tree and outcomes
│   ├── stage3_triage.md          tree rendered as Markdown
│   ├── decision_rights.json      who decides what
│   ├── decision_rights.md
│   └── source_text/
│       └── SS-23-002.txt         source text used by gen_site.py checks
├── scripts/
│   ├── partA.py                  inventory -> map
│   ├── partB.py                  map -> question tree
│   ├── render_md.py              tree -> Markdown
│   ├── decision_rights.py        inventory + map -> decision rights
│   └── gen_site.py               all of the above -> site/data.json
├── site/
│   ├── index.html                the navigator page
│   └── data.json
└── tests/
    ├── test_decisions.py
    ├── test_employee.py
    ├── test_multi.py
    ├── test_score.py
    ├── test_steps.py
    ├── test_v2.py
    ├── test_views.py
    └── a11y_audit.py
```

This repository does not include the source PDFs, or the step that produced `data/stage1_inventory.json` from them.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

The code is released under the MIT License; see [LICENSE](LICENSE). The policy text quoted in `data/`, `site/data.json` and `data/source_text/` comes from GTA documents. Check the terms of those documents before reusing the quoted text.
