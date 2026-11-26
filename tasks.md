# Tasks

From [AUDIT.md](AUDIT.md) (2026-11-26). Phases are in priority order. Items marked 🔏 change what employees are told and need GTA policy-owner sign-off.

## Phase 1: Scoring and stop sign — done 2026-11-26 (see completed_tasks.md)
- [ ] 🔏 Get GTA policy-owner sign-off on the post values, level cut-offs and sign wording (currently marked as the tool's own values)
- [ ] Consider showing the post count in the rail while a stop or Check first sign is showing (it is currently only in the reasons list and the meter's screen-reader text)

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
