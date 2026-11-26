# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

"GTA AI Policy Check": a static, single-page navigator (`site/index.html` + `site/data.json`) that asks up to 7 questions and shows which Georgia Technology Authority (GTA) AI policy provisions apply, quoting the source text verbatim. It is used for compliance, so policy wording and citations are the product.

## Commands

Pipeline (Python 3.11+, standard library only). Run from the repo root, in this order. With unchanged inputs, each step reproduces the committed files byte for byte, so `git status` after a rebuild must show no diff unless you meant to change the content.

```bash
python3 scripts/partA.py data/stage1_inventory.json data/stage2_map.json
python3 scripts/partB.py data/stage2_map.json data/stage3_triage.json 8      # must end: mism 0 redundant 0 bad_skips 0
python3 scripts/render_md.py data/stage3_triage.json data/stage3_triage.md
python3 scripts/decision_rights.py data/stage1_inventory.json data/stage2_map.json data/decision_rights.json data/decision_rights.md
NAV_UPDATED=2026-11-25 python3 scripts/gen_site.py data/stage1_inventory.json data/stage2_map.json data/stage3_triage.json site data/decision_rights.json
```

`NAV_UPDATED` sets the page's "Last updated" date; omit it and the date (and byte count) changes.

Serve and test (Playwright for Python; tests need the server running):

```bash
python3 -m http.server 8765 --directory site
python3 tests/test_score.py          # each test file is standalone; run one at a time
```

- In this cloud container, Python Playwright is not preinstalled. Install `requirements-dev.txt` into a venv, do not run `playwright install`, and set `CHROME_PATH=/opt/pw-browsers/chromium-1243/chrome-linux64/chrome` (tests default to `/usr/bin/google-chrome`).
- Each test prints one line per route ending in `PASS`/`FAIL` and exits 1 on any failure. `test_multi.py` also checks 125,280 multi-task combinations offline and ends `ALL PASS`.
- `tests/a11y_audit.py report.json` writes accessibility findings to a file, with no console output.
- `python3 scripts/verify_sources.py data/stage1_inventory.json data/source_text` checks every excerpt word for word against `data/source_text/<doc_id>.txt` (from the PDFs in `data/Instruments_GTA Policies/` with `pdftotext -layout`; `<doc_id>.raw.txt` from `pdftotext -raw` is also searched, which SS-25-001's table needs). All 537 provisions pass.
- CI (`.github/workflows/ci.yml`) runs the rebuild with `git diff --exit-code`, the source check, all browser tests and an accessibility gate. There is no linter.

## Architecture

Data flows one way through numbered stages; each script reads the previous stage's JSON:

1. `data/stage1_inventory.json`: the **input**: 537 provisions from 7 documents, each with `text_excerpt`, `modality` (must / must_not / should / should_not / may / informational), `modal_as_written`, and a `classification_basis` wherever the modality is not the literal verb. Also holds conflicts (C##), open questions (OQ##) and unresolved references (UR##). The source PDFs are in `data/Instruments_GTA Policies/`; the PDF-to-inventory step is not in the repo.
2. `scripts/partA.py` → `stage2_map.json`: groups provisions into **elements**, hand-written in Python (`E(...)` calls). Each element has a tier (`umbrella` = always shown, `conditional` = shown when its `activated_by` matches the answers, `out_of_scope_for_employee` = agency-only, reached via **indirect pointers**). It also defines the **facts** (F_TYPE, F_TASK, F_ROLE, F_DATA, F_DECISION, F_PRODUCT, F_HOST) and `ai_type_rule`: when F_TYPE is "other", only provisions outside the generative-only documents (SS-25-001, GS-25-001) are shown.
3. `scripts/partB.py` → `stage3_triage.json`: builds the question tree (text, help, `ask_if` skips, "Not sure" confirm text), then enumerates every path and checks the tree's outcome against the map. Any mismatch, redundant question or bad skip is a bug.
4. `scripts/decision_rights.py` → `decision_rights.json`/`.md`: who decides what (DR-##), hand-written; every role is asserted to be a verbatim substring of its provision.
5. `scripts/gen_site.py` → `site/data.json`: flattens everything into records keyed by `k` (`meta`, `q`, `el`, `ptr`, `step`, `dec`, `stepgap`). Next-step cards (`STEPS`) and step→decision links (`STEPDEC`) are hard-coded here, and their quotes and links are asserted against the source text.

`site/index.html` is one file of dense, inline vanilla JS and CSS. It opens on a title screen (`renderIntro()`: agency required, email optional, kept in `localStorage` only, every access in try/catch); browser tests must fill `#agency` and click `#start` first. It loads `data.json`, re-implements `match()`/`ask_if` from the tree, and renders the question flow, results (four grouping views), the Next steps tab and the review mode (`#review`). The side panel opens with "Rules that apply to you" (`rulesNow()`/`renderRules()`): 0 until the first answer, then provisions in shown topics by modality, excluding Notes and agency pointers; the label shows the change from the last answer, and legend rows call `goObl()` to open the grouped-by-obligation view at `#grp-<modality>` (agency rows sit in `#grp-agency`). `startOver()` clears answers and returns to the first question (agency kept). `tests/test_obligations.py` checks it. Guardrail factors and the red stop / amber Check first signs are defined in `gen_site.py` (`FACTORS`, `SIGNS`) and rendered by `factorsNow()`/`signsNow()`/`renderRail()`; level cut-offs (`levelOf()`, `PMAX`) are in the page. `tests/test_score.py` holds an independent `expected()` calculation of the approved design, so change it together with them. CSS is in layered override blocks (`/* 1 header band */` … `/* 8 polish */`) that redefine earlier rules; check later blocks before editing an earlier one.

## Content rules (from CONTRIBUTING.md)

- Every provision cites document title, identifier (if any), section or page.
- Keep modal verbs exactly as written; never make a requirement stronger or weaker.
- A reference to something outside the 7 documents is an unresolved reference; don't describe it.
- Where the evidence doesn't settle a question, add an open question rather than choosing an answer.
- Add a red stop only where a provision requires GTA approval or prohibits the use; add an amber Check first only where a provision requires a review or authorization first. Cite either by provision ID.

## Deployment and backend

`.github/workflows/pages.yml` publishes `site/` to GitHub Pages from `main`. There is no backend: `docs/backend_plan.md` is the Azure plan for usage data, and the page must send nothing off-origin until it is built (`tests/test_intro.py` checks this).

## Project tracking

`AUDIT.md` holds the 2026-11-26 audit. Planned work is in `tasks.md` (phases); move finished items to `completed_tasks.md`.
