# Audit: GTA AI Policy Navigator

**Date:** 2026-11-26 · **Commit audited:** `c74b8fe` · **Scope:** policy fidelity, data pipeline, scoring model, UI/UX, accessibility, engineering

## Bottom line

This is an unusually rigorous policy tool. The pipeline rebuilds byte for byte. Every answer path (6,016) is checked against the applicability map with 0 mismatches. Quoted wording is checked against the source excerpts when the data is built. All 7 browser test suites pass.

The serious problems are not in the build. They are in **two layers added on top of the verified data: the guardrail score and the stop sign.** Both live only in `site/index.html`, and the pipeline's checks never see them. These two layers are what users look at first, and in several cases they point the wrong way:

1. The score ranks *making quiz flashcards* (25 points) as 8× riskier than *legal analysis* (3 points).
2. An ML model that processes personal data shows **"No extra · 0"**, even though SS-23-002 §6 says such use *must* be authorized.
3. The stop sign generalizes a prohibition that applies to one row of a table into "decisions about people are prohibited", which another GTA document contradicts.

| Area | Grade | One-line verdict |
|---|---|---|
| Policy fidelity (citations, modals, conflicts) | **A−** | Exemplary provenance. A few modal-classification calls strengthen or weaken the text. |
| Data pipeline and verification | **A** | Reproducible and exhaustively path-checked. Provenance stops at the inventory, though. |
| Scoring model (guardrails) | **D** | It measures how many provisions match, not risk, and that produces rankings that run backwards. |
| Stop-sign logic | **C** | Conservative, but it over-generalizes one trigger and misses two cases. |
| UI/UX | **B+** | Clear flow, an honest "Not sure" path, good progressive disclosure. The gauge metaphor misleads. |
| Accessibility | **A−** | 44px targets, focus management, live region, reduced motion, print. Minor issues. |
| Engineering hygiene | **B−** | No dependencies and XSS-safe. No CI, one-line-dense JS and CSS, layered overrides, encoding bugs. |

---

## 1. What was verified

| Check | Result |
|---|---|
| Rebuild all 5 pipeline steps, then `git status` | **No diff.** The README's byte-for-byte claim holds (Python 3.13). |
| `partB.py` path verification | 6,016 paths · `mism 0 redundant 0 bad_skips 0` · longest path 7 questions |
| `test_decisions`, `test_employee`, `test_score`, `test_steps`, `test_v2`, `test_views` | All PASS |
| `test_multi` | 125,280 multi-task combinations: 0 mismatches. 5 UI routes PASS |
| `a11y_audit.py` | No contrast or target-size failures reported |

## 2. Corpus profile (data science)

- **537 provisions** from 7 documents: GS-25-001 158, SS-23-002 88, SS-25-001 86, GS-25-002 85, GS-23-001 61, 5GP 55, PS-23-001 4.
- **Modality:** should 279 · must 137 · informational 71 · may 29 · must_not 21.
- **Tiering:** 280 provisions (52%) are agency-level (`out_of_scope_for_employee`). Employees see them only through 12 agency pointers. 182 are conditional, and 75 apply to every use.
- **Every provision maps to exactly one element.** None is orphaned or double-mapped. That is clean.
- **Documented uncertainty:** 13 conflicts, 30 open questions, 31 unresolved references. These are recorded instead of being resolved silently, which is the right call for a compliance tool.

### 2.1 How modal verbs were classified (risk to the "don't strengthen or weaken" rule)

`modal_as_written` crossed with `modality` shows four judgment calls that CONTRIBUTING.md's rule ("Don't make a requirement stronger or weaker") does not clearly allow:

| Pattern | Count | Classified as | Concern |
|---|---|---|---|
| Imperative, no modal verb | 190 | `should` | Defensible for guidelines, but applied to every case. |
| "Do not" imperative (same guideline) | 2 | `must_not` | **Asymmetric.** Positive imperatives are softened to *should* while negative imperatives are hardened to *must not*. |
| Table cell under "Conditional" (legend: *Yellow = Caution*) | 10 | `must` | **Strengthened.** "Caution" is not a mandate, and these 10 cells feed the score directly. |
| "should not" / "should never" | 6 | `should` | No `should_not` category exists, so in the Must/Should/May view, prohibitions sit under the "Should" heading. |
| "It's essential to" / "it is important to" | 2 / 4 | `must` / `should` / `informational` | The same phrase family is split three ways. |

**Recommendation:** add a `should_not` modality. Record a `classification_basis` for each non-literal call. Reclassify the "Conditional" cells as `should`, or as a new `conditional` modality, unless GTA confirms they are mandatory.

## 3. The guardrail score (highest-impact finding)

> **Status 2026-11-26:** addressed in Phase 1. The score is replaced by fact-based guardrail posts (see `completed_tasks.md`). GTA sign-off is still pending.

The score is `Σ (must + 2×must_not provisions) × weight` over active conditional elements. Weights: task = 1, HEAVY = 4, other = 2. I computed it for every single task, holding the other answers at the lowest-risk value (generative AI, use only, no data, no decision, no AI content in the product):

| Task | Score | Band |
|---|---|---|
| Policy drafting | **25** | Standard (1 point below Extra) |
| Education / training (quizzes, flashcards) | **25** | Standard |
| Public chatbot | 8 | Light |
| Coding | 7 | Light |
| Internal summaries, internal chatbot, media | 5 | Light |
| Public comms, data analysis, translation | 3 | Light |
| **Legal / regulatory analysis** | **3** | Light |
| Research, content | 2 | Light |
| **Meetings (AI note-takers)** | **0** | **No extra** |

**Why:** policy drafting and education automatically switch on `C_DECISIONS` (weight 4, two `must_not` rows doubled), because the SS-25-001 table happens to place its people-decision prohibitions in those rows. Meanwhile, the meetings guidance is all *should* ("strongly discouraged"), so it scores 0. The score reflects **how the source tables are laid out and how many provisions they contain**, not exposure or risk.

**More problems:**
- **The "Not sure" answer and the stop sign dominate.** Across all 6,016 paths, 94% end in "Stop", and the share is still 87% when "Not sure" answers are excluded. On realistic inputs the bands are rarely seen. When users do see them, the bands are miscalibrated.
- **Agency pointers score 0.** So **other AI + personal data → "No extra · 0"**, while the results pane shows pointer `P_DATA_AUTHORITY`, which quotes SS-23-002 §6: data "*must* be authorized by appropriate agency authority". The gauge contradicts the content shown next to it.
- **The colours are green.** The band colours run from light to dark green, which reads as "go".

**Recommendations (pick one):**
1. **Remove the numeric score** (the YAGNI option). Keep the stop sign, plus a plain count: "N requirements and M prohibitions apply".
2. Or **redefine it as risk:** score on the facts (data, decision, public-facing, procurement), not on how many provisions matched. Score agency pointers. Publish the rubric and get GTA's sign-off.
3. At minimum, change the labels so they cannot be read as permission ("No extra" → "Baseline rules only"), and switch the scale to neutral colours.

## 4. Stop sign

> **Status 2026-11-26:** addressed in Phase 1. The decisions trigger is reworded, and an amber Check first sign covers other-AI buying and personal data. `SIGNS` now lives in `gen_site.py`.

| Trigger | Assessment |
|---|---|
| `F_DATA` yes or not sure → SS-25-001 1.3 | ✅ Faithful ("shall not … unless formally approved by GTA's Office of AI"). |
| `F_ROLE` procure, both or not sure → SS-25-001 1.5 | ✅ Faithful for GenAI. |
| `F_DECISION` yes or not sure → TABLE-15 "Listed as prohibited" | ⚠️ **Over-generalized.** TABLE-15 sits in the *Policy drafting* row and prohibits GenAI to "**make** legal, disciplinary, or eligibility decisions". The question asks about "make, **or help make**, a decision about a specific person". GS-25-001-SAFE-9 says HR "**may** consult with AI platforms in making hiring decisions". The banner does show that disagreement (OQ13), but the headline still says "prohibited". |
| Other AI + procurement | ❌ **Missing.** PS-23-001: "Agencies **shall** submit **all** software … utilizing AI … to GTA for review prior to procurement". That covers all AI, yet there is no stop. Strictly this is "review", not "approval" (DR-04), but an employee is still blocked until the review happens. |
| Other AI + personal data | ❌ **Missing.** SS-23-002-6-2 ("must be authorized by appropriate agency authority") applies to all AI. |

**Recommendations:** relabel the decision trigger "May be prohibited: the documents disagree". Add an amber "Check first" state for review and authorization requirements that do not come from GTA's Office of AI. **Move `STOPS` into the pipeline** (`gen_site.py`) so the existing quote verification covers it.

## 5. Provenance and currency (policy analysis)

- **The trust chain ends at `stage1_inventory.json`.** `gen_site.py` checks step quotes against `text_excerpt`, which is the inventory's own copy, so the check is circular. The one exception is SS-23-002, which has its full source text in `data/source_text/`. **Add source text for all 7 documents** and a check that every `text_excerpt` appears verbatim in it. That would make the whole corpus auditable, not only the last step.
- **The three most important documents have no `source_url`** (SS-25-001, GS-25-001, GS-25-002, the 2025 set). Users see "Source: the GTA PDF of this document, page N" and cannot click through to check.
- **"Last updated: 25 November 2026" is the build date.** The documents were captured on **21 July 2026**, and PS-23-001's review date (01/15/2025) has passed. Show "Documents as of 21 July 2026" separately from the build date. A user reads "last updated" as "the policy is current".
- **Supersession is unresolved.** The 2023 and 2025 documents are shown side by side, and none says it supersedes another. This is handled honestly through conflicts C11 and C13, but it is the biggest open policy question. It should be put to GTA as a single question, not left spread across a dozen open questions.
- **Naming drift:** the page is titled "GTA **GenAI** Policy Check", but it also handles other AI. The README calls it "gta-ai-policy-navigator", and the repo is `GTA-PSG-Nav`.

## 6. UI/UX

**Strengths**
- One question at a time, at most 7, with a "Your answers" panel for editing and a progress row.
- "Not sure" is available everywhere and resolves conservatively, with a "confirm with…" pointer quoted from the source. This is excellent design for a compliance tool.
- Exact wording is always one click away. Citation chips show the modal verb as written, and the review mode (`#review`) separates policy-staff detail from employee view.
- Multi-select task question with clear "Select all that apply" behaviour; "Not sure" clears the other choices.

**Issues**
| # | Issue | Fix |
|---|---|---|
| U1 | The gauge and the content can disagree (see §3), and the gauge is the most prominent element. | See §3. |
| U2 | On mobile, the rail (stop reasons, "Your answers", "Change") is placed **after** the full results list. `index.html:280` (`.grid>.rail{order:2}`) overrides the intended `order:-1` at line 136, so editing answers means scrolling past dozens of cards. | Put a compact answers summary above the results on narrow screens. Delete the dead rule. |
| U3 | The results page leads with three tiles and a sentence restating the same three numbers. | Keep one or the other. |
| U4 | The switch is labelled "Review details (for GTA admins)", while the README says "policy staff". | Pick one audience name. |
| U5 | The road-and-guardrail illustration is decorative. It takes about 110px of prime space and carries no information beyond the level label. | Consider removing it, or shrink it on mobile. |
| U6 | The meetings task scores 0 even though AI note-takers are "strongly discouraged". | Covered by §3. |

## 7. Accessibility (WCAG 2.1 AA)

Good: 44px minimum targets, visible `:focus-visible`, focus moves to the question heading on each step, a polite live region for gauge changes, `role="meter"` with `aria-valuetext`, a proper tablist with arrow, Home and End keys, `prefers-reduced-motion` respected, decorative SVGs hidden, a screen-reader "(opens in a new tab)" suffix on links, and a print sheet that expands every `<details>`.

Minor:
- The opening quotation mark comes from CSS `::before`, and only the closing mark is real text (`quote()`, `index.html:400`). Screen readers announce an unbalanced quote. Put both marks in the text, or neither.
- The stop banner uses `role="note"`. Since it is the most important message, consider `role="alert"` on first appearance, or move focus to it.
- The tab-bar bottom border has a non-text contrast of 1.44:1. It is decorative, but the unselected tabs rely on it.
- `aria-valuemax="60"` while "Full" begins at 50. That is fine, but document it.

## 8. Engineering

| Finding | Severity | Location |
|---|---|---|
| No CI. Tests need a manually started server and a hard-coded `/usr/bin/google-chrome`. | Medium | `tests/*.py` |
| `open()` without `encoding=` on files containing curly quotes. This breaks on Windows (cp1252). | Medium | `scripts/decision_rights.py:9,157,176`; `scripts/gen_site.py:70,74` |
| Policy content is hard-coded in Python (`partA.py`, ~55KB) and JS (`STOPS`, `HEAVY`). Content edits are code edits. | Medium | `scripts/partA.py`, `site/index.html:347-356` |
| Dense one-line JS and CSS, with CSS "patch layers" (`/* 1 header band */` … `/* 8 polish */`) that redefine earlier rules. Hard to review. | Low | `site/index.html` |
| `requirements-dev.txt` is unpinned (`playwright`), while the README says 1.63.0. | Low | `requirements-dev.txt` |
| Google Fonts are loaded on a state-employee tool. This sends staff IP addresses to a third party, and it may be blocked on state networks (a fallback exists). | Low | `site/index.html:7-8` |
| The process that builds the inventory from PDFs is not in the repository (the README discloses this). | Info | — |
| ✅ DOM is built with `textContent`. `innerHTML` is used only for constant SVG icons, so there is no XSS. | — | — |
| ✅ No runtime dependencies, and the pipeline uses the standard library only. | — | — |

## 9. Prioritized recommendations

1. **Fix or remove the guardrail score** (§3). It currently ranks risk backwards.
2. **Fix the stop sign:** relabel the decision trigger, add "check first" for other-AI procurement and data, and move `STOPS` into the verified pipeline (§4).
3. **Close the provenance gap:** source text for all 7 documents, verbatim checks on every excerpt, and source URLs for the 2025 documents (§5).
4. **Separate the documents-as-of date from the build date** (§5).
5. **Modal taxonomy:** add `should_not` and a `classification_basis` field, and review the 10 "Conditional" cells (§2.1).
6. **Add CI** (GitHub Actions: rebuild → `git diff --exit-code` → serve → tests). Fix the file encodings.
7. **Mobile:** answers summary above the results (U2).
8. **Accessibility polish** (§7).

Items 1, 2 and 5 change what employees are told. They need GTA policy-owner sign-off, not only a code review.
