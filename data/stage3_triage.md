# GTA AI policy triage

Generated from stage3_triage.json. Source map: stage2_map.json.

# Questions

## Q_TYPE: What kind of AI is it?

SS-25-001 defines generative AI as “tools or systems used to create models that can generate new and original content, such as images, music, or text, based on patterns and examples from existing data.” SS-23-002 also defines machine learning and deep learning. None of the documents mentions AI agents; they are grouped with “Other AI”, but if an agent creates new content, choose Generative AI. If you are asking about something with no AI in it, such as an ordinary cloud application, choose “It does not use AI”.

Fact: `F_TYPE`

Asked: always

| Option | Sets | Next |
|---|---|---|
| Generative AI that writes, summarizes, or creates images, audio or video (for example ChatGPT, Gemini, Claude or Copilot) | F_TYPE = generative | Q_TASK |
| Other AI that predicts, classifies, scores or recommends without creating new content (for example machine learning or deep learning), or an AI agent that carries out tasks or takes actions on its own | F_TYPE = other | Q_TASK |
| It does not use AI | F_TYPE = none | Q_TASK |
| Not sure | F_TYPE = not_sure | Q_TASK |

If “Not sure”: Treated as generative AI, which shows every provision that could apply. The documents name no contact for this question; ask your agency.

## Q_TASK: What best describes what you are using the generative AI tool for this time?

“Generative AI” means tools “that can generate new and original content, such as images, music, or text” (SS-25-001), for example ChatGPT, Gemini, Claude or Copilot.

Fact: `F_TASK`

Asked only when: (F_TYPE is one of: generative, not_sure)

On the 'other AI' branch every element this answer activates holds only generative-AI provisions (ai_type_rule), so it cannot change the result.

| Option | Sets | Next |
|---|---|---|
| Summarizing or drafting internal documents (meeting notes, memos, internal summaries) | F_TASK = internal_summaries | Q_PRODUCT |
| Looking up or gathering information on a topic | F_TASK = research | Q_PRODUCT |
| Writing for the public (website, email to the public, social media, press) | F_TASK = public_comms | Q_PRODUCT |
| Writing, reviewing or documenting code | F_TASK = coding | Q_PRODUCT |
| Analyzing data or producing reports from data | F_TASK = data_analysis | Q_PRODUCT |
| Drafting policy language or summarizing research for policy | F_TASK = policy_drafting | Q_PRODUCT |
| Creating education or training materials | F_TASK = education_training | Q_PRODUCT |
| A chatbot or other tool that members of the public interact with | F_TASK = chatbot_public | Q_PRODUCT |
| A chatbot or other tool used only by state staff | F_TASK = chatbot_internal | Q_PRODUCT |
| Generating images, audio or video | F_TASK = media | Q_PRODUCT |
| Translation, captioning or accessibility | F_TASK = translation | Q_PRODUCT |
| Legal or regulatory analysis | F_TASK = legal | Q_PRODUCT |
| Brainstorming ideas, or checking grammar and formatting | F_TASK = content | Q_PRODUCT |
| Recording, transcribing or taking notes in a virtual meeting | F_TASK = meetings | Q_PRODUCT |
| Something else | F_TASK = other | Q_PRODUCT |
| Not sure | F_TASK = not_sure | Q_PRODUCT |

If “Not sure”: Treated as if any of the listed tasks could apply. To confirm, ask your agency: SS-25-001 (3.0, p.6) says “Agencies should conduct their own risk assessments and consult with the Georgia Technology Authority (GTA) Office of Artificial Intelligence for novel, high-risk, or ambiguous use cases not represented here.”

## Q_PRODUCT: Will anything the AI wrote or came up with appear in what you finally produce?

GS-25-001 counts AI content as part of your product “when a substantial portion of the content is featured in the final product, even if the user extensively edits it.” If it only helped you develop your own content and ideas, answer No. The documents give “an email” as the example of an informal document and do not define “more official documents”.

Fact: `F_PRODUCT`

Asked only when: (F_TYPE is one of: generative, not_sure)

On the 'other AI' branch every element this answer activates holds only generative-AI provisions (ai_type_rule), so it cannot change the result.

| Option | Sets | Next |
|---|---|---|
| No, it only helped me develop my own content and ideas | F_PRODUCT = none | Q_ROLE |
| Yes, in an informal document like an email | F_PRODUCT = informal | Q_ROLE |
| Yes, in something more official than that | F_PRODUCT = official | Q_ROLE |
| Not sure | F_PRODUCT = not_sure | Q_ROLE |

If “Not sure”: Treated as if AI content appears in a more official document. To confirm, see GS-25-001, How to Properly Cite AI-Generated Content, p.9; the documents name no contact for citation questions, so ask your agency.

## Q_ROLE: Besides using the tool yourself, are you also helping to buy an AI tool or to build one?

Buying includes licensing, contracting, an RFP, or a paid or premium version. Building includes configuring, piloting or deploying an AI tool, or developing one with an outside partner.

Fact: `F_ROLE`

Asked only when: (F_TYPE is one of: generative, other, not_sure)

Not asked when the tool does not use AI: nothing is shown then.

| Option | Sets | Next |
|---|---|---|
| No, I only use the tool | F_ROLE = use_only | Q_DATA |
| Yes, buying, licensing or contracting (including an RFP or a paid version) | F_ROLE = procure | Q_DATA |
| Yes, building, configuring, piloting or deploying, or developing with an outside partner | F_ROLE = build | Q_DATA |
| Both buying and building | F_ROLE = both | Q_DATA |
| Not sure | F_ROLE = not_sure | Q_DATA |

If “Not sure”: Treated as if you are both buying and building. To confirm, ask your agency: PS-23-001 (Policy, p.3) says “Agencies shall submit all software, applications, tools, and services utilizing AI for business operations to GTA for review prior to procurement.”

## Q_DATA: Will you type, paste or upload into the tool any information about identifiable people, health information, personal records, or confidential or private state information?

The documents speak of “Personally identifiable information (PII), protected health information (PHI), or other regulated data”, “confidential or private state information, or personal records”, and give “biometrics and financial data” as examples. They do not define these terms.

Fact: `F_DATA`

Asked only when: (F_TYPE is one of: generative, other, not_sure)

Not asked when the tool does not use AI: nothing is shown then.

| Option | Sets | Next |
|---|---|---|
| Yes | F_DATA = yes | Q_HOST |
| No, only publicly available or non-sensitive information | F_DATA = no | Q_HOST |
| Not sure | F_DATA = not_sure | Q_HOST |

If “Not sure”: Treated as if you will enter such information. To confirm: GS-25-001 (p.2) says employees “should first consult with their department's data privacy officer or designated compliance authority to clarify.”

## Q_HOST: Are you the host of the virtual meeting?

The host is the person running the meeting, who admits participants.

Fact: `F_HOST`

Asked only when: (F_TASK is one of: meetings, not_sure AND F_TYPE is one of: generative, not_sure)

Only the meeting-host element depends on this answer, and it requires the meetings task (or Not sure).

| Option | Sets | Next |
|---|---|---|
| Yes, I am the host | F_HOST = host | Q_DECISION |
| No, I am a participant | F_HOST = participant | Q_DECISION |
| Not sure | F_HOST = not_sure | Q_DECISION |

If “Not sure”: Treated as if you are the host. The documents name no contact for this; ask your agency.

## Q_DECISION: Will what the AI produces be used to make, or help make, a decision about a specific person?

Examples the documents name: hiring, legal, disciplinary or eligibility decisions, and assessing employee performance. SS-25-001 calls a use high-risk when it has “potential impact on legal rights, access to benefits, public safety, or public trust.”

Fact: `F_DECISION`

Asked only when: (F_TASK is one of: internal_summaries, research, public_comms, coding, data_analysis, chatbot_public, chatbot_internal, media, translation, legal, content, meetings, other AND F_TYPE is one of: generative, not_sure)

Skipped when the task is policy drafting, education and training, or Not sure: those answers already activate the decisions-about-people element and its pointer, which are all this question can affect.

| Option | Sets | Next |
|---|---|---|
| Yes | F_DECISION = yes | END |
| No | F_DECISION = no | END |
| Not sure | F_DECISION = not_sure | END |

If “Not sure”: Treated as if the output feeds a decision about a person. To confirm, ask your agency: SS-25-001 (3.0, p.6) says agencies should “consult with the Georgia Technology Authority (GTA) Office of Artificial Intelligence for novel, high-risk, or ambiguous use cases”.

# Outcomes

If 'scope_gate' matches, the outcome is only its 'outcome' text. Otherwise an outcome is the 'always' block, plus every block in 'blocks' and every pointer in 'conditional_pointers' whose 'when' condition matches the facts set on the path, plus the closing line. A 'when' condition is a list of alternatives; an alternative matches when every fact it names has one of the listed values. A fact that was not asked on the path matches nothing. When 'type_rule.when_other' matches, each element uses 'other_ai_statements' instead of 'statements' and each pointer uses 'other_ai_as_written' instead of 'as_written'; an element with no other_ai_statements, or a pointer whose other_ai_as_written is null, is not shown. Every 'type_notes' entry whose 'when' matches is shown before the results.

## Scope gate

Shown when: (F_TYPE is one of: none)

Every document in this set is about artificial intelligence, so none of their provisions apply to technology that does not use AI. This tool has no results for it.

The documents cite other GTA policies that are not in this set, including PM-04-001 and PS-08-005 (unresolved references UR02, UR03). This tool does not describe them.

Citations:
- Definition of 'Artificial Intelligence': Generative AI Responsible Use (SS-25-001), Terms and Definitions, p.1: “machine-based system that can, for a given set of human-defined objectives, make predictions, recommendations or decisions influencing real or virtual environments.”

## AI-type rule

When F_TYPE is 'other', a provision is shown only if it is in other_ai_reaches; an element or pointer with no such provision is not shown, and a statement shows only those provisions. For every other F_TYPE value all provisions are in scope. When F_TYPE is 'none', nothing is shown except not_ai_outcome.

## Note NOTE_OTHER_AI

Shown when: (F_TYPE is one of: other)

The two 2025 documents say they cover generative AI: SS-25-001 says “State government employees shall follow this standard when using commercial GenAI solutions” and GS-25-001 says “These guidelines apply to all forms of generative AI”. This result shows only provisions from the five documents that cover AI in general, plus one GS-25-001 provision that names “other automated decision-making systems”. Whether other provisions in the 2025 documents reach non-generative AI is open question OQ27. None of the seven documents mentions AI agents (OQ28). The documents define generative AI as “tools or systems used to create models that can generate new and original content, such as images, music, or text, based on patterns and examples from existing data”; if your agent creates content like that, choose Generative AI instead.

Citations:
- SS-25-001-STD-2: Generative AI Responsible Use (SS-25-001), Standard (opening paragraphs, before section 1), p.2
- GS-25-001-PURPOSE-2: Generative AI Guidelines for Responsible Use (GS-25-001), Purpose, p.1
- GS-25-001-SAFE-8: Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.2
- Definition of 'Generative AI (GenAI)': Generative AI Responsible Use (SS-25-001), Terms and Definitions, p.1: “tools or systems used to create models that can generate new and original content, such as images, music, or text, based on patterns and examples from existing data.”

## Outcome block: always shown (unless the scope gate matches)

### What these documents cover and who is to follow them (`U_SCOPE`)

**Modality: must** (as written: shall)

SS-25-001 says: “State government employees shall follow this standard when using commercial GenAI solutions such as OpenAI's ChatGPT, Google's Gemini, Anthropic's Claude, or Microsoft's Copilot.”

Citations:
- Generative AI Responsible Use (SS-25-001), Standard (opening paragraphs, before section 1), p.2

**Modality: informational** (as written: it is important to; none)

SS-25-001's requirements “apply to all GenAI systems and services used within the State of Georgia’s executive branch agencies”, GS-25-001's guidelines “apply to all forms of generative AI”, and SS-25-001's use-case table is a non-exhaustive set of examples.

Citations:
- Generative AI Responsible Use (SS-25-001), Purpose, p.1
- Generative AI Responsible Use (SS-25-001), Standard (opening paragraphs, before section 1), p.2
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (text above and below the table), p.6
- Generative AI Guidelines for Responsible Use (GS-25-001), Purpose, p.1
- Enterprise Artificial Intelligence Responsible Use (PS-23-001), Purpose, p.1
- Artificial Intelligence Responsible Use (SS-23-002), Purpose, p.1

On the 'other AI' branch, only:

- **informational**: PS-23-001 says: “This policy is designed to promote the acceptable use of AI tools, while also minimizing the potential for intentional or unintentional misuse, unethical outcomes, potential biases, use of sensitive data, and information security breaches.”; PS-23-001 says: “addresses the use of artificial intelligence tools in government operations, especially as it pertains to using sensitive data and state information within these tools”; SS-23-002 says: “It also delineates the protocols for the deployment of AI, Generative AI, Deep Learning, and Machine Learning tools within government services and operations, with special emphasis on their utilization in conjunction with sensitive data and state information.” (Enterprise Artificial Intelligence Responsible Use (PS-23-001), Purpose, p.1; Artificial Intelligence Responsible Use (SS-23-002), Purpose, p.1)

Conflicts and open questions affecting this element:
- Conflict C01: The 2025 generative AI document labels itself both a policy (PS-25-001) and a standard (SS-25-001); the documents do not settle which it is.
- Open question OQ01: Are the 2023 documents (PS-23-001, SS-23-002, GS-23-001) still in force alongside the 2025 documents for generative AI use, and which governs where they differ?
- Open question OQ02: Is 'Generative AI Responsible Use' a policy or a standard, and is its identifier PS-25-001 or SS-25-001?
- Open question OQ03: Do provisions addressed to 'Agencies' or written in the passive voice bind the individual employee?
- Open question OQ04: Who counts as a 'state employee', 'State government employee' or 'agency personnel', and does the 'Agency' definition limit which employees are covered?
- Open question OQ06: Convention used for provisions that have no modal verb; reviewer to confirm or re-map.
- Open question OQ27: Do provisions in SS-25-001 and GS-25-001 that say 'AI' rather than 'GenAI' reach non-generative AI?
- Open question OQ28: Is an AI agent 'Generative AI' under the documents' definition?
- Open question OQ29: Does PS-23-001 reach non-generative AI tools, given that its own definition of 'Artificial Intelligence' uses the generative-content wording?

### The 5 Guiding Principles (`U_PRINCIPLES`)

**Modality: should** (as written: should)

GS-25-001 says: “When engaging with generative AI, all state employees should abide by the 5 Guiding Principles” (Implement Responsible Systems; Ensure Ethical and Fair Use of Automated Decisions; Maintain Data Quality and Privacy; Keep AI Usage Transparent; Keep Human Involvement at the Center).

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Purpose, p.1

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Conflict C11: The 2023 guideline words some human-involvement principles with 'shall' or 'must'; the later wording of the same principles uses 'should'.
- Open question OQ05: What force do 'must', 'shall' and 'is required' carry inside documents labeled guidelines?
- Open question OQ14: Do the 5 Guiding Principles apply to an individual employee's routine use of a GenAI tool?
- Open question OQ15: Which version of the guiding principles is current?
- Open question OQ21: Are the guiding-principle items out of scope for an individual employee, or do they bind employees because GS-25-001 says employees 'should abide by' them?

### Use AI tools GTA has vetted (`U_APPROVED_TOOLS`)

**Modality: should** (as written: are encouraged to; should)

“State employees should only use AI which GTA has vetted, with pre-approved vendors”, and “Employees are encouraged to consult with GTA regularly for updates and to verify they are using compliant versions of AI tools.”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.1
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.2

**Modality: may** (as written: can be requested)

“Conditional Approval for specific use cases of GenAI tools can be requested via ai.georgia.gov or email ai@gta.georgia.gov.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (sentence below the table), p.8

**Modality: informational** (as written: none)

Approval of one version of an AI model “does not necessarily imply that other versions of that same model are also approved”, and “an approved AI model can always have its approval revoked”.

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.1
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.2

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Open question OQ07: May an employee use a free or individually obtained GenAI tool, and are ChatGPT, Gemini, Claude and Copilot approved?
- Open question OQ10: What is the status of the 'Conditional' column in the SS-25-001 use-case table, and when is 'Conditional Approval' needed?
- Open question OQ27: Do provisions in SS-25-001 and GS-25-001 that say 'AI' rather than 'GenAI' reach non-generative AI?

### Sign in with your state-issued account (`U_CREDENTIALS`)

**Modality: must** (as written: shall)

“All agency personnel shall use state-issued credentials (email and authentication accounts) when signing up for or using GenAI tools for state business.”

Citations:
- Generative AI Responsible Use (SS-25-001), 1.4 Approved Use of State Credentials, p.3

**Modality: must_not** (as written: is prohibited unless)

“The use of personal email addresses for such access is prohibited unless specifically authorized by the agency’s technology leadership.”

Citations:
- Generative AI Responsible Use (SS-25-001), 1.4 Approved Use of State Credentials, p.3

**Modality: should** (as written: avoid (imperative); imperative (no modal verb))

GS-25-001 gives these instructions without a modal verb: “avoid using personal accounts, such as personal email addresses, within any software”, “Keep personal and work materials separate”, and “create an account using your work email specifically for GenAI materials”.

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.2
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Strategies for Data Privacy and AI, p.4

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Conflict C05: SS-25-001 prohibits personal email addresses unless the agency's technology leadership authorizes it; GS-25-001 says to avoid personal accounts and states no exception.
- Open question OQ04: Who counts as a 'state employee', 'State government employee' or 'agency personnel', and does the 'Agency' definition limit which employees are covered?
- Open question OQ09: What do the undefined trigger terms mean: 'official capacity', 'moderate-risk use case', 'sensitive data', 'regulated data', 'confidential information', 'state business', 'significant incidents'?
- Open question OQ25: Should 'for state business' and 'used in any official capacity' be separate questions?
- Open question OQ27: Do provisions in SS-25-001 and GS-25-001 that say 'AI' rather than 'GenAI' reach non-generative AI?

### Review and verify what the AI produces (`U_REVIEW`)

**Modality: must** (as written: must (earlier in same sentence); shall)

“All GenAI-generated content—whether text, code, summaries, or other media—shall be reviewed and validated by qualified personnel before being used in any official capacity” (SS-25-001), and all AI-generated content must be “double-checked to ensure it is free of inaccurate information, AI hallucinations, or bias” (GS-25-001).

Citations:
- Generative AI Responsible Use (SS-25-001), 1. Human Review and Validation, p.2
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Do Not Put Private Data at Risk, p.4

**Modality: should** (as written: imperative (no modal verb); should)

“employees should apply careful review methods”; GS-25-001 also instructs, without a modal verb, “For any fact provided by an AI, find a reliable source that corroborates it”, “Carefully review AI-generated content for accuracy”, and “Cross-check information with reliable sources”.

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.2
- Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Rubric, p.10

**Modality: informational** (as written: none)

The reviews are “to detect inaccuracies, biases, or inappropriate content”, and review “includes cross-checking AI outputs with trusted sources, verifying the accuracy of information, and assessing for possible biases or inaccuracies”.

Citations:
- Generative AI Responsible Use (SS-25-001), 1. Human Review and Validation, p.2
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.2

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Conflict C13: SS-25-001 says review is by 'qualified personnel' before use 'in any official capacity'; SS-23-002 says agencies ensure review and approval 'by the business owner or designated personnel' before content is 'published or used for decision-making'.
- Open question OQ09: What do the undefined trigger terms mean: 'official capacity', 'moderate-risk use case', 'sensitive data', 'regulated data', 'confidential information', 'state business', 'significant incidents'?
- Open question OQ25: Should 'for state business' and 'used in any official capacity' be separate questions?
- Open question OQ27: Do provisions in SS-25-001 and GS-25-001 that say 'AI' rather than 'GenAI' reach non-generative AI?

### Keep a human in charge and use judgment (`U_HUMAN`)

**Modality: should** (as written: imperative (no modal verb); should; should never; should not)

AI tools “should not be the only agents involved in any decision-making” and “AI should never have autonomous decision-making capabilities”; “Employees should use common sense and exercise caution in deciding whether AI is right for a given task”; “Users should be aware of how AI contributes to outcomes and that humans remain responsible for those outcomes”; the rubric also instructs, without a modal verb, that a human review “both the inputs to and outputs from the AI”.

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.2
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.3
- Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Rubric, p.10
- Generative AI Guidelines for Responsible Use (GS-25-001), Guiding Principles > Keep Human Involvement at the Center, p.8
- 5 Guiding Principles (no identifier), Keep Human Involvement at the Center, p.9
- Artificial Intelligence Responsible Use Guidelines (GS-23-001), V. Keep Human Involvement at the Center > 7. User Education, p.8

On the 'other AI' branch, only:

- **should**: GS-25-001 says: “AI tools, including generative AI and other automated decision-making systems, should not be the only agents involved in any decision-making.”; 5 Guiding Principles says: “Users should be aware of how AI contributes to outcomes and that humans remain responsible for those outcomes.”; GS-23-001 says: “Users should be aware of how AI contributes to outcomes and that humans remain responsible for those outcomes.” (Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.2; 5 Guiding Principles (no identifier), Keep Human Involvement at the Center, p.9; Artificial Intelligence Responsible Use Guidelines (GS-23-001), V. Keep Human Involvement at the Center > 7. User Education, p.8)

Conflicts and open questions affecting this element:
- Open question OQ27: Do provisions in SS-25-001 and GS-25-001 that say 'AI' rather than 'GenAI' reach non-generative AI?
- Open question OQ28: Is an AI agent 'Generative AI' under the documents' definition?

### Label and cite AI-generated content (`U_LABEL`)

**Modality: must** (as written: must; shall)

“Any content generated or assisted by GenAI shall be clearly labeled” (SS-25-001), and “All AI-generated content – including text, images, videos, and audio – must be clearly labeled as AI-generated” (GS-25-001).

Citations:
- Generative AI Responsible Use (SS-25-001), 1.2 Disclosure and Attribution, p.3
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Do Not Put Private Data at Risk, p.4

**Modality: should** (as written: should)

“Anything produced with the assistance of AI should be cited correctly”, and “AI should be cited when its content is used as a product rather than a tool”.

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.2
- Generative AI Guidelines for Responsible Use (GS-25-001), How to Properly Cite AI-Generated Content, p.9

**Modality: informational** (as written: can; none)

“AI-generated content is considered a product when a substantial portion of the content is featured in the final product, even if the user extensively edits it.”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), How to Properly Cite AI-Generated Content, p.9

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Conflict C06: SS-25-001 says any content 'generated or assisted by GenAI shall be clearly labeled'; GS-25-001 says citation 'isn't necessary' when AI only helped you generate your own content and ideas, yet elsewhere asks you to cite brainstormed and edited content.
- Open question OQ05: What force do 'must', 'shall' and 'is required' carry inside documents labeled guidelines?
- Open question OQ11: Does the SS-25-001 attribution requirement (tool name, prompt summary, reviewer identity) apply to every labeled item, including internal and informal content?
- Open question OQ27: Do provisions in SS-25-001 and GS-25-001 that say 'AI' rather than 'GenAI' reach non-generative AI?

### Be open about your AI use (`U_TRANSPARENCY`)

**Modality: should** (as written: imperative (no modal verb); should)

“All state employees should be open and honest about their AI use” and “should rely on the honor system, openly disclosing AI usage without fear of severe repercussions”; GS-25-001 also instructs, without a modal verb, “Cite and acknowledge all AI-generated, brainstormed, or edited content” and “Clearly inform users when they are interacting with AI-generated content.”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.3
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Do Not Put Private Data at Risk, p.4
- Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Rubric, p.10

**Modality: informational** (as written: none)

“The goal of these guidelines is to reduce the risk of employees using Shadow AI.”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Do Not Put Private Data at Risk, p.4

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Conflict C06: SS-25-001 says any content 'generated or assisted by GenAI shall be clearly labeled'; GS-25-001 says citation 'isn't necessary' when AI only helped you generate your own content and ideas, yet elsewhere asks you to cite brainstormed and edited content.
- Open question OQ27: Do provisions in SS-25-001 and GS-25-001 that say 'AI' rather than 'GenAI' reach non-generative AI?

### Keep a record of prompts and responses (`U_RECORDS`)

**Modality: should** (as written: should)

“Employees should create a record of queries and responses outside of the generative AI software or platform for future reference.”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.2

**Modality: informational** (as written: may be subject to (statement of possibility, not a permission))

“GenAI-generated content used in official communications or policy-making may be subject to Georgia’s records retention schedules and open records laws.”

Citations:
- Generative AI Responsible Use (SS-25-001), 1.7 Records Management and Public Access Compliance, p.4

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Conflict C12: GS-25-001 mentions 'regularly clearing chats' while other provisions call for keeping records of prompts and responses; the documents do not say how these fit together.

### Protect data when you use AI tools (`U_DATA_CARE`)

**Modality: must** (as written: shall (in lead-in))

SS-25-001 says “The following safeguards shall be observed”, including “data minimization practices to avoid the inclusion of unnecessary sensitive information” and adherence to “encryption and access control requirements consistent with all applicable enterprise security policies and standards”.

Citations:
- Generative AI Responsible Use (SS-25-001), 1.3 Data Privacy and Confidentiality, p.3

**Modality: should** (as written: imperative (no modal verb))

GS-25-001 instructs, without a modal verb: “Opt out of data collection on any tool you use, particularly those involving pictures” and “Protect all data used by AI systems from unauthorized access or breaches.”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Strategies for Data Privacy and AI, p.4

**Modality: informational** (as written: none)

“Generative AI models use user-inputted information to further train their models”; protecting data “includes regularly changing passwords, minimizing data retention by regularly clearing chats, and conducting regular audits to ensure compliance”.

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.2
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Strategies for Data Privacy and AI, p.4

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Conflict C12: GS-25-001 mentions 'regularly clearing chats' while other provisions call for keeping records of prompts and responses; the documents do not say how these fit together.
- Open question OQ09: What do the undefined trigger terms mean: 'official capacity', 'moderate-risk use case', 'sensitive data', 'regulated data', 'confidential information', 'state business', 'significant incidents'?
- Open question OQ24: Should the data-entry prohibitions be shown to every employee rather than only to those who answer yes or not sure?
- Open question OQ27: Do provisions in SS-25-001 and GS-25-001 that say 'AI' rather than 'GenAI' reach non-generative AI?

### Stay within privacy and other laws (`U_LAWS`)

**Modality: must** (as written: must)

“The use of GenAI tools must be consistent with Georgia’s privacy laws, such as the Georgia Computer Data Privacy Act (GCDPA).”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Strategies for Data Privacy and AI, p.4

**Modality: should** (as written: imperative (no modal verb))

The rubric instructs, without a modal verb: “Ensure that all AI applications are fully compliant with relevant laws and regulations, both at the federal level, as well as those set forth by the State of Georgia.”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Rubric, p.10

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

### Watch for bias (`U_BIAS`)

**Modality: should** (as written: It is important to; imperative (no modal verb))

“It is important to be aware of these types of biases in any work produced by AI and screen the work for bias before putting them into use”; GS-25-001 also instructs, without a modal verb, to word questions carefully, to consider whether a question “presupposes things that are not necessarily true”, and to “consult a third party or non-AI source before proceeding”.

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Beware of Bias, p.5
- Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Rubric, p.10

**Modality: informational** (as written: can)

“Generative AI models can inadvertently perpetuate biases”.

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Beware of Bias, p.4

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Open question OQ27: Do provisions in SS-25-001 and GS-25-001 that say 'AI' rather than 'GenAI' reach non-generative AI?

### Training (`U_TRAINING`)

**Modality: must** (as written: shall; shall (in lead-in))

“All users of AI systems shall undergo appropriate training to ensure the responsible and ethical use of these tools”, including “Being familiarized with this AI Usage Policy and any other relevant policies, guidelines, and best practices” and “Participating in regular training sessions and workshops”.

Citations:
- Artificial Intelligence Responsible Use (SS-23-002), 7. Training and Awareness, p.10

Conflicts and open questions affecting this element:
- Open question OQ20: Does SS-23-002's training requirement apply before an employee may use a GenAI tool, and what training satisfies it?
- Open question OQ26: Is it acceptable that training (SS-23-002 section 7) is shown to every employee?

### What the documents say happens if they are not followed (`U_CONSEQUENCES`)

**Modality: informational** (as written: may result in (consequence); will be subject to (consequence))

“Failure to follow these requirements may result in revocation of tool access and additional oversight actions by GTA” (SS-25-001); “Any state employee, contractor, or vendor found to violate this standard will be subject to disciplinary action, including but not limited to, termination of employment, contract, or agreement” (SS-23-002).

Citations:
- Generative AI Responsible Use (SS-25-001), 1.7 Records Management and Public Access Compliance, p.4
- Artificial Intelligence Responsible Use (SS-23-002), 11. Violations, p.14

On the 'other AI' branch, only:

- **informational**: SS-23-002 says: “Any state employee, contractor, or vendor found to violate this standard will be subject to disciplinary action, including but not limited to, termination of employment, contract, or agreement.” [modal as written: will be subject to (consequence)] (Artificial Intelligence Responsible Use (SS-23-002), 11. Violations, p.14)

Conflicts and open questions affecting this element:
- Open question OQ18: What does 'these requirements' cover in the SS-25-001 enforcement sentence?

### Pointer `P_AGENCY_RESTRICTIONS`

As written: “Agencies shall implement additional restrictions based on their specific needs”

Check with your agency whether it has additional restrictions on GenAI use. The documents do not name an office.

On the 'other AI' branch: not shown.

Citations:
- Generative AI Responsible Use (SS-25-001), Standard (opening paragraphs, before section 1), p.2

Conflicts and open questions affecting this pointer:
- Open question OQ08: Does 'Agencies shall implement additional restrictions based on their specific needs' impose a duty or grant a permission?

### Pointer `P_ATTRIB_FORMAT`

As written: “Agencies must use standardized attribution formats that include:” “Name of the GenAI tool used”; “Summary of the prompt or task”; “Identity of the staff who reviewed or edited the content”.

Check with your agency for its standardized attribution format. The documents do not name an office.

On the 'other AI' branch: not shown.

Citations:
- Generative AI Responsible Use (SS-25-001), 1.2 Disclosure and Attribution, p.3

Conflicts and open questions affecting this pointer:
- Conflict C07: The two 2025 documents list different contents for an attribution: SS-25-001 lists tool name, prompt summary and reviewer identity; GS-25-001 lists model name, prompt, company and date.
- Open question OQ11: Does the SS-25-001 attribution requirement (tool name, prompt summary, reviewer identity) apply to every labeled item, including internal and informal content?

### Pointer `P_AGENCY_GUIDELINES`

As written: Agencies shall: “Ensure that AI-generated content is properly reviewed and approved by the business owner or designated personnel before it is published or used for decision-making.” and “Develop and implement guidelines for the responsible use of AI-generated outputs in different contexts and situations, tailored to the specific needs and requirements of the agency.”

Check with your agency for its own guidelines on using AI-generated outputs and for who reviews and approves AI-generated content (the standard says 'the business owner or designated personnel').

Citations:
- Artificial Intelligence Responsible Use (SS-23-002), 5. Ensuring Accuracy and Appropriateness of AI-generated Outputs, p.9

Conflicts and open questions affecting this pointer:
- Conflict C12: GS-25-001 mentions 'regularly clearing chats' while other provisions call for keeping records of prompts and responses; the documents do not say how these fit together.
- Conflict C13: SS-25-001 says review is by 'qualified personnel' before use 'in any official capacity'; SS-23-002 says agencies ensure review and approval 'by the business owner or designated personnel' before content is 'published or used for decision-making'.

### Pointer `P_RECORDS`

As written: Agencies shall: “Ensure proper classification and storage of GenAI outputs.”; “Retain audit trails of prompts, responses, and reviews”; “Prepare for potential public disclosure of GenAI-related records”. Agencies shall also be “Maintaining a record of AI tool usage, including the purpose, inputs, outputs, and any actions taken based on the AI-generated results.”

Check with your agency how it classifies, stores and retains GenAI prompts, responses and outputs. The documents do not name an office.

On the 'other AI' branch: SS-23-002 says: “To ensure that AI-generated outputs are accurate and appropriate, agencies shall:” … “Maintaining a record of AI tool usage, including the purpose, inputs, outputs, and any actions taken based on the AI-generated results.” [modal as written: shall (in lead-in)]

Citations:
- Generative AI Responsible Use (SS-25-001), 1.7 Records Management and Public Access Compliance, p.4
- Artificial Intelligence Responsible Use (SS-23-002), 5. Ensuring Accuracy and Appropriateness of AI-generated Outputs, p.9

Conflicts and open questions affecting this pointer:
- Conflict C12: GS-25-001 mentions 'regularly clearing chats' while other provisions call for keeping records of prompts and responses; the documents do not say how these fit together.
- Conflict C13: SS-25-001 says review is by 'qualified personnel' before use 'in any official capacity'; SS-23-002 says agencies ensure review and approval 'by the business owner or designated personnel' before content is 'published or used for decision-making'.

### Pointer `P_INCIDENTS`

As written: “Agencies shall report significant incidents involving GenAI to the GTA Office of AI within 48 hours.” “Agencies shall report the following suspected misuse of AI systems, whether intentional or unintentional, to the agency CIO or senior executive and GTA OIS.” Agencies' data protection duties include “Reporting any data breaches or incidents involving AI systems to the designated Data Protection Officer (DPO) or other appropriate person(s).”

These reporting duties are written for agencies; the documents do not say whom an individual employee notifies. Check with your agency how to raise an incident or suspected misuse.

On the 'other AI' branch: SS-23-002 says: “Agencies shall report the following suspected misuse of AI systems, whether intentional or unintentional, to the agency CIO or senior executive and GTA OIS.”; SS-23-002 says: “This includes:” … “Reporting any data breaches or incidents involving AI systems to the designated Data Protection Officer (DPO) or other appropriate person(s).” [modal as written: shall (in lead-in)]

Citations:
- Generative AI Responsible Use (SS-25-001), 4.0 Monitoring and Audit, p.8
- Artificial Intelligence Responsible Use (SS-23-002), 8. Reporting Misuse, p.10
- Artificial Intelligence Responsible Use (SS-23-002), 6. Data Protection, Safety and Privacy, p.10

Conflicts and open questions affecting this pointer:
- Conflict C04: The documents disagree on whether personal or sensitive data can ever be entered and who can approve it: GTA's Office of Artificial Intelligence (SS-25-001 1.3), an 'appropriate agency authority' (SS-23-002 6), the Georgia Technology Authority generally (GS-25-001 rubric), or no stated exception (other GS-25-001 passages and the SS-25-001 table).
- Conflict C10: Incident and misuse reports go to different recipients in different documents, and only SS-25-001 sets a deadline (48 hours).
- Open question OQ19: Does the employee have a personal duty to report incidents or misuse, and to whom?

### Pointer `P_COMPLIANCE_CONTACT`

As written: “Each agency shall designate a staff member who shall be responsible for ensuring full compliance with this Standard and the requirements set forth herein.”

Your agency is to have a staff member designated for compliance with SS-23-002. The documents do not say who that is in your agency.

Citations:
- Artificial Intelligence Responsible Use (SS-23-002), 8. Reporting Misuse, p.10

Conflicts and open questions affecting this pointer:
- Conflict C10: Incident and misuse reports go to different recipients in different documents, and only SS-25-001 sets a deadline (48 hours).
- Open question OQ19: Does the employee have a personal duty to report incidents or misuse, and to whom?

## Outcome block: OUT_C_DATA

Shown when: (F_DATA is one of: yes, not_sure)

### Entering personal, sensitive or confidential information (`C_DATA`)

**Modality: must_not** (as written: Do not (imperative); do not (imperative); shall not)

“Personally identifiable information (PII), protected health information (PHI), or other regulated data shall not be used as inputs to GenAI tools unless formally approved by the GTA’s Office of Artificial Intelligence” (SS-25-001); GS-25-001 says “do not provide them with confidential or private state information, or personal records” and “Do not enter personal and/or sensitive data into a GenAI model.”

Citations:
- Generative AI Responsible Use (SS-25-001), 1.3 Data Privacy and Confidentiality, p.3
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.2
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Strategies for Data Privacy and AI, p.4

**Modality: should** (as written: Always verify (imperative); imperative (no modal verb))

The GS-25-001 rubric instructs, without a modal verb: “Always verify that the AI is not handling sensitive or private information, unless given explicit approval from the Georgia Technology Authority. In such cases, ensure that strict data protection protocols are being consistently enforced.”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Rubric, p.10

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Conflict C04: The documents disagree on whether personal or sensitive data can ever be entered and who can approve it: GTA's Office of Artificial Intelligence (SS-25-001 1.3), an 'appropriate agency authority' (SS-23-002 6), the Georgia Technology Authority generally (GS-25-001 rubric), or no stated exception (other GS-25-001 passages and the SS-25-001 table).
- Open question OQ09: What do the undefined trigger terms mean: 'official capacity', 'moderate-risk use case', 'sensitive data', 'regulated data', 'confidential information', 'state business', 'significant incidents'?
- Open question OQ24: Should the data-entry prohibitions be shown to every employee rather than only to those who answer yes or not sure?
- Open question OQ27: Do provisions in SS-25-001 and GS-25-001 that say 'AI' rather than 'GenAI' reach non-generative AI?

## Outcome block: OUT_C_DATA_UNSURE

Shown when: (F_DATA is one of: not_sure)

### When you are not sure whether data may be entered (`C_DATA_UNSURE`)

**Modality: should** (as written: it is better to ... avoid; should)

“If employees are uncertain whether specific data should be entered into a generative AI tool, they should first consult with their department's data privacy officer or designated compliance authority to clarify”; “it is better to err on the side of caution and avoid inputting potentially sensitive information without approval”.

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.2

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Conflict C04: The documents disagree on whether personal or sensitive data can ever be entered and who can approve it: GTA's Office of Artificial Intelligence (SS-25-001 1.3), an 'appropriate agency authority' (SS-23-002 6), the Georgia Technology Authority generally (GS-25-001 rubric), or no stated exception (other GS-25-001 passages and the SS-25-001 table).
- Open question OQ09: What do the undefined trigger terms mean: 'official capacity', 'moderate-risk use case', 'sensitive data', 'regulated data', 'confidential information', 'state business', 'significant incidents'?

## Outcome block: OUT_C_DECISIONS

Shown when: (F_DECISION is one of: yes, not_sure) OR (F_TASK is one of: policy_drafting, education_training, not_sure)

### Decisions about people (`C_DECISIONS`)

**Modality: must_not** (as written: 'Do not' / 'Don’t' under column heading 'Prohibited' (legend: Red = Prohibited); may not)

The same example says “it may not use AI to scan and reject resumes automatically”; the SS-25-001 table lists as prohibited “Do not use GenAI to make legal, disciplinary, or eligibility decisions” and “Do not use GenAI to assess employee performance or give personalized advice.”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.2
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.7

**Modality: may** (as written: may)

GS-25-001 gives this example: “an HR department may consult with AI platforms in making hiring decisions”.

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.2

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Open question OQ10: What is the status of the 'Conditional' column in the SS-25-001 use-case table, and when is 'Conditional Approval' needed?
- Open question OQ13: How do the hiring example and the decision prohibitions fit together?
- Open question OQ23: Is one task per run acceptable, and are prohibitions that sit in one table row limited to that row?
- Open question OQ27: Do provisions in SS-25-001 and GS-25-001 that say 'AI' rather than 'GenAI' reach non-generative AI?

## Outcome block: OUT_C_CITE_NONE

Shown when: (F_PRODUCT is one of: none)

### No citation when AI only helped you develop your own content (`C_CITE_NONE`)

**Modality: may** (as written: isn’t necessary)

GS-25-001 says “if the AI model helps a user in generating their own content and ideas, citation isn’t necessary”.

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), How to Properly Cite AI-Generated Content, p.9

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Conflict C06: SS-25-001 says any content 'generated or assisted by GenAI shall be clearly labeled'; GS-25-001 says citation 'isn't necessary' when AI only helped you generate your own content and ideas, yet elsewhere asks you to cite brainstormed and edited content.

## Outcome block: OUT_C_CITE_REQUIRED

Shown when: (F_PRODUCT is one of: informal, official, not_sure)

### Citation when AI content appears in the final product (`C_CITE_REQUIRED`)

**Modality: must** (as written: is required)

GS-25-001 says “if the AI model’s content or ideas appear in the final product, a citation is required”.

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), How to Properly Cite AI-Generated Content, p.9

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Conflict C06: SS-25-001 says any content 'generated or assisted by GenAI shall be clearly labeled'; GS-25-001 says citation 'isn't necessary' when AI only helped you generate your own content and ideas, yet elsewhere asks you to cite brainstormed and edited content.
- Open question OQ05: What force do 'must', 'shall' and 'is required' carry inside documents labeled guidelines?

## Outcome block: OUT_C_CITE_INFORMAL

Shown when: (F_PRODUCT is one of: informal)

### How to cite in an informal document (`C_CITE_INFORMAL`)

**Modality: must** (as written: all that is necessary is)

For “an informal document like an email”, GS-25-001 says “all that is necessary is to acknowledge somewhere in the text that AI was used in its development and which AI model was used”.

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), How to Properly Cite AI-Generated Content, p.9

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Conflict C07: The two 2025 documents list different contents for an attribution: SS-25-001 lists tool name, prompt summary and reviewer identity; GS-25-001 lists model name, prompt, company and date.
- Open question OQ05: What force do 'must', 'shall' and 'is required' carry inside documents labeled guidelines?

## Outcome block: OUT_C_CITE_OFFICIAL

Shown when: (F_PRODUCT is one of: official, not_sure)

### How to cite in a more official document (`C_CITE_OFFICIAL`)

**Modality: must** (as written: it is necessary to)

GS-25-001 says “on more official documents, it is necessary to use a more detailed citation”.

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), How to Properly Cite AI-Generated Content, p.9

**Modality: should** (as written: Be sure to (imperative))

GS-25-001 instructs, without a modal verb: “Be sure to include the name of the AI model, the name of the prompt used, the company to which the AI model belongs, and the date that the content was generated.”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), How to Properly Cite AI-Generated Content, p.10

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Conflict C07: The two 2025 documents list different contents for an attribution: SS-25-001 lists tool name, prompt summary and reviewer identity; GS-25-001 lists model name, prompt, company and date.
- Open question OQ05: What force do 'must', 'shall' and 'is required' carry inside documents labeled guidelines?
- Open question OQ16: Is text missing from GS-25-001 page 9?

## Outcome block: OUT_C_TASK_SUMMARY

Shown when: (F_TASK is one of: internal_summaries, not_sure)

### Task: summarizing or drafting internal documents (`C_TASK_SUMMARY`)

**Modality: must** (as written: imperative under column heading 'Conditional' (legend: Yellow = Caution))

SS-25-001 table, Conditional (Yellow = Caution): “Use GenAI-generated summaries only after review by staff.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.6

**Modality: must_not** (as written: 'Do not' / 'Don’t' under column heading 'Prohibited' (legend: Red = Prohibited); listed under 'Prohibited:')

SS-25-001 table, Prohibited (Red = Prohibited): “Do not share unreviewed summaries as official records or public communications.” GS-25-001, listed as Prohibited: “Summarizing sensitive government documents and personal private information, such as biometrics and financial data.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.6
- Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Task-Specific > Information Processing, p.11

**Modality: may** (as written: imperative under column heading 'Acceptable' (legend: Green = Approved); listed under 'Permissible:')

SS-25-001 table, Acceptable (Green = Approved): “Use GenAI to summarize meeting notes or internal memos with attribution.” GS-25-001, listed as Permissible: “Summarizing publicly available information (e.g., news and research journal articles).”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.6
- Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Task-Specific > Information Processing, p.11

**Modality: informational** (as written: none)

GS-25-001, question to consider: “Does the data include sensitive information?” GS-25-001, question to consider: “Is all the information in the summary accurate?” GS-25-001, question to consider: “How could this summary be biased?”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Task-Specific > Information Processing, p.11

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Open question OQ10: What is the status of the 'Conditional' column in the SS-25-001 use-case table, and when is 'Conditional Approval' needed?
- Open question OQ12: How do the meeting provisions fit with the 'Drafting internal summaries' row?

## Outcome block: OUT_C_TASK_RESEARCH

Shown when: (F_TASK is one of: research, not_sure)

### Task: looking up or gathering information (`C_TASK_RESEARCH`)

**Modality: must_not** (as written: listed under 'Prohibited:')

GS-25-001, listed as Prohibited: “Relying solely on an LLM and failing to verify your findings with other sources.”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Task-Specific > Information Gathering, p.11

**Modality: may** (as written: listed under 'Permissible:')

GS-25-001, listed as Permissible: “Using an LLM to provide you with basic information on a topic.”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Task-Specific > Information Gathering, p.11

**Modality: informational** (as written: none)

GS-25-001, question to consider: “Does the data include sensitive information?” GS-25-001, question to consider: “Is all the information in the summary accurate?” GS-25-001, question to consider: “How could this summary be wrong?”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Task-Specific > Information Gathering, p.11

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

## Outcome block: OUT_C_TASK_PUBLIC

Shown when: (F_TASK is one of: public_comms, chatbot_public, not_sure)

### Task: public-facing communications (`C_TASK_PUBLIC`)

**Modality: must** (as written: imperative under column heading 'Conditional' (legend: Yellow = Caution))

SS-25-001 table, Conditional (Yellow = Caution): “Deploy public chatbots with GenAI only after bias/safety review.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.6

**Modality: must_not** (as written: 'Do not' / 'Don’t' under column heading 'Prohibited' (legend: Red = Prohibited))

SS-25-001 table, Prohibited (Red = Prohibited): “Do not allow GenAI to autonomously publish content to websites, emails, or social media.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.6

**Modality: may** (as written: imperative under column heading 'Acceptable' (legend: Green = Approved))

SS-25-001 table, Acceptable (Green = Approved): “Use GenAI to draft first-pass content, reviewed and edited by staff.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.6

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Open question OQ10: What is the status of the 'Conditional' column in the SS-25-001 use-case table, and when is 'Conditional Approval' needed?

## Outcome block: OUT_C_TASK_CODING

Shown when: (F_TASK is one of: coding, not_sure)

### Task: coding and software development (`C_TASK_CODING`)

**Modality: must** (as written: imperative under column heading 'Conditional' (legend: Yellow = Caution))

SS-25-001 table, Conditional (Yellow = Caution): “Use in sandbox/test environments and validate security of outputs.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.7

**Modality: must_not** (as written: 'Do not' / 'Don’t' under column heading 'Prohibited' (legend: Red = Prohibited); listed under 'Prohibited:')

SS-25-001 table, Prohibited (Red = Prohibited): “Do not deploy unreviewed GenAI-generated code to production systems.” GS-25-001, listed as Prohibited: “Deploying AI-generated code without human validation/oversight.” GS-25-001, listed as Prohibited: “Generating code that violates Georgia’s AI ethics standards.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.7
- Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Task-Specific > Coding/Interpreting Software, p.11

**Modality: may** (as written: imperative under column heading 'Acceptable' (legend: Green = Approved); listed under 'Permissible:')

SS-25-001 table, Acceptable (Green = Approved): “Use GenAI for code suggestions, bug spotting, documentation.” GS-25-001, listed as Permissible: “Generating documentation and/or comments for existing software code.” GS-25-001, listed as Permissible: “Debugging existing software code.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.7
- Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Task-Specific > Coding/Interpreting Software, p.11

**Modality: informational** (as written: none)

GS-25-001, question to consider: “Is GenAI being used to code entire scripts autonomously?” GS-25-001, question to consider: “Is the generated code thoroughly reviewed by a human?” GS-25-001, question to consider: “Does the software application deal with any sensitive information?”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Task-Specific > Coding/Interpreting Software, p.11

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Open question OQ10: What is the status of the 'Conditional' column in the SS-25-001 use-case table, and when is 'Conditional Approval' needed?

## Outcome block: OUT_C_TASK_DATA_ANALYSIS

Shown when: (F_TASK is one of: data_analysis, not_sure)

### Task: data analysis and reports (`C_TASK_DATA_ANALYSIS`)

**Modality: must** (as written: imperative under column heading 'Conditional' (legend: Yellow = Caution))

SS-25-001 table, Conditional (Yellow = Caution): “Cross-validate with source data and check for misinterpretation.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.7

**Modality: must_not** (as written: 'Do not' / 'Don’t' under column heading 'Prohibited' (legend: Red = Prohibited))

SS-25-001 table, Prohibited (Red = Prohibited): “Don’t use GenAI to analyze or process personally identifiable or regulated data.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.7

**Modality: may** (as written: imperative under column heading 'Acceptable' (legend: Green = Approved))

SS-25-001 table, Acceptable (Green = Approved): “Use GenAI to visualize trends or automate draft insights from open data.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.7

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Conflict C04: The documents disagree on whether personal or sensitive data can ever be entered and who can approve it: GTA's Office of Artificial Intelligence (SS-25-001 1.3), an 'appropriate agency authority' (SS-23-002 6), the Georgia Technology Authority generally (GS-25-001 rubric), or no stated exception (other GS-25-001 passages and the SS-25-001 table).
- Open question OQ10: What is the status of the 'Conditional' column in the SS-25-001 use-case table, and when is 'Conditional Approval' needed?
- Open question OQ23: Is one task per run acceptable, and are prohibitions that sit in one table row limited to that row?

## Outcome block: OUT_C_TASK_POLICY

Shown when: (F_TASK is one of: policy_drafting, not_sure)

### Task: policy drafting support (`C_TASK_POLICY`)

**Modality: must** (as written: imperative under column heading 'Conditional' (legend: Yellow = Caution))

SS-25-001 table, Conditional (Yellow = Caution): “Review all content for tone, bias, and policy implications before sharing.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.7

**Modality: may** (as written: imperative under column heading 'Acceptable' (legend: Green = Approved))

SS-25-001 table, Acceptable (Green = Approved): “Use GenAI to brainstorm policy language or summarize research.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.7

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Open question OQ10: What is the status of the 'Conditional' column in the SS-25-001 use-case table, and when is 'Conditional Approval' needed?
- Open question OQ23: Is one task per run acceptable, and are prohibitions that sit in one table row limited to that row?

## Outcome block: OUT_C_TASK_EDU

Shown when: (F_TASK is one of: education_training, not_sure)

### Task: education and training materials (`C_TASK_EDU`)

**Modality: must** (as written: imperative under column heading 'Conditional' (legend: Yellow = Caution))

SS-25-001 table, Conditional (Yellow = Caution): “Vet any public-facing content for bias and misinformation.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.7

**Modality: may** (as written: imperative under column heading 'Acceptable' (legend: Green = Approved))

SS-25-001 table, Acceptable (Green = Approved): “Use GenAI to create quiz questions, flashcards, or explainers for internal use.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.7

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Open question OQ10: What is the status of the 'Conditional' column in the SS-25-001 use-case table, and when is 'Conditional Approval' needed?
- Open question OQ23: Is one task per run acceptable, and are prohibitions that sit in one table row limited to that row?

## Outcome block: OUT_C_TASK_CHATBOT

Shown when: (F_TASK is one of: chatbot_public, chatbot_internal, not_sure)

### Task: chatbots and user interaction (`C_TASK_CHATBOT`)

**Modality: must** (as written: imperative under column heading 'Conditional' (legend: Yellow = Caution))

SS-25-001 table, Conditional (Yellow = Caution): “Provide escalation path to human assistance and monitor performance.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.7

**Modality: must_not** (as written: 'Do not' / 'Don’t' under column heading 'Prohibited' (legend: Red = Prohibited); listed under 'Prohibited:')

SS-25-001 table, Prohibited (Red = Prohibited): “Don’t allow GenAI chatbots to answer legal, medical, or emergency questions.” GS-25-001, listed as Prohibited: “Storing information from user interactions with GenAI without explicit consent from the user.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.7
- Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Task-Specific > User Interaction, p.12

**Modality: should** (as written: imperative (no modal verb))

GS-25-001: “For applications requiring users’ data, ensure that such data is only used with user consent.”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Use AI Tools Safely and Properly, p.3

**Modality: may** (as written: imperative under column heading 'Acceptable' (legend: Green = Approved); listed under 'Permissible:')

SS-25-001 table, Acceptable (Green = Approved): “Use GenAI to support FAQ responses clearly marked as AI-generated.” GS-25-001, listed as Permissible: “Creating chatbots to streamline user support.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.7
- Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Task-Specific > User Interaction, p.12

**Modality: informational** (as written: none)

GS-25-001, question to consider: “Are users aware that they are interacting with AI-generated content?” GS-25-001, question to consider: “Does the AI application require sensitive or private user information?” GS-25-001, question to consider: “Is that information stored, or is it promptly deleted following the interaction?”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Task-Specific > User Interaction, p.12

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Open question OQ10: What is the status of the 'Conditional' column in the SS-25-001 use-case table, and when is 'Conditional Approval' needed?
- Open question OQ30: Does the SS-25-001 'Constituent service' row apply to chatbots used only by state staff?

## Outcome block: OUT_C_TASK_MEDIA

Shown when: (F_TASK is one of: media, not_sure)

### Task: image, audio or video generation (`C_TASK_MEDIA`)

**Modality: must** (as written: imperative under column heading 'Conditional' (legend: Yellow = Caution); must)

SS-25-001 table, Conditional (Yellow = Caution): “Clearly disclose synthetic content when used in public contexts.” GS-25-001: “Photos and videos must have a clear watermark indicating that the following content was generated by AI.” GS-25-001: “Any audio including AI-generated sound must include an audio disclaimer notifying listeners that some or all of the recording was generated with AI.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.7
- Generative AI Guidelines for Responsible Use (GS-25-001), How to Properly Cite AI-Generated Content, p.10

**Modality: must_not** (as written: 'Do not' / 'Don’t' under column heading 'Prohibited' (legend: Red = Prohibited))

SS-25-001 table, Prohibited (Red = Prohibited): “Do not use GenAI to create deepfakes, impersonations, or sensitive likenesses.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.7

**Modality: may** (as written: imperative under column heading 'Acceptable' (legend: Green = Approved))

SS-25-001 table, Acceptable (Green = Approved): “Use for creative brainstorming, mockups, training materials (with proper attribution).”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.7

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Open question OQ05: What force do 'must', 'shall' and 'is required' carry inside documents labeled guidelines?
- Open question OQ10: What is the status of the 'Conditional' column in the SS-25-001 use-case table, and when is 'Conditional Approval' needed?

## Outcome block: OUT_C_TASK_TRANSLATION

Shown when: (F_TASK is one of: translation, not_sure)

### Task: translation and accessibility (`C_TASK_TRANSLATION`)

**Modality: must** (as written: imperative under column heading 'Conditional' (legend: Yellow = Caution))

SS-25-001 table, Conditional (Yellow = Caution): “Confirm with human review, especially for formal or legal documents.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.8

**Modality: must_not** (as written: 'Do not' / 'Don’t' under column heading 'Prohibited' (legend: Red = Prohibited))

SS-25-001 table, Prohibited (Red = Prohibited): “Do not rely on GenAI alone for accessibility compliance or legal document translations.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.8

**Modality: may** (as written: imperative under column heading 'Acceptable' (legend: Green = Approved))

SS-25-001 table, Acceptable (Green = Approved): “Use GenAI to provide draft translations or captioning to improve access.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.8

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Open question OQ10: What is the status of the 'Conditional' column in the SS-25-001 use-case table, and when is 'Conditional Approval' needed?

## Outcome block: OUT_C_TASK_LEGAL

Shown when: (F_TASK is one of: legal, not_sure)

### Task: legal and regulatory analysis (`C_TASK_LEGAL`)

**Modality: must** (as written: imperative under column heading 'Conditional' (legend: Yellow = Caution))

SS-25-001 table, Conditional (Yellow = Caution): “Use with legal staff oversight only.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.8

**Modality: must_not** (as written: 'Do not' / 'Don’t' under column heading 'Prohibited' (legend: Red = Prohibited))

SS-25-001 table, Prohibited (Red = Prohibited): “Do not use GenAI to provide legal advice or determine compliance status.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.8

**Modality: may** (as written: imperative under column heading 'Acceptable' (legend: Green = Approved))

SS-25-001 table, Acceptable (Green = Approved): “Use GenAI to organize and summarize non-sensitive legal text for research.”

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), p.8

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Open question OQ10: What is the status of the 'Conditional' column in the SS-25-001 use-case table, and when is 'Conditional Approval' needed?

## Outcome block: OUT_C_TASK_CONTENT

Shown when: (F_TASK is one of: content, not_sure)

### Task: brainstorming, editing and other content generation (`C_TASK_CONTENT`)

**Modality: must_not** (as written: listed under 'Prohibited:')

GS-25-001, listed as Prohibited: “Generating content that replicates or closely mimics copyrighted material.”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Task-Specific > Content Generation, p.12

**Modality: may** (as written: listed under 'Permissible:')

GS-25-001, listed as Permissible: “Brainstorming a list of ideas.” GS-25-001, listed as Permissible: “Checking for grammatical errors and/or formatting a human-written document that does not include sensitive information.”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Task-Specific > Content Generation, p.12

**Modality: informational** (as written: none)

GS-25-001, question to consider: “Did the GenAI “hallucinate” or create other false information?” GS-25-001, question to consider: “Is the content plagiarized or involved in any form of copyright infringement?”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Task-Specific > Content Generation, p.12

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

## Outcome block: OUT_C_MEETINGS

Shown when: (F_TASK is one of: meetings, not_sure)

### AI in virtual meetings (`C_MEETINGS`)

**Modality: should** (as written: imperative (no modal verb); is strongly discouraged; should; should not)

“The use of AI note-taking tools in Microsoft Teams meetings or any other conferencing platforms is strongly discouraged for meetings held within the State”; AI recording and transcription “should be used thoughtfully”, “AI should not be used to manipulate or misrepresent the contributions of participants”, and “AI outputs should be used only to supplement, not replace, human judgment.”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Be Vigilant in Virtual Meetings, p.3

**Modality: informational** (as written: none)

“Once created, meeting recordings and transcriptions become public records and are subject to retention rules.”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Be Vigilant in Virtual Meetings, p.3

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Open question OQ12: How do the meeting provisions fit with the 'Drafting internal summaries' row?

## Outcome block: OUT_C_MEETING_HOST

Shown when: (F_TASK is one of: meetings, not_sure AND F_HOST is one of: host, not_sure)

### If you host the meeting (`C_MEETING_HOST`)

**Modality: must** (as written: are responsible for)

GS-25-001 says, without a modal verb: “Meeting hosts are responsible for determining the need for recordings and automated transcriptions and keeping any records created.”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Be Vigilant in Virtual Meetings, p.3

**Modality: should** (as written: should)

“Meeting hosts should be diligent when admitting participants to virtual meetings to ensure no AI bot note-takers join.”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Be Vigilant in Virtual Meetings, p.3

**Modality: may** (as written: may)

“Meeting hosts may opt to use the recording and transcription services built into Teams.”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Be Vigilant in Virtual Meetings, p.3

**Modality: informational** (as written: can)

“You can look for the “.ai” suffix to confirm.”

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Be Vigilant in Virtual Meetings, p.3

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Open question OQ12: How do the meeting provisions fit with the 'Drafting internal summaries' row?

## Outcome block: OUT_C_PROCURE_APPROVAL

Shown when: (F_ROLE is one of: procure, both, not_sure)

### GTA approval before procuring a GenAI product or service (`C_PROCURE_APPROVAL`)

**Modality: must** (as written: must (in lead-in))

“Any procurement of GenAI products or services must” be “approved in advance by the Georgia Technology Authority (GTA) by completing the review form at https://ai.georgia.gov/ai-application-and-tool-request-form”, comply “with GTA’s IT security, privacy, and accessibility standards”, and include “provisions for auditability, explainability, model documentation, data retention, and intellectual property rights in contracts”.

Citations:
- Generative AI Responsible Use (SS-25-001), 1.5 Procurement and Third-Party Vendor Compliance, p.3
- Generative AI Responsible Use (SS-25-001), 1.5 Procurement and Third-Party Vendor Compliance, p.4

On the 'other AI' branch: not shown (no provision reaches non-generative AI under ai_type_rule).

Conflicts and open questions affecting this element:
- Conflict C08: Pre-procurement review is described three ways: a web form at ai.georgia.gov (SS-25-001), a Business Solutions Review form sent by email (SS-23-002), and submission to GTA with no channel named (PS-23-001).
- Open question OQ07: May an employee use a free or individually obtained GenAI tool, and are ChatGPT, Gemini, Claude and Copilot approved?
- Open question OQ29: Does PS-23-001 reach non-generative AI tools, given that its own definition of 'Artificial Intelligence' uses the generative-content wording?

## Outcome block: OUT_C_PROC_PRINCIPLES

Shown when: (F_ROLE is one of: procure, both, not_sure)

### Procurement of AI tools: key principles (`C_PROC_PRINCIPLES`)

**Modality: should** (as written: imperative (no modal verb))

GS-25-002's key principles are instructions written without modal verbs, for example “Prioritize data assessment and governance before procurement”, “Emphasize the problem, not a specific solution”, “Establish robust oversight mechanisms”, and “Plan for ongoing evaluation, maintenance, training, and knowledge transfer throughout the AI system's lifecycle.”

Citations:
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines > Key Principles, p.1

**Modality: informational** (as written: none)

“These guidelines outline best practices for state agencies when preparing and evaluating Requests for Proposals (RFPs) or other procurements for AI tools or solutions that include AI features.”

Citations:
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Purpose, p.1

Conflicts and open questions affecting this element:
- Open question OQ22: Should the procurement guideline (GS-25-002) be shown to an employee who works on an AI procurement?

## Outcome block: OUT_C_PROC_PREP

Shown when: (F_ROLE is one of: procure, both, not_sure)

### Procurement of AI tools: preparing the RFP (`C_PROC_PREP`)

**Modality: should** (as written: Specify that ... must (imperative to the drafter; 'must' describes the RFP term); imperative (no modal verb); should)

GS-25-002 lists twelve topics of instructions for preparing the RFP (objectives and scope; ethics and fairness; transparency and explainability; data privacy and security; performance and accountability; open standards; workforce change management and training; continuous monitoring; ethical AI governance; algorithmic impact assessment; collaboration; referrals), written without modal verbs except where it says the vendor or the assessment “should” do something; read the cited section for each item.

Citations:
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Preparing the RFP > 1. Define Objectives and Scope, p.2
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Preparing the RFP > 2. Ethical and Fairness Considerations, p.2
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Preparing the RFP > 3. Transparency and Explainability, p.2
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Preparing the RFP > 4. Data Privacy and Security, p.2
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Preparing the RFP > 4. Data Privacy and Security, p.3
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Preparing the RFP > 5. Performance and Accountability, p.3
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Preparing the RFP > 6. Open Standards and Interoperability, p.3
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Preparing the RFP > 7. Workforce Change Management and Training, p.3
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Preparing the RFP > 8. Continuous Monitoring and Feedback Loops, p.3
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Preparing the RFP > 9. Ethical AI Governance, p.3
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Preparing the RFP > 10. Algorithmic Impact Assessment, p.4
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Preparing the RFP > 11. Collaboration and Knowledge Sharing, p.4
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Preparing the RFP > 12. Referrals and Production-Facing Examples of Work, p.4

Conflicts and open questions affecting this element:
- Open question OQ22: Should the procurement guideline (GS-25-002) be shown to an employee who works on an AI procurement?

## Outcome block: OUT_C_PROC_EVAL

Shown when: (F_ROLE is one of: procure, both, not_sure)

### Procurement of AI tools: evaluating RFP responses (`C_PROC_EVAL`)

**Modality: should** (as written: imperative (no modal verb); should)

GS-25-002 lists thirteen topics of instructions for evaluating RFP responses, from “Establish a diverse evaluation committee with expertise in AI, ethics, and procurement” to “Where feasible, require a pilot phase before full deployment”, written without modal verbs except “Both training and technical documentation should be provided”; read the cited section for each item.

Citations:
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Evaluating RFP Responses > 1. Fair and Objective Evaluation Process, p.4
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Evaluating RFP Responses > 2. Assessing Bias Mitigation Strategies, p.4
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Evaluating RFP Responses > 3. Examining Transparency and Explainability, p.5
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Evaluating RFP Responses > 4. Reviewing Data Security and Privacy Protections, p.5
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Evaluating RFP Responses > 5. Evaluating Performance and Accountability Measures, p.5
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Evaluating RFP Responses > 6. Ensuring Compliance with Ethical and Legal Standards, p.5
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Evaluating RFP Responses > 7. Evaluating Workforce Change Management and Training Plans, p.5
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Evaluating RFP Responses > 8. Evaluating Continuous Monitoring and Feedback Loops, p.5
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Evaluating RFP Responses > 9. Evaluating Ethical AI Governance, p.5
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Evaluating RFP Responses > 10. Evaluating Algorithmic Impact Assessments, p.5
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Evaluating RFP Responses > 11. Evaluating Collaboration and Knowledge Sharing, p.6
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Evaluating RFP Responses > 12. Evaluating Referrals or Similar Work Product, p.6
- Procurement of AI tools Guidelines for Responsible Use (GS-25-002), Guidelines for Evaluating RFP Responses > 13. Conducting a Pilot or Trial Implementation, p.6

Conflicts and open questions affecting this element:
- Open question OQ22: Should the procurement guideline (GS-25-002) be shown to an employee who works on an AI procurement?

## Outcome block: OUT_C_DEVELOP

Shown when: (F_ROLE is one of: build, both, not_sure)

### Developing AI tools or working with external collaborators (`C_DEVELOP`)

**Modality: must** (as written: must; shall)

“When developing AI tools or engaging with external collaborators, the following guidelines shall be adhered to”, including that “Collaboration agreements must clearly disclose the manner and use of AI technology”, “AI development shall prioritize safety, privacy, and ethical considerations”, “Prior to deployment, AI systems shall undergo rigorous testing”, and risks or ethical concerns “shall be reported to the agency’s designated Ethics Officer, CIO, and State CIO”.

Citations:
- Artificial Intelligence Responsible Use (SS-23-002), 9. AI Development and External Collaboration, p.12
- Artificial Intelligence Responsible Use (SS-23-002), 9. AI Development and External Collaboration, p.13

**Modality: should** (as written: should)

Collaboration agreements “should also address ownership and usage rights of AI models and data.”

Citations:
- Artificial Intelligence Responsible Use (SS-23-002), 9. AI Development and External Collaboration, p.12

Conflicts and open questions affecting this element:
- Conflict C10: Incident and misuse reports go to different recipients in different documents, and only SS-25-001 sets a deadline (48 hours).

## Outcome block: OUT_P_DATA_AUTHORITY

Shown when: (F_DATA is one of: yes, not_sure)

### Pointer `P_DATA_AUTHORITY`

As written: Agencies shall ensure that “all confidential information or sensitive and personal data must be authorized by appropriate agency authority for use in the manner proposed” and that it “when used, is anonymized, encrypted, or otherwise protected when used with AI tools”. “Before using any GenAI system, agencies shall assess whether the tool stores, processes, or accesses sensitive data.”

SS-23-002 refers to an 'appropriate agency authority' for authorizing use of confidential, sensitive or personal data with AI tools. The documents do not say who that is.

On the 'other AI' branch: SS-23-002 says: “This includes:” … “all confidential information or sensitive and personal data must be authorized by appropriate agency authority for use in the manner proposed”; SS-23-002 says: “This includes:” … “when used, is anonymized, encrypted, or otherwise protected when used with AI tools” [modal as written: must (earlier in same sentence)]

Citations:
- Artificial Intelligence Responsible Use (SS-23-002), 6. Data Protection, Safety and Privacy, p.9
- Generative AI Responsible Use (SS-25-001), 1.3 Data Privacy and Confidentiality, p.3

Conflicts and open questions affecting this pointer:
- Conflict C04: The documents disagree on whether personal or sensitive data can ever be entered and who can approve it: GTA's Office of Artificial Intelligence (SS-25-001 1.3), an 'appropriate agency authority' (SS-23-002 6), the Georgia Technology Authority generally (GS-25-001 rubric), or no stated exception (other GS-25-001 passages and the SS-25-001 table).
- Conflict C10: Incident and misuse reports go to different recipients in different documents, and only SS-25-001 sets a deadline (48 hours).

## Outcome block: OUT_P_HIGH_RISK

Shown when: (F_DECISION is one of: yes, not_sure) OR (F_TASK is one of: other, not_sure, policy_drafting, education_training)

### Pointer `P_HIGH_RISK`

As written: “Agencies should conduct their own risk assessments and consult with the Georgia Technology Authority (GTA) Office of Artificial Intelligence for novel, high-risk, or ambiguous use cases not represented here.” “Agencies shall implement human-in-the-loop (HITL) review workflows, especially for moderate- and high-risk use cases.”

Check with your agency about its risk assessment and human-in-the-loop review workflow for this use; SS-25-001 says agencies should consult the GTA Office of Artificial Intelligence for novel, high-risk, or ambiguous use cases.

On the 'other AI' branch: not shown.

Citations:
- Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (text above and below the table), p.6
- Generative AI Responsible Use (SS-25-001), 1. Human Review and Validation, p.2

Conflicts and open questions affecting this pointer:
- Conflict C12: GS-25-001 mentions 'regularly clearing chats' while other provisions call for keeping records of prompts and responses; the documents do not say how these fit together.
- Conflict C13: SS-25-001 says review is by 'qualified personnel' before use 'in any official capacity'; SS-23-002 says agencies ensure review and approval 'by the business owner or designated personnel' before content is 'published or used for decision-making'.

## Outcome block: OUT_P_PROCUREMENT

Shown when: (F_ROLE is one of: procure, both, not_sure)

### Pointer `P_PROCUREMENT`

As written: “Agencies shall submit all software, applications, tools, and services utilizing AI for business operations to GTA for review prior to procurement.” “Agencies shall submit a Business Solutions Review (BSR) Request form to GTA via email” “Agencies must consult with the GTA Office of Artificial Intelligence before entering into any contractual agreement involving GenAI features or integrations.” “Individual agencies retain discretion to purchase premium versions through standard procurement processes.”

Check with your agency how it submits AI tools to GTA for review before procurement. The documents describe more than one route (see conflict C08).

On the 'other AI' branch: PS-23-001 says: “Agencies shall submit all software, applications, tools, and services utilizing AI for business operations to GTA for review prior to procurement.”; SS-23-002 says: “Agencies shall submit a Business Solutions Review (BSR) Request form to GTA via email”

Citations:
- Enterprise Artificial Intelligence Responsible Use (PS-23-001), Policy, p.3
- Artificial Intelligence Responsible Use (SS-23-002), 3. Procuring AI Solutions, p.5
- Generative AI Responsible Use (SS-25-001), 1.5 Procurement and Third-Party Vendor Compliance, p.4
- Generative AI Responsible Use (SS-25-001), Standard (opening paragraphs, before section 1), p.2

Conflicts and open questions affecting this pointer:
- Conflict C02: PS-23-001 cites a standard numbered SS-23-001; the standard in the document set is numbered SS-23-002.
- Conflict C03: PS-23-001 defines 'Artificial Intelligence' in the words the other documents use for 'Generative AI', so the reach of its procurement-review rule is unclear.
- Conflict C08: Pre-procurement review is described three ways: a web form at ai.georgia.gov (SS-25-001), a Business Solutions Review form sent by email (SS-23-002), and submission to GTA with no channel named (PS-23-001).
- Open question OQ08: Does 'Agencies shall implement additional restrictions based on their specific needs' impose a duty or grant a permission?
- Open question OQ17: Does PS-23-001's passed review date (01/15/2025) affect its status?

## Outcome block: OUT_P_CONTRACTS

Shown when: (F_ROLE is one of: procure, both, not_sure)

### Pointer `P_CONTRACTS`

As written: “Service and technology contracts shall provide standards of third-party provider and their partners or subcontractors, including:” “Adhering to GTA Policies, Standards and Guidelines (PSGs)”; “Adhering to NIST guidance, risk management frameworks and standards for responsible artificial intelligence practices.”; and providing the contractors' Responsible AI framework and policies to GTA.

Check with your agency's procurement process for the contract standards SS-23-002 section 3 lists. The documents do not name an office.

Citations:
- Artificial Intelligence Responsible Use (SS-23-002), 3. Procuring AI Solutions, p.5

## Outcome block: OUT_P_SANDBOX

Shown when: (F_ROLE is one of: build, both, not_sure)

### Pointer `P_SANDBOX`

As written: “To participate in the Horizons Innovation Lab, agencies shall:” “Submit a brief project proposal outlining goals, target outcomes, and potential risks via the online form at https://ai.georgia.gov/innovation-lab/how-do-i-submit-project-innovation-lab” “Following successful sandbox evaluation, agencies shall seek approval to transition GenAI projects into pilot or production phases.”

Sandbox participation is arranged by the agency with GTA's Horizons Innovation Lab; check with your agency whether your project is or should be in the Sandbox.

On the 'other AI' branch: not shown.

Citations:
- Generative AI Responsible Use (SS-25-001), 2.2 Participation Requirements, p.5
- Generative AI Responsible Use (SS-25-001), 2.5 Advancement and Scaling, p.5

## Outcome block: OUT_P_MEETINGS_AGENCY

Shown when: (F_TASK is one of: meetings, not_sure)

### Pointer `P_MEETINGS_AGENCY`

As written: “Agencies should ensure that the use of AI tools in virtual meetings complies with all relevant laws and regulations, including those related to data protection, intellectual property, and labor laws.”

Check with your agency for its rules on AI tools in virtual meetings. The documents do not name an office.

On the 'other AI' branch: not shown.

Citations:
- Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Be Vigilant in Virtual Meetings, p.3

## Closing line (every outcome)

This tool lists which GTA policies, standards and guidelines apply to what you described. It does not say whether a specific use is permitted overall, and it is not legal advice. For decisions the documents leave to the agency, ask your agency.

# Verification report

Every path was enumerated by following 'next' from the first question and honoring 'ask_if'. For each path the outcome was assembled from this file's 'outcomes' and separately recomputed from stage2_map.json ('activated_by' for elements, 'show_when' for pointers); the two were compared. Each asked question was tested by changing only its answer and recomputing; each skipped question was tested by supplying every possible answer and recomputing.

- Number of paths: 6016
- Longest path: 7 questions (limit 8; within limit: True)
- Shortest path: 1 questions
- Paths by length: {'1': 1, '3': 15, '5': 240, '6': 4680, '7': 1080}
- Distinct outcomes: 1161
- Mismatches: 0
- Conditional elements: 26; unreachable: []
- Asked questions whose answer cannot change the result: 0
- Skipped questions that could have changed the result: 0
- Every question has a Not sure option: True
- Question order: Q_TYPE, Q_TASK, Q_PRODUCT, Q_ROLE, Q_DATA, Q_HOST, Q_DECISION

The AI-type question comes first because it decides which provisions are in scope. The rest are ordered by the average number of fact-dependent elements an answer rules out, assuming each answer is equally likely. Only 'It does not use AI' ends the interview early; otherwise order does not change how many questions are asked, only the 'ask_if' skips do.

- F_TYPE: Asked first: it decides which provisions are in scope.
- F_TASK: rules out 12.94 elements per answer on average; 15 elements depend on it
- F_PRODUCT: rules out 2.25 elements per answer on average; 4 elements depend on it
- F_ROLE: rules out 2.0 elements per answer on average; 5 elements depend on it
- F_DATA: rules out 1.0 elements per answer on average; 2 elements depend on it
- F_HOST: rules out 0.33 elements per answer on average; 1 elements depend on it
- F_DECISION: rules out 0.33 elements per answer on average; 1 elements depend on it
