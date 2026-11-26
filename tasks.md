# Tasks

From [AUDIT.md](AUDIT.md) (2026-11-26). Phases are in priority order. Items marked 🔏 change what employees are told and need GTA policy-owner sign-off.

## Phase 1: Scoring and stop sign (high impact)
- [ ] 🔏 Decide: remove the numeric guardrail score, or redefine it as a fact-based risk rubric (AUDIT §3)
- [ ] If kept: score agency pointers so that other AI + personal data does not show "No extra · 0"
- [ ] Relabel bands so they cannot be read as permission ("No extra" → "Baseline rules only"); use neutral colours instead of green
- [ ] 🔏 Relabel the `F_DECISION` stop trigger: "May be prohibited: the documents disagree" (TABLE-15 vs GS-25-001-SAFE-9)
- [ ] 🔏 Add a "Check first" state for other-AI procurement (PS-23-001 POLICY-1) and other-AI data (SS-23-002-6-2)
- [ ] Move `STOPS` (and `HEAVY`, if kept) from `site/index.html` into `gen_site.py` so quote verification covers them; update `tests/test_score.py`

## Phase 2: Provenance and currency
- [ ] Add `data/source_text/` for all 7 documents
- [ ] Add a pipeline check that every `text_excerpt` appears verbatim in its source text
- [ ] Add `source_url` for SS-25-001, GS-25-001, GS-25-002
- [ ] Show "Documents as of <capture date>" separately from the build date
- [ ] 🔏 Put the 2023 vs 2025 supersession question to GTA as a single question

## Phase 3: Modal taxonomy
- [ ] Add a `should_not` modality (6 provisions)
- [ ] Add `classification_basis` for each non-literal modal call
- [ ] 🔏 Review the 10 "Conditional" (Yellow = Caution) table cells currently classified as `must`
- [ ] Make imperative handling symmetric ("do not" vs positive imperatives in guidelines)

## Phase 4: Engineering
- [ ] GitHub Actions: rebuild → `git diff --exit-code` → serve → run tests
- [ ] Add `encoding='utf-8'` to every `open()` in `decision_rights.py` and `gen_site.py`
- [ ] Pin `playwright` in `requirements-dev.txt`
- [ ] Remove dead or overridden CSS (`index.html:136-137` vs `:280`); collapse the CSS patch layers
- [ ] Decide whether to self-host fonts or use system fonts (privacy, state-network blocking)

## Phase 5: UX and accessibility polish
- [ ] Mobile: compact answers summary above the results
- [ ] Remove the duplicated tiles or sentence on the results header
- [ ] Use one audience name for review mode ("GTA admins" vs "policy staff")
- [ ] Balanced quotation marks in text (not CSS `::before`)
- [ ] Stop banner: announce on first appearance (`role="alert"` or move focus)
- [ ] Align the product name (GenAI Policy Check / AI Policy Navigator / GTA-PSG-Nav)
