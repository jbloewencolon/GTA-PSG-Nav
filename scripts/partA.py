import json, re, sys, collections
INV, OUT = sys.argv[1], sys.argv[2]
inv = json.load(open(INV, encoding='utf-8'))
P = collections.OrderedDict((p['id'], p) for p in inv['provisions'])

def R(doc, code, spec='all'):
    if spec == 'all':
        rx = re.compile('^' + re.escape(f"{doc}-{code}-") + r'\d+$')
        out = [i for i in P if rx.match(i)]
    else:
        out = [f"{doc}-{code}-{n}" for n in spec]
    assert out, (doc, code)
    for i in out: assert i in P, i
    return out
def rng(a, b): return list(range(a, b + 1))
SS25, GS25, GS252, PS23, SS23, GS23, GP5 = "SS-25-001", "GS-25-001", "GS-25-002", "PS-23-001", "SS-23-002", "GS-23-001", "5GP"

ELEMENTS = []
def E(eid, title, tier, ids, activated_by, basis, summaries=None, auto=False):
    ELEMENTS.append(dict(id=eid, title=title, tier=tier, provision_ids=ids, activated_by=activated_by, tier_basis=basis, _summ=summaries or {}, _auto=auto))

ALWAYS = "always"; NA = "not_applicable"
B_EMP = "Addressed to employees, agency personnel or users by name, or stated without a named party inside a document that says employees are to follow it (SS-25-001 Standard, p.2: 'State government employees shall follow this standard when using commercial GenAI solutions'; GS-25-001 Purpose, p.1: 'By following these guidelines, state employees can use AI responsibly'). No further condition in the text."
B_COND = "Same basis as the umbrella tier for who is bound; the provision's own trigger limits it to the situation named in activated_by."
B_AGY = "The text names agencies, GTA, the State CIO, vendors or contractors as the party that acts; no action is stated for the individual employee."

# ---------------- umbrella ----------------
E("U_SCOPE", "What these documents cover and who is to follow them", "umbrella",
  R(SS25, "PURPOSE") + R(SS25, "STD", [1, 2]) + R(SS25, "3.0", [1, 2, 3]) + R(GS25, "PURPOSE", [1, 2]) + R(PS23, "PURPOSE") + R(SS23, "PURPOSE"), ALWAYS, B_EMP,
  {"must": "SS-25-001 says: “State government employees shall follow this standard when using commercial GenAI solutions such as OpenAI's ChatGPT, Google's Gemini, Anthropic's Claude, or Microsoft's Copilot.”",
   "informational": "SS-25-001's requirements “apply to all GenAI systems and services used within the State of Georgia’s executive branch agencies”, GS-25-001's guidelines “apply to all forms of generative AI”, and SS-25-001's use-case table is a non-exhaustive set of examples."})
E("U_PRINCIPLES", "The 5 Guiding Principles", "umbrella", R(GS25, "PURPOSE", [3]), ALWAYS, B_EMP,
  {"should": "GS-25-001 says: “When engaging with generative AI, all state employees should abide by the 5 Guiding Principles” (Implement Responsible Systems; Ensure Ethical and Fair Use of Automated Decisions; Maintain Data Quality and Privacy; Keep AI Usage Transparent; Keep Human Involvement at the Center)."})
E("U_APPROVED_TOOLS", "Use AI tools GTA has vetted", "umbrella", R(GS25, "SAFE", [1, 2, 3, 4]) + R(SS25, "3.0-APPROVAL"), ALWAYS, B_EMP,
  {"should": "“State employees should only use AI which GTA has vetted, with pre-approved vendors”, and “Employees are encouraged to consult with GTA regularly for updates and to verify they are using compliant versions of AI tools.”",
   "may": "“Conditional Approval for specific use cases of GenAI tools can be requested via ai.georgia.gov or email ai@gta.georgia.gov.”",
   "informational": "Approval of one version of an AI model “does not necessarily imply that other versions of that same model are also approved”, and “an approved AI model can always have its approval revoked”."})
E("U_CREDENTIALS", "Sign in with your state-issued account", "umbrella", R(SS25, "1.4") + R(GS25, "SAFE", [17]) + R(GS25, "STRAT", [1, 2]), ALWAYS, B_EMP,
  {"must": "“All agency personnel shall use state-issued credentials (email and authentication accounts) when signing up for or using GenAI tools for state business.”",
   "must_not": "“The use of personal email addresses for such access is prohibited unless specifically authorized by the agency’s technology leadership.”",
   "should": "GS-25-001 gives these instructions without a modal verb: “avoid using personal accounts, such as personal email addresses, within any software”, “Keep personal and work materials separate”, and “create an account using your work email specifically for GenAI materials”."})
E("U_REVIEW", "Review and verify what the AI produces", "umbrella", R(SS25, "1", [1, 3]) + R(GS25, "SAFE", [6, 7, 12]) + R(GS25, "PRIV", [4]) + R(GS25, "RUBRIC", [4, 5]), ALWAYS, B_EMP,
  {"must": "“All GenAI-generated content—whether text, code, summaries, or other media—shall be reviewed and validated by qualified personnel before being used in any official capacity” (SS-25-001), and all AI-generated content must be “double-checked to ensure it is free of inaccurate information, AI hallucinations, or bias” (GS-25-001).",
   "should": "“employees should apply careful review methods”; GS-25-001 also instructs, without a modal verb, “For any fact provided by an AI, find a reliable source that corroborates it”, “Carefully review AI-generated content for accuracy”, and “Cross-check information with reliable sources”.",
   "informational": "The reviews are “to detect inaccuracies, biases, or inappropriate content”, and review “includes cross-checking AI outputs with trusted sources, verifying the accuracy of information, and assessing for possible biases or inaccuracies”."})
E("U_HUMAN", "Keep a human in charge and use judgment", "umbrella", R(GS25, "SAFE", [8, 24]) + R(GS25, "RUBRIC", [1, 2, 3]) + R(GS25, "GP-V", [12]) + R(GP5, "V", [12]) + R(GS23, "V.7", [2]), ALWAYS, B_EMP,
  {"should": "AI tools “should not be the only agents involved in any decision-making” and “AI should never have autonomous decision-making capabilities”; “Employees should use common sense and exercise caution in deciding whether AI is right for a given task”; “Users should be aware of how AI contributes to outcomes and that humans remain responsible for those outcomes”; the rubric also instructs, without a modal verb, that a human review “both the inputs to and outputs from the AI”."})
E("U_LABEL", "Label and cite AI-generated content", "umbrella", R(SS25, "1.2", [1]) + R(GS25, "PRIV", [3]) + R(GS25, "SAFE", [11]) + R(GS25, "CITE", [1, 2, 3]), ALWAYS, B_EMP,
  {"must": "“Any content generated or assisted by GenAI shall be clearly labeled” (SS-25-001), and “All AI-generated content – including text, images, videos, and audio – must be clearly labeled as AI-generated” (GS-25-001).",
   "should": "“Anything produced with the assistance of AI should be cited correctly”, and “AI should be cited when its content is used as a product rather than a tool”.",
   "informational": "“AI-generated content is considered a product when a substantial portion of the content is featured in the final product, even if the user extensively edits it.”"})
E("U_TRANSPARENCY", "Be open about your AI use", "umbrella", R(GS25, "SAFE", rng(19, 23)) + R(GS25, "PRIV", [1, 2]) + R(GS25, "RUBRIC", [10, 11]), ALWAYS, B_EMP,
  {"should": "“All state employees should be open and honest about their AI use” and “should rely on the honor system, openly disclosing AI usage without fear of severe repercussions”; GS-25-001 also instructs, without a modal verb, “Cite and acknowledge all AI-generated, brainstormed, or edited content” and “Clearly inform users when they are interacting with AI-generated content.”",
   "informational": "“The goal of these guidelines is to reduce the risk of employees using Shadow AI.”"})
E("U_RECORDS", "Keep a record of prompts and responses", "umbrella", R(GS25, "SAFE", [5]) + R(SS25, "1.7", [1]), ALWAYS, B_EMP,
  {"should": "“Employees should create a record of queries and responses outside of the generative AI software or platform for future reference.”",
   "informational": "“GenAI-generated content used in official communications or policy-making may be subject to Georgia’s records retention schedules and open records laws.”"})
E("U_DATA_CARE", "Protect data when you use AI tools", "umbrella", R(SS25, "1.3", [3, 4]) + R(GS25, "SAFE", [13]) + R(GS25, "STRAT", [3, 4, 5]), ALWAYS, B_EMP,
  {"must": "SS-25-001 says “The following safeguards shall be observed”, including “data minimization practices to avoid the inclusion of unnecessary sensitive information” and adherence to “encryption and access control requirements consistent with all applicable enterprise security policies and standards”.",
   "should": "GS-25-001 instructs, without a modal verb: “Opt out of data collection on any tool you use, particularly those involving pictures” and “Protect all data used by AI systems from unauthorized access or breaches.”",
   "informational": "“Generative AI models use user-inputted information to further train their models”; protecting data “includes regularly changing passwords, minimizing data retention by regularly clearing chats, and conducting regular audits to ensure compliance”."})
E("U_LAWS", "Stay within privacy and other laws", "umbrella", R(GS25, "STRAT", [7]) + R(GS25, "RUBRIC", [12]), ALWAYS, B_EMP,
  {"must": "“The use of GenAI tools must be consistent with Georgia’s privacy laws, such as the Georgia Computer Data Privacy Act (GCDPA).”",
   "should": "The rubric instructs, without a modal verb: “Ensure that all AI applications are fully compliant with relevant laws and regulations, both at the federal level, as well as those set forth by the State of Georgia.”"})
E("U_BIAS", "Watch for bias", "umbrella", R(GS25, "BIAS") + R(GS25, "RUBRIC", [8, 9]), ALWAYS, B_EMP,
  {"should": "“It is important to be aware of these types of biases in any work produced by AI and screen the work for bias before putting them into use”; GS-25-001 also instructs, without a modal verb, to word questions carefully, to consider whether a question “presupposes things that are not necessarily true”, and to “consult a third party or non-AI source before proceeding”.",
   "informational": "“Generative AI models can inadvertently perpetuate biases”."})
E("U_TRAINING", "Training", "umbrella", R(SS23, "7"), ALWAYS, "Addressed to 'All users of AI systems' (SS-23-002 section 7); an employee using a generative AI tool is a user of an AI system under that standard's definitions. See OQ20.",
  {"must": "“All users of AI systems shall undergo appropriate training to ensure the responsible and ethical use of these tools”, including “Being familiarized with this AI Usage Policy and any other relevant policies, guidelines, and best practices” and “Participating in regular training sessions and workshops”."})
E("U_CONSEQUENCES", "What the documents say happens if they are not followed", "umbrella", R(SS25, "1.7", [5]) + R(SS23, "11"), ALWAYS, B_EMP,
  {"informational": "“Failure to follow these requirements may result in revocation of tool access and additional oversight actions by GTA” (SS-25-001); “Any state employee, contractor, or vendor found to violate this standard will be subject to disciplinary action, including but not limited to, termination of employment, contract, or agreement” (SS-23-002)."})

# ---------------- conditional ----------------
YN = lambda f: [{f: ["yes", "not_sure"]}]
E("C_DATA", "Entering personal, sensitive or confidential information", "conditional", R(SS25, "1.3", [2]) + R(GS25, "SAFE", [14]) + R(GS25, "STRAT", [6]) + R(GS25, "RUBRIC", [6, 7]), YN("F_DATA"), B_COND,
  {"must_not": "“Personally identifiable information (PII), protected health information (PHI), or other regulated data shall not be used as inputs to GenAI tools unless formally approved by the GTA’s Office of Artificial Intelligence” (SS-25-001); GS-25-001 says “do not provide them with confidential or private state information, or personal records” and “Do not enter personal and/or sensitive data into a GenAI model.”",
   "should": "The GS-25-001 rubric instructs, without a modal verb: “Always verify that the AI is not handling sensitive or private information, unless given explicit approval from the Georgia Technology Authority. In such cases, ensure that strict data protection protocols are being consistently enforced.”"})
E("C_DATA_UNSURE", "When you are not sure whether data may be entered", "conditional", R(GS25, "SAFE", [15, 16]), [{"F_DATA": ["not_sure"]}], B_COND,
  {"should": "“If employees are uncertain whether specific data should be entered into a generative AI tool, they should first consult with their department's data privacy officer or designated compliance authority to clarify”; “it is better to err on the side of caution and avoid inputting potentially sensitive information without approval”."})
E("C_DECISIONS", "Decisions about people", "conditional", R(GS25, "SAFE", [9, 10]) + R(SS25, "3.0-TABLE", [15, 18]),
  [{"F_DECISION": ["yes", "not_sure"]}, {"F_TASK": ["policy_drafting", "education_training", "not_sure"]}],
  B_COND + " The two table prohibitions sit in the 'Policy drafting support' and 'Education & training tools' rows of the SS-25-001 table, so those tasks also activate this element.",
  {"may": "GS-25-001 gives this example: “an HR department may consult with AI platforms in making hiring decisions”.",
   "must_not": "The same example says “it may not use AI to scan and reject resumes automatically”; the SS-25-001 table lists as prohibited “Do not use GenAI to make legal, disciplinary, or eligibility decisions” and “Do not use GenAI to assess employee performance or give personalized advice.”"})
E("C_CITE_NONE", "No citation when AI only helped you develop your own content", "conditional", R(GS25, "CITE", [4]), [{"F_PRODUCT": ["none"]}], B_COND,
  {"may": "GS-25-001 says “if the AI model helps a user in generating their own content and ideas, citation isn’t necessary”."})
E("C_CITE_REQUIRED", "Citation when AI content appears in the final product", "conditional", R(GS25, "CITE", [5]), [{"F_PRODUCT": ["informal", "official", "not_sure"]}], B_COND,
  {"must": "GS-25-001 says “if the AI model’s content or ideas appear in the final product, a citation is required”."})
E("C_CITE_INFORMAL", "How to cite in an informal document", "conditional", R(GS25, "CITE", [6]), [{"F_PRODUCT": ["informal"]}], B_COND,
  {"must": "For “an informal document like an email”, GS-25-001 says “all that is necessary is to acknowledge somewhere in the text that AI was used in its development and which AI model was used”."})
E("C_CITE_OFFICIAL", "How to cite in a more official document", "conditional", R(GS25, "CITE", [7, 8]), [{"F_PRODUCT": ["official", "not_sure"]}], B_COND,
  {"must": "GS-25-001 says “on more official documents, it is necessary to use a more detailed citation”.",
   "should": "GS-25-001 instructs, without a modal verb: “Be sure to include the name of the AI model, the name of the prompt used, the company to which the AI model belongs, and the date that the content was generated.”"})
def row(r, cols=(1, 2, 3)): return R(SS25, "3.0-TABLE", [3 * r + c for c in cols])
def T(v): return [{"F_TASK": [v, "not_sure"]}]
E("C_TASK_SUMMARY", "Task: summarizing or drafting internal documents", "conditional", row(0) + R(GS25, "TASK-INFOPROC"), T("internal_summaries"), B_COND, auto=True)
E("C_TASK_RESEARCH", "Task: looking up or gathering information", "conditional", R(GS25, "TASK-INFOGATH"), T("research"), B_COND, auto=True)
E("C_TASK_PUBLIC", "Task: public-facing communications", "conditional", row(1), [{"F_TASK": ["public_comms", "chatbot_public", "not_sure"]}], B_COND + " This SS-25-001 row includes “Deploy public chatbots with GenAI only after bias/safety review.” (SS-25-001-3.0-TABLE-5), so it is also shown for a chatbot that members of the public interact with.", auto=True)
E("C_TASK_CODING", "Task: coding and software development", "conditional", row(2) + R(GS25, "TASK-CODE"), T("coding"), B_COND, auto=True)
E("C_TASK_DATA_ANALYSIS", "Task: data analysis and reports", "conditional", row(3), T("data_analysis"), B_COND, auto=True)
E("C_TASK_POLICY", "Task: policy drafting support", "conditional", row(4, (1, 2)), T("policy_drafting"), B_COND, auto=True)
E("C_TASK_EDU", "Task: education and training materials", "conditional", row(5, (1, 2)), T("education_training"), B_COND, auto=True)
E("C_TASK_CHATBOT", "Task: chatbots and user interaction", "conditional", row(6) + R(GS25, "TASK-USER") + R(GS25, "SAFE", [18]), [{"F_TASK": ["chatbot_public", "chatbot_internal", "not_sure"]}], B_COND, auto=True)
E("C_TASK_MEDIA", "Task: image, audio or video generation", "conditional", row(7) + R(GS25, "CITE", [9, 10]), T("media"), B_COND, auto=True)
E("C_TASK_TRANSLATION", "Task: translation and accessibility", "conditional", row(8), T("translation"), B_COND, auto=True)
E("C_TASK_LEGAL", "Task: legal and regulatory analysis", "conditional", row(9), T("legal"), B_COND, auto=True)
E("C_TASK_CONTENT", "Task: brainstorming, editing and other content generation", "conditional", R(GS25, "TASK-CONTENT"), T("content"), B_COND, auto=True)
E("C_MEETINGS", "AI in virtual meetings", "conditional", R(GS25, "MEET", [1, 5, 7, 8, 9, 10]), T("meetings"), B_COND,
  {"should": "“The use of AI note-taking tools in Microsoft Teams meetings or any other conferencing platforms is strongly discouraged for meetings held within the State”; AI recording and transcription “should be used thoughtfully”, “AI should not be used to manipulate or misrepresent the contributions of participants”, and “AI outputs should be used only to supplement, not replace, human judgment.”",
   "informational": "“Once created, meeting recordings and transcriptions become public records and are subject to retention rules.”"})
E("C_MEETING_HOST", "If you host the meeting", "conditional", R(GS25, "MEET", [2, 3, 4, 11]), [{"F_TASK": ["meetings", "not_sure"], "F_HOST": ["host", "not_sure"]}],
  "Addressed to 'Meeting hosts' by name (GS-25-001, Be Vigilant in Virtual Meetings).",
  {"may": "“Meeting hosts may opt to use the recording and transcription services built into Teams.”",
   "should": "“Meeting hosts should be diligent when admitting participants to virtual meetings to ensure no AI bot note-takers join.”",
   "must": "GS-25-001 says, without a modal verb: “Meeting hosts are responsible for determining the need for recordings and automated transcriptions and keeping any records created.”",
   "informational": "“You can look for the “.ai” suffix to confirm.”"})
PRO = [{"F_ROLE": ["procure", "both", "not_sure"]}]; BLD = [{"F_ROLE": ["build", "both", "not_sure"]}]
B_PROC = "GS-25-002's Purpose names state agencies, but its items are instructions to the people preparing and evaluating a procurement and speak of 'your team'; placed as conditional for employees who do that work. See OQ22."
E("C_PROCURE_APPROVAL", "GTA approval before procuring a GenAI product or service", "conditional", R(SS25, "1.5", [1, 2, 3]), PRO, "Stated without a named party ('Any procurement of GenAI products or services must:') in the standard employees are to follow; applies to whoever carries out the procurement.",
  {"must": "“Any procurement of GenAI products or services must” be “approved in advance by the Georgia Technology Authority (GTA) by completing the review form at https://ai.georgia.gov/ai-application-and-tool-request-form”, comply “with GTA’s IT security, privacy, and accessibility standards”, and include “provisions for auditability, explainability, model documentation, data retention, and intellectual property rights in contracts”."})
E("C_PROC_PRINCIPLES", "Procurement of AI tools: key principles", "conditional", R(GS252, "PURPOSE") + R(GS252, "KP"), PRO, B_PROC,
  {"should": "GS-25-002's key principles are instructions written without modal verbs, for example “Prioritize data assessment and governance before procurement”, “Emphasize the problem, not a specific solution”, “Establish robust oversight mechanisms”, and “Plan for ongoing evaluation, maintenance, training, and knowledge transfer throughout the AI system's lifecycle.”",
   "informational": "“These guidelines outline best practices for state agencies when preparing and evaluating Requests for Proposals (RFPs) or other procurements for AI tools or solutions that include AI features.”"})
E("C_PROC_PREP", "Procurement of AI tools: preparing the RFP", "conditional", [i for i in P if i.startswith("GS-25-002-PREP-")], PRO, B_PROC,
  {"should": "GS-25-002 lists twelve topics of instructions for preparing the RFP (objectives and scope; ethics and fairness; transparency and explainability; data privacy and security; performance and accountability; open standards; workforce change management and training; continuous monitoring; ethical AI governance; algorithmic impact assessment; collaboration; referrals), written without modal verbs except where it says the vendor or the assessment “should” do something; read the cited section for each item."})
E("C_PROC_EVAL", "Procurement of AI tools: evaluating RFP responses", "conditional", [i for i in P if i.startswith("GS-25-002-EVAL-")], PRO, B_PROC,
  {"should": "GS-25-002 lists thirteen topics of instructions for evaluating RFP responses, from “Establish a diverse evaluation committee with expertise in AI, ethics, and procurement” to “Where feasible, require a pilot phase before full deployment”, written without modal verbs except “Both training and technical documentation should be provided”; read the cited section for each item."})
E("C_DEVELOP", "Developing AI tools or working with external collaborators", "conditional", R(SS23, "9"), BLD, "Stated without a named party ('the following guidelines shall be adhered to') and triggered by 'When developing AI tools or engaging with external collaborators' (SS-23-002 section 9).",
  {"must": "“When developing AI tools or engaging with external collaborators, the following guidelines shall be adhered to”, including that “Collaboration agreements must clearly disclose the manner and use of AI technology”, “AI development shall prioritize safety, privacy, and ethical considerations”, “Prior to deployment, AI systems shall undergo rigorous testing”, and risks or ethical concerns “shall be reported to the agency’s designated Ethics Officer, CIO, and State CIO”.",
   "should": "Collaboration agreements “should also address ownership and usage rights of AI models and data.”"})

# ---------------- out of scope for employee ----------------
def O(eid, title, ids, basis=B_AGY): E(eid, title, "out_of_scope_for_employee", ids, NA, basis)
O("O_AGENCY_RESTRICTIONS", "Agency discretion and additional restrictions", R(SS25, "STD", [3, 4, 5]))
O("O_AGENCY_OUTPUTS", "Agency duties for responsible use, bias and accuracy of AI output", R(SS25, "1", [2]) + R(SS23, "1", [1, 2, 3, 4]) + R(SS23, "4") + R(SS23, "5"))
O("O_ATTRIB_FORMAT", "Agency standardized attribution formats", R(SS25, "1.2", [2, 3, 4, 5]))
O("O_AGENCY_DATA", "Agency data protection duties", R(SS25, "1.3", [1]) + R(SS23, "6"))
O("O_PROCURE_AGENCY", "Agency submission of AI tools to GTA before procurement", R(SS25, "1.5", [4]) + R(PS23, "POLICY") + R(SS23, "3", [1, 2, 3]))
O("O_CONTRACTS_VENDORS", "Contract standards and vendor duties", R(SS23, "2") + R(SS23, "3", rng(4, 26)))
O("O_INVENTORY_AUDIT", "Agency inventory, reporting of tools, audits and monitoring", R(SS25, "1.6") + R(SS25, "4.0", [1]) + R(SS23, "1", [5]) + R(SS23, "12"))
O("O_RECORDS_AGENCY", "Agency records management for GenAI outputs", R(SS25, "1.7", [2, 3, 4]))
O("O_INCIDENTS", "Agency reporting of incidents and misuse", R(SS25, "4.0", [2]) + R(SS23, "8"))
O("O_SANDBOX", "GTA Horizons Innovation Lab and GenAI Sandbox", R(SS25, "2") + R(SS25, "2.1") + R(SS25, "2.2") + R(SS25, "2.3") + R(SS25, "2.4") + R(SS25, "2.5"),
  "Section 2 of SS-25-001 addresses GTA and 'agencies' participating in the Sandbox; 2.3 is stated of 'All tools tested in the Sandbox' with no employee action.")
O("O_AGENCY_RISK", "Agency risk assessments for novel or high-risk use cases", R(SS25, "3.0", [4]))
O("O_MEET_AGENCY", "Agency compliance for AI tools in virtual meetings", R(GS25, "MEET", [6]))
O("O_TERMINATION", "Termination of AI tools and contingency planning", R(SS23, "10"))
B_PR = "The introduction to the principles says they 'are intended to guide state agencies as they integrate protective measures into their policies and operational procedures' (5GP p.1; GS-25-001 Guiding Principles p.5; GS-23-001 Principles p.2: 'direct state agencies'); items are addressed to state agencies, GTA, or have no named subject. Placed out of scope from that context. See OQ14 and OQ21."
def PR(code25, code5, codes23):
    out = R(GS25, "GP-" + code25) + R(GP5, code5)
    for c in codes23: out += R(GS23, c)
    return out
O("O_PRINC_INTRO", "Guiding principles: purpose and applicability statements", PR("INTRO", "INTRO", ["PURPOSE", "PRINCIPLES"]), B_PR)
O("O_PRINC_I", "Guiding principle: Implement Responsible Systems", PR("I", "I", ["I.1", "I.2", "I.3", "I.4", "I.5", "I.6"]), B_PR)
O("O_PRINC_II", "Guiding principle: Ensure Ethical and Fair Use of Automated Decisions", PR("II", "II", ["II.1", "II.2", "II.3", "II.4", "II.5", "II.6"]), B_PR)
O("O_PRINC_III", "Guiding principle: Maintain Data Quality and Privacy", PR("III", "III", ["III"]), B_PR)
O("O_PRINC_IV", "Guiding principle: Keep AI Usage Transparent", PR("IV", "IV", ["IV"]), B_PR)
umb = set(ELEMENTS[5]['provision_ids'])
O("O_PRINC_V", "Guiding principle: Keep Human Involvement at the Center", [i for i in PR("V", "V", ["V.1", "V.2", "V.3", "V.4", "V.5", "V.6", "V.7", "V.8", "V.9", "V.10"]) if i not in umb], B_PR)

# ---------------- placement check ----------------
seen = collections.Counter(i for e in ELEMENTS for i in e['provision_ids'])
dups = [i for i, n in seen.items() if n > 1]; missing = [i for i in P if i not in seen]
assert not dups, dups
assert not missing, missing
EL = {e['id']: e for e in ELEMENTS}
elem_of = {i: e['id'] for e in ELEMENTS for i in e['provision_ids']}

def cite(p):
    ident = p['doc_id'] if p['doc_id'] != '5GP' else 'no identifier'
    return f"{p['doc_title']} ({ident}), {p['section']}, p.{p['page']}"
ORDER = ["must", "must_not", "should", "may", "informational"]
def auto_label(p):
    aw = p['modal_as_written']
    if 'Acceptable' in aw: return "SS-25-001 table, Acceptable (Green = Approved)"
    if 'Conditional' in aw: return "SS-25-001 table, Conditional (Yellow = Caution)"
    if "column heading 'Prohibited'" in aw: return "SS-25-001 table, Prohibited (Red = Prohibited)"
    if 'Permissible' in aw: return "GS-25-001, listed as Permissible"
    if "'Prohibited:'" in aw: return "GS-25-001, listed as Prohibited"
    if p['notes'] and 'Questions to Consider' in p['notes']: return "GS-25-001, question to consider"
    return f"{p['doc_id']}"
for e in ELEMENTS:
    groups = collections.OrderedDict()
    for i in e['provision_ids']: groups.setdefault(P[i]['modality'], []).append(i)
    st = []
    for m in ORDER:
        if m not in groups: continue
        ids = groups[m]
        if e['tier'] == 'out_of_scope_for_employee':
            who = sorted({P[i]['addressee'] for i in ids})
            summ = f"{len(ids)} provision(s) recorded with modality '{m}' and addressee {', '.join(who)}; the documents state no action for the individual employee. See the provisions in stage1_inventory.json."
        elif e['_auto']:
            summ = " ".join(f"{auto_label(P[i])}: “{P[i]['text_excerpt']}”" for i in ids)
        else:
            assert m in e['_summ'], (e['id'], m)
            summ = e['_summ'][m]
        cites = []
        for i in ids:
            c = cite(P[i])
            if c not in cites: cites.append(c)
        st.append(dict(modality=m, modal_as_written=sorted({P[i]['modal_as_written'] for i in ids}), summary=summ, provision_ids=ids, citations=cites))
    extra = set(e['_summ']) - set(groups)
    assert not extra, (e['id'], extra)
    e['statements'] = st
    e['addressee_counts'] = dict(collections.Counter(P[i]['addressee'] for i in e['provision_ids']))
    e['provision_count'] = len(e['provision_ids'])
    del e['_summ'], e['_auto']

# ---------------- facts ----------------
def acts(fid, val):
    out = []
    for e in ELEMENTS:
        if e['tier'] != 'conditional': continue
        if any(val in c.get(fid, []) for c in e['activated_by']): out.append(e['id'])
    return out
def defc(term, doc):
    d = [x for x in inv['definitions'] if x['term'] == term and x['doc_id'] == doc][0]
    return f"Definition of '{term}': {d['doc_title']} ({doc}), {d['section']}, p.{d['page']}: “{d['text']}”"
TASKS = [("internal_summaries", "Summarizing or drafting internal documents (meeting notes, memos, internal summaries)"),
 ("research", "Looking up or gathering information on a topic"),
 ("public_comms", "Writing for the public (website, email to the public, social media, press)"),
 ("coding", "Writing, reviewing or documenting code"),
 ("data_analysis", "Analyzing data or producing reports from data"),
 ("policy_drafting", "Drafting policy language or summarizing research for policy"),
 ("education_training", "Creating education or training materials"),
 ("chatbot_public", "A chatbot or other tool that members of the public interact with"),
 ("chatbot_internal", "A chatbot or other tool used only by state staff"),
 ("media", "Generating images, audio or video"),
 ("translation", "Translation, captioning or accessibility"),
 ("legal", "Legal or regulatory analysis"),
 ("content", "Brainstorming ideas, or checking grammar and formatting"),
 ("meetings", "Recording, transcribing or taking notes in a virtual meeting"),
 ("other", "Something else"),
 ("not_sure", "Not sure")]
FACTS = []
def F(fid, name, test, values, cites, applies_when=None, term_notes=None):
    FACTS.append(dict(id=fid, name=name, plain_language_test=test,
        values=[dict(value=v, label=l, activates=acts(fid, v)) for v, l in values],
        source_citations=cites, asked_only_when=applies_when, defined_terms=term_notes or []))
c = lambda i: f"{i}: {cite(P[i])}"
F("F_TASK", "What the tool is being used for", "Which one of the listed kinds of work best describes this use? The list is the ten use cases in the SS-25-001 table, the task headings in GS-25-001, and virtual meetings.",
  TASKS, ["Use-case names: Generative AI Responsible Use (SS-25-001), 3.0 Common Gen AI Use Cases (table), pp.6-8", "Task headings: Generative AI Guidelines for Responsible Use (GS-25-001), Mitigating the Risks of Generative AI: Task-Specific, pp.11-12", "Generative AI Guidelines for Responsible Use (GS-25-001), Guidelines > Be Vigilant in Virtual Meetings, p.3"],
  term_notes=["The documents give use-case names without definitions; the labels restate them in everyday words."])
F("F_HOST", "Whether the employee hosts the virtual meeting", "Did you set up or are you running the meeting (the person who admits participants)?",
  [("host", "Yes, I am the host"), ("participant", "No, I am a participant"), ("not_sure", "Not sure")],
  [c("GS-25-001-MEET-3"), c("GS-25-001-MEET-11")], applies_when={"F_TASK": ["meetings", "not_sure"]},
  term_notes=["'Meeting hosts' is not defined; the test uses the document's own description, 'when admitting participants to virtual meetings'."])
F("F_DECISION", "Whether the output feeds a decision about a person", "Will what the AI produces be used to make, or help make, a decision about a specific person, such as hiring, eligibility for a benefit or service, discipline, a performance assessment, or a legal matter?",
  [("yes", "Yes"), ("no", "No"), ("not_sure", "Not sure")],
  [c("GS-25-001-SAFE-9"), c("GS-25-001-SAFE-10"), c("SS-25-001-3.0-TABLE-15"), c("SS-25-001-3.0-TABLE-18"), defc("High-Risk Use Case", "SS-25-001")],
  term_notes=["'High-Risk Use Case' is defined in SS-25-001 as “any GenAI implementation with potential impact on legal rights, access to benefits, public safety, or public trust.” The test asks about the decision examples the documents name; 'moderate-risk' is not defined (OQ09)."])
F("F_ROLE", "Whether the employee also buys or builds AI tools", "Besides using the tool, are you helping to buy, license or contract for an AI tool (including a paid or premium version, or an RFP), or helping to build, configure, pilot or deploy one, or working with an outside partner to develop one?",
  [("use_only", "No, I only use the tool"), ("procure", "Yes, buying, licensing or contracting (including an RFP or a paid version)"), ("build", "Yes, building, configuring, piloting or deploying, or developing with an outside partner"), ("both", "Both buying and building"), ("not_sure", "Not sure")],
  [c("SS-25-001-1.5-1"), c("GS-25-002-PURPOSE-1"), c("PS-23-001-POLICY-1"), "SS-23-002-9 lead-in: Artificial Intelligence Responsible Use (SS-23-002), 9. AI Development and External Collaboration, p.12: “When developing AI tools or engaging with external collaborators, the following guidelines shall be adhered to:”"],
  term_notes=["'Procurement' is not defined; the documents do not say whether signing up for a no-cost tool counts (OQ07)."])
F("F_PRODUCT", "Whether AI content appears in the final work product, and how formal that product is", "Will anything the AI wrote or came up with appear in what you finally produce, even after you edit it? If so, is it an informal document like an email, or something more official?",
  [("none", "No, it only helped me develop my own content and ideas"), ("informal", "Yes, in an informal document like an email"), ("official", "Yes, in something more official than that"), ("not_sure", "Not sure")],
  [defc("AI-generated content as a product", "GS-25-001"), c("GS-25-001-CITE-4"), c("GS-25-001-CITE-5"), c("GS-25-001-CITE-6"), c("GS-25-001-CITE-7")],
  term_notes=["GS-25-001 treats AI content as a 'product' “when a substantial portion of the content is featured in the final product, even if the user extensively edits it.” 'informal document' and 'more official documents' are not defined beyond the example 'like an email'."])
F("F_DATA", "Whether personal, sensitive or confidential information will be entered", "Will you type, paste or upload into the tool any information about identifiable people, health information, personal records, or confidential or private state information?",
  [("yes", "Yes"), ("no", "No, only publicly available or non-sensitive information"), ("not_sure", "Not sure")],
  [c("SS-25-001-1.3-2"), c("GS-25-001-SAFE-14"), c("GS-25-001-STRAT-6"), c("GS-25-001-TASK-INFOPROC-2"), c("GS-25-001-SAFE-15")],
  term_notes=["The documents' trigger terms are 'Personally identifiable information (PII), protected health information (PHI), or other regulated data' (SS-25-001 1.3), 'confidential or private state information, or personal records' and 'personal and/or sensitive data' (GS-25-001), with 'biometrics and financial data' given as examples. None of these terms is defined in the attached set (OQ09), so the plain-language test restates them and cannot be traced to a definition."])
for f in FACTS:
    vals = [tuple(v['activates']) for v in f['values']]
    assert len(set(vals)) > 1, f['id']
AI_DEF = defc("Artificial Intelligence", "SS-25-001"); GEN_DEF = defc("Generative AI (GenAI)", "SS-25-001")
def G(fid, name, test, values, cites, applies_when, term_notes):
    FACTS.insert(len([x for x in FACTS if x.get('gate')]), dict(id=fid, name=name, plain_language_test=test, gate=True,
        values=[dict(value=v, label=l, activates=[], gate_effect=eff) for v, l, eff in values],
        source_citations=cites, asked_only_when=applies_when, defined_terms=term_notes))
G("F_TYPE", "What type of AI the tool is", "Is it generative AI, other AI (one that predicts, classifies, scores or recommends, or an AI agent that carries out tasks on its own), or not AI at all?",
  [("generative", "Generative AI that writes, summarizes, or creates images, audio or video (for example ChatGPT, Gemini, Claude or Copilot)", "All provisions in scope."),
   ("other", "Other AI that predicts, classifies, scores or recommends without creating new content (for example machine learning or deep learning), or an AI agent that carries out tasks or takes actions on its own", "Only provisions in ai_type_rule.other_ai_reaches are shown; AI agents are grouped here (OQ28)."),
   ("none", "It does not use AI", "Scope gate: no element or pointer is shown, because every document in the set covers AI only (see ai_type_rule.not_ai_outcome)."),
   ("not_sure", "Not sure", "Treated as generative AI (protective).")],
  [GEN_DEF, defc("Machine learning", "SS-23-002"), defc("Deep learning", "SS-23-002"), c("SS-23-002-PURPOSE-1"), c("SS-25-001-STD-2"), c("GS-25-001-PURPOSE-2"), AI_DEF], None,
  ["None of the seven documents uses the terms 'agentic' or 'AI agent' (OQ28). 'Machine learning' and 'Deep learning' are defined only in SS-23-002."])

# ---------------- indirect pointers ----------------
def q(i): return f"“{P[i]['text_excerpt']}”"
PTR = []
def PT(pid, element_ids, show_when, text, ids, employee_note):
    PTR.append(dict(id=pid, element_ids=element_ids, show_when=show_when, as_written=text, employee_pointer=employee_note, provision_ids=ids, citations=list(dict.fromkeys(cite(P[i]) for i in ids))))
PT("P_AGENCY_RESTRICTIONS", ["O_AGENCY_RESTRICTIONS"], ALWAYS, q("SS-25-001-STD-4"), ["SS-25-001-STD-4", "SS-25-001-STD-5"], "Check with your agency whether it has additional restrictions on GenAI use. The documents do not name an office.")
PT("P_ATTRIB_FORMAT", ["O_ATTRIB_FORMAT"], ALWAYS, "“Agencies must use standardized attribution formats that include:” “Name of the GenAI tool used”; “Summary of the prompt or task”; “Identity of the staff who reviewed or edited the content”.", R(SS25, "1.2", [2, 3, 4, 5]), "Check with your agency for its standardized attribution format. The documents do not name an office.")
PT("P_AGENCY_GUIDELINES", ["O_AGENCY_OUTPUTS"], ALWAYS, f"Agencies shall: {q('SS-23-002-5-4')} and {q('SS-23-002-5-5')}", ["SS-23-002-5-4", "SS-23-002-5-5"], "Check with your agency for its own guidelines on using AI-generated outputs and for who reviews and approves AI-generated content (the standard says 'the business owner or designated personnel').")
PT("P_RECORDS", ["O_RECORDS_AGENCY", "O_AGENCY_OUTPUTS"], ALWAYS, f"Agencies shall: {q('SS-25-001-1.7-2')}; {q('SS-25-001-1.7-3')}; {q('SS-25-001-1.7-4')}. Agencies shall also be {q('SS-23-002-5-7')}", ["SS-25-001-1.7-2", "SS-25-001-1.7-3", "SS-25-001-1.7-4", "SS-23-002-5-7"], "Check with your agency how it classifies, stores and retains GenAI prompts, responses and outputs. The documents do not name an office.")
PT("P_INCIDENTS", ["O_INCIDENTS", "O_AGENCY_DATA"], ALWAYS, f"{q('SS-25-001-4.0-2')} {q('SS-23-002-8-2')} Agencies' data protection duties include {q('SS-23-002-6-6')}", ["SS-25-001-4.0-2", "SS-23-002-8-2", "SS-23-002-6-6"], "These reporting duties are written for agencies; the documents do not say whom an individual employee notifies. Check with your agency how to raise an incident or suspected misuse.")
PT("P_COMPLIANCE_CONTACT", ["O_INCIDENTS"], ALWAYS, q("SS-23-002-8-1"), ["SS-23-002-8-1"], "Your agency is to have a staff member designated for compliance with SS-23-002. The documents do not say who that is in your agency.")
PT("P_DATA_AUTHORITY", ["O_AGENCY_DATA"], YN("F_DATA"), f"Agencies shall ensure that {q('SS-23-002-6-2')} and that it {q('SS-23-002-6-3')}. {q('SS-25-001-1.3-1')}", ["SS-23-002-6-2", "SS-23-002-6-3", "SS-25-001-1.3-1"], "SS-23-002 refers to an 'appropriate agency authority' for authorizing use of confidential, sensitive or personal data with AI tools. The documents do not say who that is.")
PT("P_HIGH_RISK", ["O_AGENCY_RISK", "O_AGENCY_OUTPUTS"], [{"F_DECISION": ["yes", "not_sure"]}, {"F_TASK": ["other", "not_sure", "policy_drafting", "education_training"]}], f"{q('SS-25-001-3.0-4')} {q('SS-25-001-1-2')}", ["SS-25-001-3.0-4", "SS-25-001-1-2"], "Check with your agency about its risk assessment and human-in-the-loop review workflow for this use; SS-25-001 says agencies should consult the GTA Office of Artificial Intelligence for novel, high-risk, or ambiguous use cases.")
PT("P_PROCUREMENT", ["O_PROCURE_AGENCY", "O_AGENCY_RESTRICTIONS"], PRO, f"{q('PS-23-001-POLICY-1')} {q('SS-23-002-3-1')} {q('SS-25-001-1.5-4')} {q('SS-25-001-STD-3')}", ["PS-23-001-POLICY-1", "SS-23-002-3-1", "SS-25-001-1.5-4", "SS-25-001-STD-3"], "Check with your agency how it submits AI tools to GTA for review before procurement. The documents describe more than one route (see conflict C08).")
PT("P_CONTRACTS", ["O_CONTRACTS_VENDORS"], PRO, "“Service and technology contracts shall provide standards of third-party provider and their partners or subcontractors, including:” “Adhering to GTA Policies, Standards and Guidelines (PSGs)”; “Adhering to NIST guidance, risk management frameworks and standards for responsible artificial intelligence practices.”; and providing the contractors' Responsible AI framework and policies to GTA.", R(SS23, "3", [4, 5, 6]), "Check with your agency's procurement process for the contract standards SS-23-002 section 3 lists. The documents do not name an office.")
PT("P_SANDBOX", ["O_SANDBOX"], BLD, f"“To participate in the Horizons Innovation Lab, agencies shall:” {q('SS-25-001-2.2-1')} {q('SS-25-001-2.5-1')}", ["SS-25-001-2.2-1", "SS-25-001-2.5-1"], "Sandbox participation is arranged by the agency with GTA's Horizons Innovation Lab; check with your agency whether your project is or should be in the Sandbox.")
PT("P_MEETINGS_AGENCY", ["O_MEET_AGENCY"], T("meetings"), q("GS-25-001-MEET-6"), ["GS-25-001-MEET-6"], "Check with your agency for its rules on AI tools in virtual meetings. The documents do not name an office.")
for p in PTR:
    for e in p['element_ids']: assert EL[e]['tier'] == 'out_of_scope_for_employee'
for e in ELEMENTS:
    e['indirect_pointer_ids'] = [p['id'] for p in PTR if e['id'] in p['element_ids']]

# ---------------- conflicts / references / open questions ----------------
CPLAIN = {
 "C01": "The 2025 generative AI document labels itself both a policy (PS-25-001) and a standard (SS-25-001); the documents do not settle which it is.",
 "C02": "PS-23-001 cites a standard numbered SS-23-001; the standard in the document set is numbered SS-23-002.",
 "C03": "PS-23-001 defines 'Artificial Intelligence' in the words the other documents use for 'Generative AI', so the reach of its procurement-review rule is unclear.",
 "C04": "The documents disagree on whether personal or sensitive data can ever be entered and who can approve it: GTA's Office of Artificial Intelligence (SS-25-001 1.3), an 'appropriate agency authority' (SS-23-002 6), the Georgia Technology Authority generally (GS-25-001 rubric), or no stated exception (other GS-25-001 passages and the SS-25-001 table).",
 "C05": "SS-25-001 prohibits personal email addresses unless the agency's technology leadership authorizes it; GS-25-001 says to avoid personal accounts and states no exception.",
 "C06": "SS-25-001 says any content 'generated or assisted by GenAI shall be clearly labeled'; GS-25-001 says citation 'isn't necessary' when AI only helped you generate your own content and ideas, yet elsewhere asks you to cite brainstormed and edited content.",
 "C07": "The two 2025 documents list different contents for an attribution: SS-25-001 lists tool name, prompt summary and reviewer identity; GS-25-001 lists model name, prompt, company and date.",
 "C08": "Pre-procurement review is described three ways: a web form at ai.georgia.gov (SS-25-001), a Business Solutions Review form sent by email (SS-23-002), and submission to GTA with no channel named (PS-23-001).",
 "C09": "Agencies are told to report AI tools to GTA in two ways: the annual STARR report (SS-25-001) and email (SS-23-002).",
 "C10": "Incident and misuse reports go to different recipients in different documents, and only SS-25-001 sets a deadline (48 hours).",
 "C11": "The 2023 guideline words some human-involvement principles with 'shall' or 'must'; the later wording of the same principles uses 'should'.",
 "C12": "GS-25-001 mentions 'regularly clearing chats' while other provisions call for keeping records of prompts and responses; the documents do not say how these fit together.",
 "C13": "SS-25-001 says review is by 'qualified personnel' before use 'in any official capacity'; SS-23-002 says agencies ensure review and approval 'by the business owner or designated personnel' before content is 'published or used for decision-making'.",
}
C_EXTRA = {"C01": ["U_SCOPE"], "C07": ["C_CITE_INFORMAL", "C_CITE_OFFICIAL", "O_ATTRIB_FORMAT"], "C06": ["C_CITE_NONE", "C_CITE_REQUIRED", "U_TRANSPARENCY"], "C02": ["O_PROCURE_AGENCY"], "C10": ["O_INCIDENTS"], "C12": ["O_RECORDS_AGENCY"], "C13": ["O_AGENCY_OUTPUTS"], "C04": ["C_DATA_UNSURE", "O_AGENCY_DATA"], "C11": ["U_PRINCIPLES"]}
CONF = []
for cf in inv['conflicts']:
    cf = dict(cf)
    aff = list(dict.fromkeys([elem_of[i] for i in cf['provisions']] + C_EXTRA.get(cf['id'], [])))
    cf['plain_statement'] = CPLAIN[cf['id']]; cf['affected_element_ids'] = aff; cf['carried_from'] = "stage1"
    CONF.append(cf)
OQ_EL = {"OQ01": ["U_SCOPE"], "OQ02": ["U_SCOPE"], "OQ03": ["U_SCOPE"], "OQ04": ["U_SCOPE", "U_CREDENTIALS"], "OQ05": ["U_LABEL", "C_CITE_REQUIRED", "C_CITE_INFORMAL", "C_CITE_OFFICIAL", "C_TASK_MEDIA", "U_PRINCIPLES"],
 "OQ06": ["U_SCOPE"], "OQ07": ["U_APPROVED_TOOLS", "C_PROCURE_APPROVAL"], "OQ08": ["O_AGENCY_RESTRICTIONS"], "OQ09": ["C_DATA", "C_DATA_UNSURE", "U_REVIEW", "U_DATA_CARE", "U_CREDENTIALS"],
 "OQ10": ["C_TASK_SUMMARY", "C_TASK_PUBLIC", "C_TASK_CODING", "C_TASK_DATA_ANALYSIS", "C_TASK_POLICY", "C_TASK_EDU", "C_TASK_CHATBOT", "C_TASK_MEDIA", "C_TASK_TRANSLATION", "C_TASK_LEGAL", "C_DECISIONS", "U_APPROVED_TOOLS"],
 "OQ11": ["U_LABEL", "O_ATTRIB_FORMAT"], "OQ12": ["C_MEETINGS", "C_MEETING_HOST", "C_TASK_SUMMARY"], "OQ13": ["C_DECISIONS"], "OQ14": ["U_PRINCIPLES"], "OQ15": ["U_PRINCIPLES"], "OQ16": ["C_CITE_OFFICIAL"], "OQ17": ["O_PROCURE_AGENCY"],
 "OQ18": ["U_CONSEQUENCES"], "OQ19": ["O_INCIDENTS"], "OQ20": ["U_TRAINING"]}
OQ = []
for o in inv['open_questions']:
    o = dict(o); o['affected_element_ids'] = OQ_EL[o['id']]; o['carried_from'] = "stage1"; OQ.append(o)
def NQ(i, qn, why, els): OQ.append(dict(id=i, question=qn, why_undecided=why, documents=[], affected_element_ids=els, carried_from="stage2 (new)"))
NQ("OQ21", "Are the guiding-principle items out of scope for an individual employee, or do they bind employees because GS-25-001 says employees 'should abide by' them?", "171 provisions across 5GP, GS-23-001 and the GS-25-001 reproduction were placed in the out_of_scope_for_employee tier because the principles say they are 'intended to guide state agencies' and most items describe designing, testing or governing systems. The only employee-addressed sentence (GS-25-001-PURPOSE-3) is kept as an umbrella element that names the five principles. If the reviewer reads GS-25-001 as binding employees to each item, these elements would move to the umbrella or conditional tier.", ["U_PRINCIPLES", "O_PRINC_INTRO", "O_PRINC_I", "O_PRINC_II", "O_PRINC_III", "O_PRINC_IV", "O_PRINC_V"])
NQ("OQ22", "Should the procurement guideline (GS-25-002) be shown to an employee who works on an AI procurement?", "Its Purpose addresses 'state agencies', but its items are instructions to whoever prepares or evaluates the RFP and refer to 'your team'. It was placed as conditional on the employee doing that work. One item (GS-25-002-PREP-10-2) is addressed to 'The vendor' and is kept inside the same element as RFP content.", ["C_PROC_PRINCIPLES", "C_PROC_PREP", "C_PROC_EVAL"])
NQ("OQ23", "Is one task per run acceptable, and are prohibitions that sit in one table row limited to that row?", "The task fact offers one choice per run; an employee whose use spans several tasks has to run the tool once per task. Some table prohibitions read generally but sit in one row, for example 'Do not use GenAI to make legal, disciplinary, or eligibility decisions' under Policy drafting support and 'Don’t use GenAI to analyze or process personally identifiable or regulated data' under Data analysis & reports. The first was also tied to the decisions-about-people fact; the second is shown only for the data-analysis task (the general data rules cover the same ground).", ["C_DECISIONS", "C_TASK_DATA_ANALYSIS", "C_TASK_POLICY", "C_TASK_EDU"])
NQ("OQ24", "Should the data-entry prohibitions be shown to every employee rather than only to those who answer yes or not sure?", "The prohibitions on entering personal, sensitive or confidential information were placed as conditional because their trigger is the kind of data entered. An employee who answers 'No' does not see them; the umbrella tier still shows data minimization and data protection. Moving C_DATA to the umbrella tier would remove the data question's effect on that element.", ["C_DATA", "U_DATA_CARE"])
NQ("OQ25", "Should 'for state business' and 'used in any official capacity' be separate questions?", "The credential rule applies 'for state business' and the review rule applies 'before being used in any official capacity'. Neither term is defined (OQ09) and the tool is for work use, so both were left inside umbrella statements with the condition quoted rather than turned into facts.", ["U_CREDENTIALS", "U_REVIEW"])
NQ("OQ26", "Is it acceptable that training (SS-23-002 section 7) is shown to every employee?", "Section 7 binds 'All users of AI systems'. It was placed in the umbrella tier on the reading that a GenAI tool is an AI system under the standard's definitions; the standard does not say so in terms.", ["U_TRAINING"])
UNRES = [dict(u, carried_from="stage1") for u in inv['unresolved_references']]
UNRES.append(dict(id="UR31", reference="Agency-level rules the documents tell agencies to create: additional restrictions (SS-25-001 Standard), standardized attribution formats (SS-25-001 1.2), human-in-the-loop review workflows (SS-25-001 1), guidelines for responsible use of AI-generated outputs (SS-23-002 5(e)), contingency plans (SS-23-002 10)", kind="agency documents", cited_in=["SS-25-001 Standard p.2; 1 p.2; 1.2 p.2", "SS-23-002 5(e) p.9; 10 p.14"], note="Each indirect pointer sends the employee to one of these; none is in the attached set.", carried_from="stage2 (new)"))

tiers = collections.Counter(e['tier'] for e in ELEMENTS)
ptier = collections.Counter(EL[elem_of[i]]['tier'] for i in P)
unspec = [i for i in P if P[i]['addressee'] == 'unspecified']
unspec_by = collections.Counter(EL[elem_of[i]]['tier'] for i in unspec)
GEN_ONLY_DOCS = [SS25, GS25]; OTHER_EXCEPTIONS = ["GS-25-001-SAFE-8"]
def reaches_other(i): return P[i]['doc_id'] not in GEN_ONLY_DOCS or i in OTHER_EXCEPTIONS
for e in ELEMENTS:
    for st in e['statements']: st['other_ai_provision_ids'] = [i for i in st['provision_ids'] if reaches_other(i)]
for p in PTR: p['other_ai_provision_ids'] = [i for i in p['provision_ids'] if reaches_other(i)]
DOCNAME = lambda i: P[i]['doc_id'] if P[i]['doc_id'] != GP5 else "5 Guiding Principles"
def verbatim(ids):
    parts = []
    for i in ids:
        lead = P[i]['lead_in_excerpt']
        mw = P[i]['modal_as_written']
        tag = f" [modal as written: {mw}]" if "(" in mw else ""
        parts.append(f"{DOCNAME(i)} says: " + (f"“{lead}” … " if lead else "") + f"“{P[i]['text_excerpt']}”" + tag)
    return "; ".join(parts)
for e in ELEMENTS:
    for st in e['statements']:
        oid = st['other_ai_provision_ids']
        st['other_ai_summary'] = st['summary'] if oid == st['provision_ids'] else (verbatim(oid) if oid else None)
        st['other_ai_citations'] = list(dict.fromkeys(cite(P[i]) for i in oid))
for p in PTR:
    oid = p['other_ai_provision_ids']
    p['other_ai_as_written'] = p['as_written'] if oid == p['provision_ids'] else (verbatim(oid) if oid else None)
    p['other_ai_citations'] = list(dict.fromkeys(cite(P[i]) for i in oid))
AI_TYPE_RULE = collections.OrderedDict(
  rule="When F_TYPE is 'other', a provision is shown only if it is in other_ai_reaches; an element or pointer with no such provision is not shown, and a statement shows only those provisions. For every other F_TYPE value all provisions are in scope. When F_TYPE is 'none', nothing is shown except not_ai_outcome.",
  generative_only_documents=GEN_ONLY_DOCS,
  generative_only_basis=[c("SS-25-001-STD-2"), c("GS-25-001-PURPOSE-2")],
  other_ai_exceptions=[dict(id="GS-25-001-SAFE-8", basis="The provision names 'other automated decision-making systems': " + c("GS-25-001-SAFE-8"))],
  other_ai_reaches="Every provision whose doc_id is not in generative_only_documents, plus other_ai_exceptions. Reading chosen: strict (OQ27).",
  not_ai_outcome=collections.OrderedDict(
    text="Every document in this set is about artificial intelligence, so none of their provisions apply to technology that does not use AI. This tool has no results for it.",
    citations=[AI_DEF],
    unresolved_references=["UR02", "UR03"],
    unresolved_note="The documents cite other GTA policies that are not in this set, including PM-04-001 and PS-08-005 (unresolved references UR02, UR03). This tool does not describe them."),
  other_note=collections.OrderedDict(
    text="The two 2025 documents say they cover generative AI: SS-25-001 says “State government employees shall follow this standard when using commercial GenAI solutions” and GS-25-001 says “These guidelines apply to all forms of generative AI”. This result shows only provisions from the five documents that cover AI in general, plus one GS-25-001 provision that names “other automated decision-making systems”. Whether other provisions in the 2025 documents reach non-generative AI is open question OQ27. None of the seven documents mentions AI agents (OQ28). The documents define generative AI as “tools or systems used to create models that can generate new and original content, such as images, music, or text, based on patterns and examples from existing data”; if your agent creates content like that, choose Generative AI instead.",
    citations=[c("SS-25-001-STD-2"), c("GS-25-001-PURPOSE-2"), c("GS-25-001-SAFE-8"), GEN_DEF]))
NQ("OQ27", "Do provisions in SS-25-001 and GS-25-001 that say 'AI' rather than 'GenAI' reach non-generative AI?", "Both documents state a generative-AI scope (SS-25-001-STD-2; GS-25-001-PURPOSE-2), but some of their provisions say only 'AI', and GS-25-001-SAFE-8 names 'other automated decision-making systems'. The tool takes the strict reading: on the 'other AI' branch it shows only provisions from the five general-AI documents plus GS-25-001-SAFE-8.", ["U_SCOPE", "U_HUMAN", "U_APPROVED_TOOLS", "U_CREDENTIALS", "U_REVIEW", "U_LABEL", "U_TRANSPARENCY", "U_DATA_CARE", "U_BIAS", "C_DATA", "C_DECISIONS"])
NQ("OQ28", "Is an AI agent 'Generative AI' under the documents' definition?", "No document uses the terms 'agentic' or 'AI agent'. By the project owner's decision (21 Nov 2026) the tool groups AI agents with 'Other AI', so an agent is shown only the general-AI provisions unless the user chooses Generative AI. The note on that branch quotes the generative AI definition. Two GenAI-document provisions speak to autonomy and are therefore not shown on that branch: GS-25-001-RUBRIC-2 and SS-25-001-3.0-TABLE-6.", ["U_SCOPE", "U_HUMAN"])
NQ("OQ29", "Does PS-23-001 reach non-generative AI tools, given that its own definition of 'Artificial Intelligence' uses the generative-content wording?", "See conflict C03. The tool shows PS-23-001 provisions on the 'other AI' branch because its title and policy text say 'AI'; under its own definition it might cover generative tools only.", ["U_SCOPE", "C_PROCURE_APPROVAL"])
NQ("OQ30", "Does the SS-25-001 'Constituent service' row apply to chatbots used only by state staff?", "The row's examples are constituent-facing ('support FAQ responses', 'Don’t allow GenAI chatbots to answer legal, medical, or emergency questions'). It sits in C_TASK_CHATBOT, which is shown for both public and staff-only chatbots, as before the chatbot answer was split.", ["C_TASK_CHATBOT"])
out = collections.OrderedDict(elements=ELEMENTS, facts=FACTS, indirect_pointers=PTR, conflicts=CONF, unresolved_references=UNRES, open_questions=OQ, ai_type_rule=AI_TYPE_RULE)
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.load(open(OUT, encoding='utf-8'))
print("elements by tier", dict(tiers)); print("provisions by tier", dict(ptier), sum(ptier.values()))
print("unspecified addressee:", len(unspec), dict(unspec_by), "undecidable: 0")
for f in FACTS: print(f['id'], [(v['value'], len(v['activates'])) for v in f['values']])
print("pointers", len(PTR), "conflicts", len(CONF), "unres", len(UNRES), "oq", len(OQ))
