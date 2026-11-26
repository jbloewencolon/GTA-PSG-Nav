# Tasks

From [AUDIT.md](AUDIT.md) (2026-11-26). Phases 1–5 are done; see [completed_tasks.md](completed_tasks.md). Items marked 🔏 need GTA policy-owner sign-off. They are collected in [docs/questions_for_gta.md](docs/questions_for_gta.md).

## Waiting on GTA (🔏, see docs/questions_for_gta.md)
- [ ] Which 2023 documents the 2025 documents replace, and whether PS-23-001 has a newer version
- [ ] Confirm the three 2025 document links (found by web search)
- [ ] Guardrail post values, level cut-offs and sign wording
- [ ] Scope of the "decisions about people" prohibition (SS-25-001-3.0-TABLE-15 vs GS-25-001-SAFE-9)
- [ ] Whether the 10 "Conditional" table cells are mandatory (currently read as Must)
- [ ] Whether the 2 "Do not" commands in GS-25-001 are Must not (currently yes)

## Optional
- [ ] Show the post count in the rail while a stop or Check first sign is showing (it is currently only in the reasons list and the meter's screen-reader text)
- [ ] Merge the remaining CSS "patch layer" blocks into the base rules. The 16 fully overridden declarations are already removed; what remains is a readability refactor with no visible effect

## Demo hosting
- [ ] Turn on GitHub Pages once: Settings → Pages → Source: **GitHub Actions** (then merge to `main`)

## Backend for usage data and trends (plan: docs/backend_plan.md)
- [ ] 🔏 Phase A, decide: privacy review; opt-in or opt-out; agency pick list and owner; retention; data and dashboard owners
- [ ] Phase B, ingest (MVP): Bicep (Static Web Apps, Functions, Azure SQL, Key Vault); `/api/events` and `/api/contact`; `scripts/gen_schema.py` allow-lists; telemetry block in the page (off unless `meta.telemetry_endpoint` is set); contract and privacy tests
- [ ] Phase C, report: suppressed reporting views; Power BI dataset with the 11 metrics; row-level security by agency; release markers
- [ ] Phase D, harden: WAF rate limits, alerts, Defender for SQL, retention jobs, load test, restore drill
- [ ] Phase E, launch: production deploy, custom domain, first monthly trend report
- [ ] Replace the free-text agency box with the approved pick list (needed before collecting data)
