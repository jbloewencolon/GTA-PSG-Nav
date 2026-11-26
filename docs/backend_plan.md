# Backend plan: usage data and trends (Microsoft Azure)

**Status:** proposal, 2026-11-26. Nothing here is built yet. Items marked ⚖️ need sign-off from GTA, agency counsel or a records officer before data collection starts.

## 1. What the backend is for

The GTA AI Policy Check is a static page. Today it records nothing: the title screen's agency and email stay in the visitor's browser. The backend adds two things:

1. **Usage events:** what people ask about and what the tool tells them, without saying who they are.
2. **Contacts:** emails that people choose to give, kept apart from usage.

Questions the data should answer:

| Question | Why it matters |
|---|---|
| How many people use the tool, from which agencies, week by week? | Adoption, and where to focus outreach |
| Which tasks and AI types do people describe, and how is that changing? | Shows demand, for example a rise in "other AI" or chatbots |
| How often does each red stop or amber Check first fire, by agency? | Shows where approvals and reviews will land, and their volume |
| Which questions get "Not sure" most often? | Questions people find unclear, or gaps in the policy itself |
| Where do people stop before reaching results? | Usability problems in the questionnaire |
| Which provisions' exact wording do people open most? | Text people need to read closely, which may need guidance |
| Which next-step links do people follow? | Whether the request routes are being used |
| Did a change in the documents or the tool change the pattern? | Before-and-after comparison by content version |

## 2. Principles

1. **Collect less.** Store answers as values from fixed lists only, never free text. Store no IP addresses and no device fingerprints. Store no identifier that lasts beyond one visit.
2. **Keep usage apart from people.** Usage events carry a random session ID that lasts one visit. Emails go to a separate store, never joined to usage.
3. **Say what is collected, where people see it.** The title screen says what is recorded and why, and offers a way to opt out.
4. **Check everything at the door.** The API accepts only known event types and values. The allowed values are generated from `site/data.json`, so the API and the page can't drift apart.
5. **Report in aggregate.** Dashboards show no count below 5 for an agency, so small agencies' users can't be singled out.
6. **Assume the records are public.** ⚖️ Data held by a state agency may be subject to the Georgia Open Records Act (O.C.G.A. § 50-18-70 et seq.) and to records retention schedules. Design as if any stored record could be requested. Counsel and the records officer confirm before launch.

## 3. Architecture

```
Browser (static page)
  │  POST /api/events   (batched JSON, sendBeacon)
  │  POST /api/contact  (only when the visitor ticks "contact me")
  ▼
Azure Static Web Apps (Standard) ── hosts site/ + linked Azure Functions API
  │                                  (custom domain, TLS, CORS locked to the site)
  ▼
Azure Functions (Python, HTTP trigger)
  │  validate against the event schema + allow-lists generated from data.json
  │  drop anything unknown; never log request bodies
  │  managed identity, no passwords in code
  ├──────────────▶ Azure SQL Database (serverless, auto-pause)
  │                  schema "usage"    : sessions, events, content dimensions
  │                  schema "contacts" : emails (separate role, Always Encrypted)
  ▼
Application Insights (function health only; IP masking left on; no request bodies)

Azure SQL ──▶ Power BI (views with small-number suppression; row-level security by agency)
Secrets: Azure Key Vault · Infrastructure: Bicep · Deploys: GitHub Actions with OIDC
```

### Why these services

| Need | Choice | Alternatives considered |
|---|---|---|
| Host the page and API under one origin | **Azure Static Web Apps (Standard)**: static hosting plus linked Functions, custom domain, Entra ID sign-in if ever needed | App Service (more to manage); keep GitHub Pages plus a separate Functions app (cross-origin calls, two places to secure) |
| Receive events | **Azure Functions**, consumption or Flex plan | API Management in front, for rate limiting at scale (add in hardening, phase D) |
| Store and query trends | **Azure SQL Database, serverless** (auto-pauses when idle, standard SQL, native Power BI connector) | Cosmos DB (no relational joins, so harder for trend SQL); Log Analytics only (short default retention, and awkward to model) |
| Dashboards | **Power BI** (likely already licensed through Microsoft 365), with row-level security by agency | Azure Monitor workbooks (fine for operations, weak for business reporting) |
| Abuse protection | SWA built-in limits, request size caps, schema validation; then Azure Front Door WAF rate-limit rules if needed | — |

## 4. What the page sends

### 4.1 Session

A **session** is one visit, from the title screen to closing the tab. Its ID is a random UUID kept in `sessionStorage`, so it disappears when the tab closes. There is no cross-visit identifier.

### 4.2 Events

Every event has: `event_id` (UUID, used to ignore duplicates), `session_id`, `type`, `ts` (client time; the server adds its own), `content_version` (the page's build date from `data.json`), and the fields below. All values come from fixed lists.

| `type` | Fields | Allowed values come from |
|---|---|---|
| `session_start` | `agency_code`, `device_class` (`desktop` / `mobile`) | Agency pick list (see 4.3) |
| `answer` | `question_id`, `values[]`, `position` (1–7) | `q` records in `data.json` (`Q_TYPE`, `Q_TASK`, `Q_ROLE`, `Q_DATA`, `Q_DECISION`, `Q_PRODUCT`, `Q_HOST`) and their option values |
| `results_view` | `posts`, `level`, `signs[]`, `topics[]`, `not_sure_count` | `factor` / `sign` records; element IDs (for example `C_DATA`, `U_REVIEW`) |
| `view_change` | `view` (`topic`/`mod`/`dt`/`doc`), `tab` (`applies`/`steps`) | Fixed |
| `wording_open` | `provision_id` | Provision IDs in `data.json` |
| `step_link` | `step_pid`, `link` (`form`/`email`/`web`) | `step` records |
| `answer_change` | `question_id` | As above |
| `session_end` | `last_question_id`, `reached_results` (bool), `duration_s` | Sent with `navigator.sendBeacon` when the page is hidden |

**Never sent:** free text, email, agency free text, IP address, user agent string, screen size, referrer, or anything typed.

### 4.3 Agency: a pick list, not free text

The demo's free-text agency box is fine for a proof of concept. For collection, replace it with a pick list of state entities, plus "Other state entity" and "Prefer not to say". A pick list:
- gives clean groups for trend reports;
- stops people typing a name or email into the agency box.

⚖️ Source the list from an official register of state entities, and have GTA own it. Store `agency_code` only.

### 4.4 Consent and opt-out

- The title screen explains what is recorded, in one sentence plus a "What we record" link to a plain-language notice.
- **Usage events** are collected for everyone who starts, with a visible "Don't record my answers" checkbox (opt-out). The browser's Global Privacy Control signal (`navigator.globalPrivacyControl`) is treated as opt-out. ⚖️ Counsel decides whether opt-in is required instead.
- **Email** is only sent if the visitor ticks "Contact me about this tool", which is unticked by default.

### 4.5 Page changes (small)

- A `telemetry.js` block: `track(type, fields)` adds events to a queue; the queue is sent every 10 events or 15 seconds, and on `visibilitychange` with `sendBeacon`.
- Telemetry turns on only when `data.json` carries `meta.telemetry_endpoint`. The GitHub Pages build leaves it out, so the public demo keeps sending nothing. `tests/test_intro.py` already fails if a request leaves the page's origin.
- Failures are silent, and never block the questionnaire.

## 5. Data model (Azure SQL)

```sql
-- usage schema: no personal data
CREATE TABLE usage.sessions (
  session_id      UNIQUEIDENTIFIER PRIMARY KEY,
  started_at      DATETIME2(0) NOT NULL,      -- server time
  agency_code     VARCHAR(32)  NOT NULL,
  device_class    VARCHAR(8)   NOT NULL,
  content_version DATE         NOT NULL,
  reached_results BIT          NULL,
  duration_s      INT          NULL
);
CREATE TABLE usage.events (
  event_id        UNIQUEIDENTIFIER PRIMARY KEY,   -- client UUID: repeats are ignored
  session_id      UNIQUEIDENTIFIER NOT NULL REFERENCES usage.sessions,
  received_at     DATETIME2(0) NOT NULL,
  type            VARCHAR(24)  NOT NULL,
  question_id     VARCHAR(16)  NULL,
  provision_id    VARCHAR(40)  NULL,
  payload         NVARCHAR(2000) NOT NULL CHECK (ISJSON(payload) = 1)  -- validated, enum-only fields
);
CREATE INDEX ix_events_type_time ON usage.events (type, received_at);

-- one row per answer value, for easy counting
CREATE TABLE usage.answers (
  session_id  UNIQUEIDENTIFIER NOT NULL REFERENCES usage.sessions,
  question_id VARCHAR(16) NOT NULL,
  value       VARCHAR(32) NOT NULL,
  is_final    BIT NOT NULL,              -- last answer before results
  PRIMARY KEY (session_id, question_id, value)
);

-- content dimensions: loaded from data.json at each deploy, keyed by content_version
CREATE TABLE usage.dim_question  (content_version DATE, question_id VARCHAR(16), text NVARCHAR(400), PRIMARY KEY (content_version, question_id));
CREATE TABLE usage.dim_option    (content_version DATE, question_id VARCHAR(16), value VARCHAR(32), label NVARCHAR(300), not_sure BIT, PRIMARY KEY (content_version, question_id, value));
CREATE TABLE usage.dim_topic     (content_version DATE, element_id VARCHAR(40), title NVARCHAR(200), tier VARCHAR(32), PRIMARY KEY (content_version, element_id));
CREATE TABLE usage.dim_provision (content_version DATE, provision_id VARCHAR(40), doc_id VARCHAR(16), section NVARCHAR(200), modality VARCHAR(16), PRIMARY KEY (content_version, provision_id));
CREATE TABLE usage.dim_agency    (agency_code VARCHAR(32) PRIMARY KEY, name NVARCHAR(200), active BIT);

-- contacts schema: separate role, never joined to usage
CREATE TABLE contacts.requests (
  contact_id   UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
  received_at  DATETIME2(0) NOT NULL,
  email        NVARCHAR(254) NOT NULL,   -- Always Encrypted (deterministic, so duplicates can be found)
  agency_code  VARCHAR(32) NULL,
  delete_after DATE NOT NULL
);
```

**Reporting views** apply suppression: any group under 5 sessions shows as "fewer than 5". Power BI reads only from views, never from the base tables.

```sql
CREATE VIEW usage.v_weekly_by_agency AS
SELECT DATEADD(week, DATEDIFF(week, 0, s.started_at), 0) AS week_start,
       s.agency_code,
       CASE WHEN COUNT(*) < 5 THEN NULL ELSE COUNT(*) END AS sessions,
       CASE WHEN COUNT(*) < 5 THEN NULL ELSE AVG(CAST(s.reached_results AS FLOAT)) END AS completion_rate
FROM usage.sessions s
GROUP BY DATEADD(week, DATEDIFF(week, 0, s.started_at), 0), s.agency_code;
```

## 6. API

| Endpoint | Body | Response | Limits |
|---|---|---|---|
| `POST /api/events` | `{ "events": [ …up to 50 ] }` | `204` always (accepted or dropped), so the client never retries in a loop | ≤ 16 KB; ≤ 50 events; ≤ 300 events per session |
| `POST /api/contact` | `{ "email", "agency_code", "consent": true }` | `204` | ≤ 1 KB; 3 per session |
| `GET /api/health` | — | `200` | — |

Validation, all at the server:
- JSON Schema per event type. Every enumerated field is checked against allow-lists generated from `data.json` at build time (a new pipeline step, `scripts/gen_schema.py`, next to `gen_site.py`).
- Unknown fields, unknown values, or a `content_version` older than 90 days: the event is dropped and counted in a metric, never stored.
- Email: format check, length ≤ 254, and stored only when `consent` is true.
- CORS allows only the site's own origin. Request bodies are never logged.

## 7. Dashboards and trend metrics

| Metric | Definition | Trend view |
|---|---|---|
| Sessions | Sessions started | Weekly, by agency; 4-week rolling average |
| Completion rate | Sessions with `reached_results` ÷ sessions | Weekly; drop-off funnel by `last_question_id` |
| Task mix | Share of final `Q_TASK` values | Monthly share; growth of each task |
| AI type mix | Generative / other / not sure / none | Monthly share |
| Stop rate | Sessions with any red stop ÷ sessions reaching results, split by sign | Weekly by agency |
| Check first rate | Same, for amber signs | Weekly by agency |
| Not sure rate | Per question: sessions answering Not sure ÷ sessions asked | Monthly; flag a question above 20% for review |
| Guardrail level mix | Share of Baseline / Light / Standard / Extra | Monthly |
| Wording opened | Top 20 provisions by `wording_open` per 100 results | Monthly; candidates for plain-language guidance |
| Step links | `step_link` per 100 results, by step | Monthly; shows whether request routes are used |
| Version effect | All of the above split by `content_version` | Before and after each content release |

**Trend detection:** compare each week with the trailing 8-week mean and standard deviation. Flag any change beyond 2 standard deviations for a series with at least 20 sessions a week. Mark content releases on every chart, so a jump can be traced to a change.

**Access:**
- GTA analysts see all agencies.
- Agency points of contact see their own agency, through Power BI row-level security on `agency_code`.
- Nobody can query the base tables through Power BI.

## 8. Security and privacy

| Risk | Control |
|---|---|
| Spam or flooding | Size and count limits; per-session caps; WAF rate rules (phase D); an alert on unusual volume |
| Injected or unexpected data | Schema validation and allow-lists; parameterized SQL; `payload` holds validated fields only |
| Personal data slipping into usage | No free-text fields; agency pick list; email only on the separate endpoint; automated test that scans `usage.*` for `@` and digit patterns |
| Re-identifying a person in a small agency | Suppress counts under 5; no exact timestamps in reports (week granularity); no device detail beyond desktop/mobile |
| Linking emails to answers | Separate schema, separate database role, and no shared key |
| Credential leakage | Managed identity for Functions to SQL; Key Vault for anything else; no secrets in the repository |
| Breach of the contacts table | Always Encrypted on `email`; short retention; Defender for SQL alerts |
| Logs revealing data | Application Insights keeps IP masking on (its default) and is never sent request bodies; log retention 30 days |
| Open records requests ⚖️ | Data minimization means a released record reveals nothing personal from `usage`; counsel confirms how `contacts` is handled |

Before launch: ⚖️ a privacy impact review, a security review against GTA's enterprise security standards, and an accessibility check of the consent text and dashboards.

## 9. Retention ⚖️

| Data | Keep | Then |
|---|---|---|
| `usage.events`, `usage.answers` | 13 months (one full year, for comparison) | Roll up into monthly aggregate tables, then delete the rows |
| `usage.sessions` | 13 months | Delete |
| Monthly aggregates | Per the records schedule | — |
| `contacts.requests` | Until the proof of concept ends, at most 12 months, or sooner on request | Delete (`delete_after`, nightly job) |
| Application Insights | 30 days | Automatic |

A nightly timer-triggered Function runs the roll-up and deletes. The retention periods must match the approved records retention schedule.

## 10. Environments, deployment and cost

- **Environments:** `dev`, `test` and `prod`, each with its own resource group, created from the same Bicep templates.
- **Deploys:** GitHub Actions signs in to Azure with OIDC federated credentials, so no stored secrets. The existing CI (rebuild + tests) runs first; then it deploys the site, the Functions, SQL schema migrations (DACPAC or versioned scripts), and the content dimensions for the new `content_version`.
- **Cost (approximate, at list prices; check with the Azure pricing calculator):**

| Item | Rough monthly cost |
|---|---|
| Static Web Apps Standard | about $9 per app |
| Functions (consumption) | likely within the free grant at proof-of-concept volume |
| Azure SQL serverless (auto-pause) | about $5–40, depending on active hours |
| Application Insights | small at this volume (billed per GB ingested) |
| Key Vault | cents |
| Power BI | per-user Pro licences, if not already held |

## 11. Testing

- **Contract tests:** every event type, valid and invalid, against the Function. Unknown values must be dropped, never stored.
- **Allow-list drift:** CI fails if `gen_schema.py` output differs from what is committed, as for the other generated files.
- **Privacy tests:**
  - Seed the database through the API, then assert that no `usage.*` column contains an `@`, a 7+ digit number or a value outside the allow-lists.
  - Assert that `contacts` can't be read by the reporting role.
- **Front end:**
  - Extend `tests/test_intro.py`: with telemetry off, no requests leave the origin (already checked); with it on, only the API is called, events are enum-only, and opt-out or Global Privacy Control means nothing is sent.
- **Load:** 50 concurrent sessions sending batched events, with p95 under 300 ms and no throttling, before launch.
- **Restore drill:** restore the SQL database from a point-in-time backup in `test` once per quarter.

## 12. Roadmap

| Phase | Work | Exit criteria |
|---|---|---|
| **A. Decide** ⚖️ | Privacy review; opt-in or opt-out; agency pick list and owner; retention; who owns the data and dashboards | Written approvals; final consent text |
| **B. Ingest (MVP)** | Bicep for SWA, Functions, SQL and Key Vault; `/api/events` and `/api/contact`; `gen_schema.py`; telemetry block in the page; contract and privacy tests | Events from `test` land in SQL; all tests green |
| **C. Report** | Reporting views with suppression; Power BI dataset and the 11 metrics; row-level security; release markers | GTA reviews the dashboard with real `test` data |
| **D. Harden** | WAF rate limits; alerts; Defender for SQL; retention jobs; load test; restore drill | Security review passed |
| **E. Launch** | Production deploy; custom domain; announce; first monthly trend report | Two weeks of clean production data |

## 13. Decisions needed

1. ⚖️ Opt-in or opt-out for usage events, and the exact notice wording.
2. ⚖️ The agency list's source and owner.
3. ⚖️ Retention periods, matched to the records schedule.
4. Who owns the dashboards, and which agency contacts get access.
5. Whether to keep GitHub Pages for the public demo and run the Azure-hosted copy for state staff, or to move entirely to Azure Static Web Apps.
6. Whether the "contact me" emails are needed at all after the proof of concept.
