# Completed tasks

## 2026-11-26: Project audit
- [x] Rebuilt all 5 pipeline steps; confirmed a byte-for-byte match with the committed data (no diff)
- [x] Ran all 7 browser test suites and the accessibility audit; all pass
- [x] Profiled the corpus: 537 provisions, modality cross-tab, tiering, conflicts, open questions and unresolved references
- [x] Simulated the guardrail score and stop sign over all 6,016 answer paths and every single task
- [x] Reviewed the UI at desktop and mobile widths
- [x] Wrote [AUDIT.md](AUDIT.md) and turned its recommendations into phases in [tasks.md](tasks.md)

## 2026-11-26: Setup
- [x] Created `CLAUDE.md` (commands, pipeline architecture, content rules)

## 2026-11-26: Phase 1 — guardrails and signs
Decisions (user-approved): the proposed post values; levels Baseline rules only / Light / Standard / Extra; add an amber Check first sign; keep the decisions trigger red but reword it. Check first fires for buying other AI only: no provision requires a review before building it.
- [x] Replaced the points score (provision counts × weights) with risk factors from the answers: personal data 2, decision about a person 2, public-facing 1, buying or building 1, official document 1, legal analysis or meeting note-taking 1; Not sure counts as yes
- [x] Each factor quotes its provision, with a separate provision for the other-AI branch where one applies (other AI + personal data now shows 2 posts, not 0)
- [x] New levels: Baseline rules only (0), Light (1–2), Standard (3–4), Extra (5+); road posts equal the post count, up to 5 pairs
- [x] Neutral-to-amber palette instead of green; reasons list now shown on mobile
- [x] Reworded the decisions stop: "May be prohibited: decisions about people (the documents disagree)"
- [x] Added an amber Check first sign and banner: other-AI buying (PS-23-001 POLICY-1), other-AI personal data (SS-23-002 6-2)
- [x] Moved the factors and signs from `site/index.html` into `scripts/gen_site.py` (`factor`/`sign` records; build asserts provisions exist and generative-only documents stay on the generative branch)
- [x] Rewrote `tests/test_score.py`: independent calculation over 53,656 routes (0 mismatches), with a check that every quoted provision is shown on its route, plus 11 page routes
- [x] Full suite passes: test_decisions, test_employee, test_steps, test_v2, test_views, test_multi, test_score; accessibility audit reports no contrast, target-size or reflow issues
- [x] Updated README, CONTRIBUTING and CLAUDE.md

## 2026-11-26: Phase 2 — provenance and currency
Decisions: you will upload the PDFs; PDF download links for the 2025 documents; header shows the build date, and each citation shows its own document dates.
- [x] `scripts/verify_sources.py`: checks every excerpt and lead-in word for word against `data/source_text/<doc_id>.txt`, ignoring only print headers and footers, line breaks and hyphen line breaks. SS-23-002: all 146 excerpts and lead-ins match
- [x] Added `source_url` for SS-25-001, GS-25-001 and GS-25-002 (found by web search), with a `source_url_note` saying they need confirming
- [x] Citations show each document's effective date and, where known, the capture date of the copy used; the header now says "Page built"
- [x] `docs/questions_for_gta.md`: supersession, PS-23-001 currency, links, guardrail values, sign wording, modal readings

## 2026-11-26: Phase 3 — modal taxonomy
Decisions: keep the 10 "Conditional" cells as Must and the 2 "Do not" commands as Must not, each with a recorded reason.
- [x] New `should_not` modality for "should not" / "should never" (6 provisions); a "Should not" pill and group on the page
- [x] `classification_basis` recorded on all 283 provisions whose modality is not the literal verb
- [x] Split the U_HUMAN and C_MEETINGS summaries by modality

## 2026-11-26: Phase 4 — engineering
- [x] GitHub Actions CI: rebuild + `git diff --exit-code`, source check, all browser tests, accessibility gate (simulated locally)
- [x] `encoding='utf-8'` on all 16 `open()` calls that lacked it
- [x] Pinned `playwright==1.65.2`
- [x] System fonts only; removed Google Fonts (no third-party requests)
- [x] Removed 16 fully overridden CSS declarations and the dead mobile ordering rules; 16 before/after screenshots are byte-identical

## 2026-11-26: Phase 5 — UX and accessibility
- [x] Renamed to "GTA AI Policy Check" (page title, heading, README)
- [x] Mobile: a collapsible "Your answers (N)" list with Change buttons at the top of the results
- [x] Results header: the count tiles are now readable by screen readers and in print; removed the sentence that repeated them
- [x] Review mode is labelled "for policy staff" everywhere
- [x] Quotations: the decorative opening mark is silent to screen readers, and the unbalanced closing mark is gone from the text
- [x] Stop / Check first announcement: already announced by the polite live region whenever it appears (no change needed)
- [x] Full suite and accessibility audit pass
