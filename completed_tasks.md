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
