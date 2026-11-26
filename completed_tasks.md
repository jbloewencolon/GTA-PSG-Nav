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

## 2026-11-26: Source PDFs verified
- [x] Extracted the 7 uploaded PDFs (`data/Instruments_GTA Policies/`) into `data/source_text/`; the re-extracted SS-23-002 is identical to the existing text file
- [x] `verify_sources.py`: also searches other extractions of the same PDF (`SS-25-001.raw.txt`, which keeps table cells whole) and rejoins em dashes at line breaks
- [x] All 537 provisions in all 7 documents match their source word for word; a mutation test (one changed modal verb, one dropped comma) fails as expected
- [x] Removed `desktop.ini` (Google Drive folder settings) and ignored it
- [x] CI confirmed on GitHub: runs 1–6 (branch and main) all succeeded
- [x] Proof-of-concept screenshots: 9 images in docs/images/ (3200×1800, phone 1170×2532); README Screenshots section

## 2026-11-26: Demo hosting, title screen, backend plan
Decisions: details kept in the browser only; agency required, email optional; proof-of-concept notice and noindex; Azure for the backend.
- [x] `.github/workflows/pages.yml`: publishes `site/` to GitHub Pages from `main`
- [x] Title screen: proof-of-concept notice, agency (required) and work email (optional, format-checked), stored only in `localStorage` with guarded access; "Forget my details"; Start over returns to it; agency shown in Your answers; answers card hidden until the questions start
- [x] Header pill "Proof of concept · not an official GTA tool"; `noindex, nofollow`
- [x] `tests/test_intro.py` (15 checks, incl. no off-origin requests and blocked storage); all other tests updated to pass the title screen; title screen added to the accessibility audit, which caught and fixed a 320px reflow overflow
- [x] Screenshots regenerated, plus `00-title-screen.png`
- [x] `docs/backend_plan.md`: Azure plan (Static Web Apps, Functions, Azure SQL, Power BI), event model, schema, API, metrics, security, retention, testing, roadmap
- [x] Diagrams 10–15 (data pipeline, data at a glance, JSON anatomy, tech stack, current and planned architecture), generated from the data by docs/diagrams/; README Architecture and data section
- [x] 16-tech-stack-simple.png: plain-language, logo version for non-expert audiences (Simple Icons, CC0; trademark notice in docs/diagrams/icons/NOTICE.md)
- [x] Diagrams 10–16 reworked to show the proposed Georgia build (State's Microsoft Azure, GTA approval, Power BI insights), all marked PROPOSED; GitHub removed from the simplified stack; 14 renamed 14-architecture-georgia.png

## 2026-11-26: Live count restored as "Rules that apply to you"
Diagnosis: the live site worked as built, but Phase 1 replaced the rule count with risk-based posts that move only for six factors, so on many routes the panel sat at "0 posts" and felt broken.
- [x] New first card in the side panel: total rules that apply (must, must not, should, should not, may), "+N from your answers", a pulse when it changes (off with reduced motion), a segmented bar and legend by obligation, and a note of Notes and agency rules not counted
- [x] On results, a link opens the rules grouped by obligation; the live region announces the new total
- [x] Guardrail posts and stop / Check first signs unchanged
- [x] `tests/test_obligations.py` (added to CI): count and breakdown match the data after every answer on 4 routes; all 9 suites and the accessibility audit pass
- [x] Page screenshots 00–09 regenerated
- [x] Title screen simplified: one centred card (heading, one-line intro, agency, optional email, full-width Start, one privacy line); side panel and header description hidden until the questions start; whole form fits on a phone screen
