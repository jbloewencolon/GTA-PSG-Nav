# Questions for GTA policy owners

The GTA AI Policy Check shows GTA's AI documents to state employees. Each item below is a reading the tool had to make, or a fact it could not confirm. The tool marks each one as its own choice until GTA confirms it. Provision IDs refer to `data/stage1_inventory.json`.

## 1. Which documents are current?

The 2025 documents (SS-25-001, GS-25-001, GS-25-002, all effective 1 July 2025) list the 2023 documents (PS-23-001, SS-23-002, GS-23-001) as related documents. None of the documents says it supersedes, amends or retires another. So the tool shows both sets side by side and flags where they disagree (conflicts C04, C05, C08, C09, C10, C11, C13).

- **Question:** do the 2025 documents replace any of the 2023 documents, in whole or in part? If so, which provisions no longer apply?
- **Related:** PS-23-001's review date (15 January 2025) has passed, and the copy used was captured on 21 July 2026. A web search shows a GTA page for PS-23-001 under a different address ("enterprise-generative-artificial-intelligence-acceptable-use-ps-23-001"), with wording about "AI-enabled capabilities incorporated into other technology products". The captured copy does not contain that wording. Is there a newer version of PS-23-001?

## 2. Source links for the 2025 documents

These links were found by web search and could not be opened from the build environment:

| Document | Link used |
|---|---|
| SS-25-001 Generative AI Responsible Use | https://gta-psg.georgia.gov/document/document/generative-ai-responsible-use-ss-25-001/download |
| GS-25-001 Generative AI Guidelines for Responsible Use | https://gta-psg.georgia.gov/document/document/generative-ai-guidelines-responsible-use-gs-25-001/download |
| GS-25-002 Procurement of AI Tools Guidelines | https://gta-psg.georgia.gov/document/document/procurement-ai-tools-guidelines-responsible-use-gs-25-002/download |

- **Question:** are these the official, current versions?

## 3. Guardrail posts (the tool's own values)

The page shows guardrail posts that rise with what the employee describes. The values are this tool's, not GTA's:

| If the employee says… | Posts |
|---|---|
| They will enter personal or sensitive information | 2 |
| The output feeds a decision about a person | 2 |
| The public sees the output or interacts with it | 1 |
| They are helping to buy or build an AI tool | 1 |
| AI content goes into an official document | 1 |
| Legal analysis, or AI note-taking in meetings | 1 |

Levels: Baseline rules only (0), Light (1–2), Standard (3–4), Extra (5 or more). A "Not sure" answer counts as yes.

- **Question:** are these factors and values acceptable? Should any factor be added, removed or reweighted?

## 4. Stop and Check first signs

| Sign | When | Provision quoted |
|---|---|---|
| Red: "GTA approval needed: personal or regulated data" | Generative AI, personal data | SS-25-001-1.3-2 |
| Red: "GTA approval needed: buying a GenAI product or service" | Generative AI, buying | SS-25-001-1.5-1 |
| Red: "May be prohibited: decisions about people (the documents disagree)" | Generative AI, output feeds a decision about a person | SS-25-001-3.0-TABLE-15 |
| Amber: "GTA review needed before buying an AI tool" | Other AI, buying | PS-23-001-POLICY-1 |
| Amber: "Authorization needed: personal or sensitive data" | Other AI, personal data | SS-23-002-6-2 |

- **Question (decisions about people):** the prohibition "Do not use GenAI to make legal, disciplinary, or eligibility decisions" sits in the Policy drafting row of the SS-25-001 table. GS-25-001-SAFE-9 says "an HR department may consult with AI platforms in making hiring decisions" (open question OQ13). Does the prohibition apply to every use, or only to that row? Does it cover *helping* to make a decision, or only *making* it?
- **Question (Check first):** is PS-23-001's review before procurement a step that should stop an employee until it is complete? Who is the "appropriate agency authority" in SS-23-002 §6?
- **Not included:** no provision requires a review before *building* a non-generative AI tool. SS-23-002-9-7 requires testing before deployment but names no reviewer. Is that intended?

## 5. How modal verbs were read

The tool keeps each document's wording, but it also has to group provisions under Must, Must not, Should, Should not, May or Note. These readings are recorded in the inventory (`classification_basis`):

- **"Conditional" table cells read as Must** (SS-25-001-3.0-TABLE-2, 5, 8, 11, 14, 17, 20, 23, 26, 29). The column legend is "Yellow = Caution". The cells state conditions of use, for example "Use with legal staff oversight only". **Question:** are these conditions mandatory?
- **Guideline commands without a modal verb read as Should** (about 190 provisions in GS-25-001, GS-25-002 and others), **except two "Do not" commands read as Must not:** GS-25-001-STRAT-6 ("Do not enter personal and/or sensitive data into a GenAI model") and GS-25-001-SAFE-14 ("do not provide them with confidential or private state information, or personal records"). **Question:** is that the intended strength?
