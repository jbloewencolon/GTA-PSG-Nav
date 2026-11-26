# Decision rights in the GTA AI documents (Phase 1 inventory, for review)

Rendered from `decision_rights.json`. Built only from the seven documents. Roles are quoted as written.

19 decision points: 12 named, 2 where the documents disagree, 5 not named.

## DR-01: Entering PII, PHI, regulated, confidential or sensitive data into an AI tool

- **Who decides:** Documents disagree. Three provisions name three different approvers. No document gives a request process.
- **Type:** approval; **level:** employee
- Decides: “GTA’s Office of Artificial Intelligence” (Generative AI Responsible Use (SS-25-001), 1.3 Data Privacy and Confidentiality, p.3; modal as written: shall not). Shown today via `C_DATA`.
- Decides: “appropriate agency authority” (Artificial Intelligence Responsible Use (SS-23-002), 6. Data Protection, Safety and Privacy, p.9; modal as written: must). Shown today via `P_DATA_AUTHORITY`.
- Decides: “Georgia Technology Authority” (Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Rubric, p.10; modal as written: Always verify (imperative)). Shown today via `C_DATA`.
- Consulted: “department's data privacy officer or designated compliance authority” (Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.2; modal as written: should). Shown today via `C_DATA_UNSURE`.
- See: C04, OQ09, UR12, UR27

## DR-02: Using a personal email address to access GenAI tools for state business

- **Who decides:** Named. The role is named but not identified; the documents do not say who holds it in an agency.
- **Type:** authorization; **level:** employee
- Decides: “agency’s technology leadership” (Generative AI Responsible Use (SS-25-001), 1.4 Approved Use of State Credentials, p.3; modal as written: is prohibited unless). Shown today via `U_CREDENTIALS`.
- See: C05, UR27

## DR-03: Procuring a GenAI product or service

- **Who decides:** Named. GTA is named; the office within GTA that approves is not. The 2023 documents describe other review routes (DR-04).
- **Type:** approval; **level:** employee
- Decides: “Georgia Technology Authority (GTA)” (Generative AI Responsible Use (SS-25-001), 1.5 Procurement and Third-Party Vendor Compliance, p.3; modal as written: must (in lead-in)). Shown today via `C_PROCURE_APPROVAL`.
- Consulted: “GTA Office of Artificial Intelligence” (Generative AI Responsible Use (SS-25-001), 1.5 Procurement and Third-Party Vendor Compliance, p.4; modal as written: must). Shown today via `P_PROCUREMENT`.
- Channel: “https://ai.georgia.gov/ai-application-and-tool-request-form”
- Timing: “approved in advance”
- See: C08, OQ07, UR10

## DR-04: Review of any AI software, application, tool or service before procurement

- **Who decides:** Named. The documents describe a review and a response from the State CIO. They do not call the response an approval.
- **Type:** review; **level:** agency
- Asks: “Agencies shall submit” (Enterprise Artificial Intelligence Responsible Use (PS-23-001), Policy, p.3; modal as written: shall). Shown today via `P_PROCUREMENT`.
- Reviews: “GTA for review” (Enterprise Artificial Intelligence Responsible Use (PS-23-001), Policy, p.3; modal as written: shall). Shown today via `P_PROCUREMENT`.
- Reviews: “GTA will assess the tool for safety, privacy, and compliance” (Artificial Intelligence Responsible Use (SS-23-002), 3. Procuring AI Solutions, p.5; modal as written: will). Not shown by the tool today.
- Decides: “The State CIO will provide a response to the senior executive of the requesting agency” (Artificial Intelligence Responsible Use (SS-23-002), 3. Procuring AI Solutions, p.5; modal as written: will). Not shown by the tool today.
- Channel: “Business Solutions Review (BSR) Request form to GTA via email”
- Timing: “prior to procurement”
- See: C02, C03, C08, OQ01, OQ17, OQ29, UR11

## DR-05: Purchasing a premium version of a GenAI tool

- **Who decides:** Named. Agencies 'retain discretion'. How this fits with GTA's advance approval of any GenAI procurement (DR-03) is not stated.
- **Type:** discretion; **level:** agency
- Decides: “Individual agencies” (Generative AI Responsible Use (SS-25-001), Standard (opening paragraphs, before section 1), p.2; modal as written: retain discretion to). Shown today via `P_PROCUREMENT`.
- See: OQ07

## DR-06: Setting additional agency restrictions on GenAI use

- **Who decides:** Named. Agencies set the restrictions and 'should first consult' GTA.
- **Type:** determination; **level:** agency
- Decides: “Agencies” (Generative AI Responsible Use (SS-25-001), Standard (opening paragraphs, before section 1), p.2; modal as written: shall). Shown today via `P_AGENCY_RESTRICTIONS`.
- Consulted: “Georgia Technology Authority (GTA)” (Generative AI Responsible Use (SS-25-001), Standard (opening paragraphs, before section 1), p.2; modal as written: should). Shown today via `P_AGENCY_RESTRICTIONS`.
- See: OQ08, UR31

## DR-07: Conditional Approval for a specific use case of a GenAI tool

- **Who decides:** Not named. The provision gives where to send the request. It does not say who grants it, or which uses need it.
- **Type:** approval; **level:** employee
- Asks: “can be requested” (Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (sentence below the table), p.8; modal as written: can be requested). Shown today via `U_APPROVED_TOOLS`.
- Channel: “ai.georgia.gov or email ai@gta.georgia.gov”
- See: OQ10, UR13

## DR-08: Reviewing AI-generated content before it is used

- **Who decides:** Documents disagree. SS-25-001 defines Qualified Personnel as the subject-matter employee who would otherwise be responsible for the content; SS-23-002 names the business owner or designated personnel, and a different trigger.
- **Type:** review; **level:** employee
- Decides: “qualified personnel” (Generative AI Responsible Use (SS-25-001), 1. Human Review and Validation, p.2; modal as written: shall). Shown today via `U_REVIEW`.
- Decides: “business owner or designated personnel” (Artificial Intelligence Responsible Use (SS-23-002), 5. Ensuring Accuracy and Appropriateness of AI-generated Outputs, p.9; modal as written: shall (in lead-in)). Shown today via `P_AGENCY_GUIDELINES`.
- Timing: “before being used in any official capacity”
- See: C13, OQ09, OQ25

## DR-09: Which AI tools, vendors and versions employees may use

- **Who decides:** Named. GTA vets tools and vendors. Approval is per version and 'can always' be revoked; who revokes is not stated. No list of vetted tools is in the document set.
- **Type:** vetting; **level:** employee
- Decides: “GTA has vetted” (Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.1; modal as written: should). Shown today via `U_APPROVED_TOOLS`.
- Consulted: “consult with GTA” (Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.2; modal as written: are encouraged to). Shown today via `U_APPROVED_TOOLS`.
- See: OQ07, UR14

## DR-10: Admitting a project to the Horizons Innovation Lab sandbox

- **Who decides:** Not named. Agencies submit a proposal. The documents do not say who accepts or declines it.
- **Type:** approval; **level:** agency
- Asks: “agencies shall” (Generative AI Responsible Use (SS-25-001), 2.2 Participation Requirements, p.5; modal as written: shall (in lead-in)). Shown today via `P_SANDBOX`.
- Channel: “https://ai.georgia.gov/innovation-lab/how-do-i-submit-project-innovation-lab”
- See: UR17

## DR-11: Security vetting of a tool tested in the sandbox

- **Who decides:** Named. Either of two roles may vet; the documents do not say which one applies when.
- **Type:** vetting; **level:** agency
- Decides: “GTA Office of Information Security or the agency’s Information Security Officer” (Generative AI Responsible Use (SS-25-001), 2.3 Security and Oversight, p.5; modal as written: shall (in lead-in)). Not shown by the tool today.
- See: UR17, UR27

## DR-12: Using sensitive or PII datasets in the sandbox

- **Who decides:** Not named. The provision allows an exception 'unless otherwise approved' and names no approver.
- **Type:** approval; **level:** agency
- Asks: “unless otherwise approved” (Generative AI Responsible Use (SS-25-001), 2.3 Security and Oversight, p.5; modal as written: shall (in lead-in)). Not shown by the tool today.
- See: C04, UR17

## DR-13: Moving a sandbox project into pilot or production

- **Who decides:** Not named. Agencies 'shall seek approval'; the approver is not named. The next lines say GTA will review Sandbox reports and risk assessments.
- **Type:** approval; **level:** agency
- Asks: “agencies shall seek approval” (Generative AI Responsible Use (SS-25-001), 2.5 Advancement and Scaling, p.5; modal as written: shall). Shown today via `P_SANDBOX`.
- Reviews: “Review Sandbox reports and risk assessments” (Generative AI Responsible Use (SS-25-001), 2.5 Advancement and Scaling, p.5; modal as written: will (in lead-in)). Not shown by the tool today.
- Timing: “Following successful sandbox evaluation”
- See: UR17

## DR-14: Going ahead with a novel, high-risk or ambiguous use case

- **Who decides:** Not named. Agencies assess the risk and consult the Office of AI. The documents do not say who decides whether the use goes ahead.
- **Type:** consultation; **level:** agency
- Reviews: “Agencies should conduct their own risk assessments” (Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (text above and below the table), p.6; modal as written: should). Shown today via `P_HIGH_RISK`.
- Consulted: “Georgia Technology Authority (GTA) Office of Artificial Intelligence” (Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (text above and below the table), p.6; modal as written: should). Shown today via `P_HIGH_RISK`.
- See: OQ09, OQ10

## DR-15: Recording or transcribing a virtual meeting

- **Who decides:** Named. Meeting hosts are 'responsible for determining the need for recordings and automated transcriptions'.
- **Type:** determination; **level:** employee
- Decides: “Meeting hosts” (Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Be Vigilant in Virtual Meetings, p.3; modal as written: are responsible for). Shown today via `C_MEETING_HOST`.
- See: OQ12

## DR-16: Legal or regulatory analysis with GenAI

- **Who decides:** Named. The table's Conditional cell requires 'legal staff oversight'; it does not say which legal staff.
- **Type:** oversight; **level:** employee
- Decides: “legal staff” (Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.8; modal as written: imperative under column heading 'Conditional' (legend: Yellow = Caution)). Shown today via `C_TASK_LEGAL`.
- See: OQ10

## DR-17: Ordering an AI tool to stop being used

- **Who decides:** Named. Either may order termination of use.
- **Type:** order; **level:** agency
- Decides: “The State CIO or GTA OIS” (Artificial Intelligence Responsible Use (SS-23-002), 10. Termination and Business Continuity, p.13; modal as written: may). Not shown by the tool today.
- See: UR27

## DR-18: Further investigation of reported misuse, and deviation from corrective action

- **Who decides:** Named. GTA OIS decides whether further investigation is warranted and approves any deviation.
- **Type:** determination; **level:** agency
- Decides: “GTA OIS determines” (Artificial Intelligence Responsible Use (SS-23-002), 8. Reporting Misuse, p.11; modal as written: shall). Not shown by the tool today.
- Decides: “subject to GTA OIS’s approval” (Artificial Intelligence Responsible Use (SS-23-002), 8. Reporting Misuse, p.11; modal as written: must). Not shown by the tool today.
- See: C10, OQ19, UR27

## DR-19: Revoking tool access for not following SS-25-001 requirements

- **Who decides:** Named. GTA is named for oversight actions; which requirements the sentence covers is an open question.
- **Type:** order; **level:** employee
- Decides: “revocation of tool access and additional oversight actions by GTA” (Generative AI Responsible Use (SS-25-001), 1.7 Records Management and Public Access Compliance, p.4; modal as written: may result in (consequence)). Shown today via `U_CONSEQUENCES`.
- See: OQ18

## Left out

- Reporting duties (incidents, misuse, development risks, inventories) are routes for information, not decisions; see next_steps_scan.md.
- The guiding-principle items and GS-25-002 name no decider for any step.
- Roles, bodies and documents outside the seven documents (for example SM-14-008, the State CTO, EPMO, DOAS, OPB, an Executive Decision-Making Board) are not included.
