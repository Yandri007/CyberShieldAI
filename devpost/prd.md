---
doc: prd
status: approved
---

# CyberShield AI — Product Requirements

A polished, guided cybersecurity self-assessment that helps small-business owners understand their risks and choose what to improve first.

Source: `scope.md > The Unique Kernel`, `Who It's For`, `The Core Loop`, `What "Working" Looks Like`, and `The POC Boundary`.

## The Core Journey

1. **Arrive.** A small-business owner sees what CyberShield AI does, that the assessment takes about 3–5 minutes, and that it produces a security overview and three prioritized actions. They can start without creating an account.
2. **Assess.** The owner answers eight concise, plain-language questions, one focused question for each agreed security area. They can go back, see progress, and choose **Yes**, **No**, or **Not sure** where appropriate. They must answer all questions before analysis.
3. **Understand the results.** CyberShield AI calculates the 0–100 score from the fixed rules, assigns a status, and ranks findings by potential impact and answer. The dashboard labels the number as a self-reported security-controls score: it reflects the owner’s answers, is not a measured or technically verified security level, and does not imply that systems were scanned or audited.
4. **Get guidance.** From the dashboard, the owner selects **Get AI Guidance** (working button copy). The app presents a structured action plan connected to the findings; it does not open a chatbot.
5. **Act.** The owner sees up to three top findings and their related actions. Each action explains what to do, why it matters, which risk it addresses, and how to get started. The owner leaves with clear next steps.

## Screens and Layout

### Landing

A simple, professional introduction with the main message: **“Understand your business’s cybersecurity risks and know what to fix first.”** It explains that the assessment takes 3–5 minutes, needs no cybersecurity expertise, and returns a personalized security overview and prioritized actions. A short **Assess → Understand → Act** visual and prominent **Start Assessment** button set the path. No account or login is required.

### Assessment

Show one question at a time, with a **Question N of 8** progress indicator, answer choices, and a short explanation/example when a term may be unfamiliar. **Next** advances; **Back** returns without discarding an answer. After question eight, **Analyze My Security** submits the completed answers.

The eight assessment areas and draft question intents are:

| Area | Draft question intent | Equal score contribution | Potential impact and rationale |
|---|---|---:|---|
| Password security | Are business passwords unique rather than reused across accounts? | 12.5 points | **High:** reused or weak passwords can enable unauthorized account access. |
| Multi-factor authentication | Is an extra sign-in verification step enabled for important business accounts? | 12.5 points | **High:** without MFA, a compromised password can more easily lead to account takeover. |
| Backups | Are important business files backed up regularly in a way they can be recovered? | 12.5 points | **High:** missing or unreliable backups can cause data loss and difficult recovery. |
| Software and system updates | Are business devices and software kept up to date with security updates? | 12.5 points | **Moderate:** outdated software increases exposure to known vulnerabilities. |
| User access and permissions | Do employees have access only to the business accounts and information they need? | 12.5 points | **High:** excessive access can expose important business information. |
| Network/Wi-Fi security | Is business Wi-Fi protected from unauthorized use? | 12.5 points | **Moderate:** weak network security can expose connected devices and business traffic. |
| Device protection | Are business devices protected against malware and other compromise? | 12.5 points | **Moderate:** insufficient protection can put an individual device at risk. |
| Employee security practices | Do employees know how to identify and report suspicious messages? | 12.5 points | **Moderate:** poor habits can increase phishing and credential-theft risk. |

These are concise draft prompts/intents for review; the learner approved the eight areas, one question per area, and the risk rationale. The final wording should stay plain and test one focused signal per question. Offer **Not sure** as an explicit choice where appropriate; never treat a blank response as **Not sure**.

### Results Dashboard

Label the number **Self-reported security-controls score** and show it prominently with its status and a short plain-language explanation. Include a clear note such as **Based on your answers—not a technical measurement or verification of your security.** A high score must not imply that the business has been technically verified. Make the top risks visually prominent, with each finding showing its area, priority/severity, and why it matters. A clear **Get AI Guidance** button continues to the action plan.

### AI Guidance and Action Plan

Present a structured continuation of the dashboard, not a conversational interface. Show up to three prioritized findings and connect each one to its explanation and action. Every action includes:

- **What to do:** a practical improvement.
- **Why it matters:** a plain-language explanation.
- **Risk addressed:** the specific finding that prompted it.
- **How to get started:** a realistic first step.

Before the AI call, the application determines the score, status, impact severity, finding ranking, and risk-to-action mapping from its rules. It sends the structured results and relevant assessment answers to AI as context. AI may explain those results and personalize the application-selected recommendations, but it must not calculate or revise the score, severity, ranking, action mapping, or findings.

## Look and Feel

Use a modern cybersecurity identity without the stereotypical hacker aesthetic. The direction is deep navy or blue, lighter blue/cyan accents, and white/light-gray surfaces. Use green, amber, and red for risk levels, with readable text and clear hierarchy. The landing screen and dashboard should feel polished, professional, clean, and reassuring. Show the score, top risks, and actions at a glance without overwhelming the owner. Codex may select the exact palette and typography within this direction, prioritizing readability and accessibility.

## Features and Behavior

### Guided Assessment

- The assessment contains exactly eight focused questions, one for each area above, and is designed for a 3–5-minute completion.
- Questions use simple language and clear choices. Use **Yes**, **No**, and **Not sure** where appropriate; provide a brief helper explanation for unfamiliar terms.
- **Next** and **Back** move through the questions while preserving selected answers. The progress indicator uses the question number out of eight.
- If the owner tries to continue past an unanswered question, identify it, highlight it, and show: **“Please answer this question to continue.”**
- If **Analyze My Security** is selected with any unanswered item, return to the first unanswered question and highlight it. Do not silently convert blank answers to **Not sure**.
- **Acceptance criteria:** the owner can answer all eight, revisit and change answers, see their progress, and cannot submit a partial assessment.

### Transparent Score and Risk Priorities

Each of the eight areas contributes equally to the overall posture score:

| Answer | Points for that area | Meaning |
|---|---:|---|
| Yes | 12.5 | The owner reports the control is in place. |
| Not sure | 6.25 | Partial credit; the control needs verification. |
| No | 0 | A confirmed gap. |

Sum the eight area values for a score from 0 to 100. The rules, not AI, calculate the score. Use these status bands:

| Score | Status | Plain-language meaning |
|---:|---|---|
| 80–100 | Strong | Most important controls appear to be in place. |
| 50–79 | Needs Attention | Meaningful gaps should be addressed. |
| 0–49 | High Risk | Several important controls appear to be missing or need urgent attention. |

Risk priority is separate from the equal-weight overall score. A risk’s potential-impact band and answer determine its priority:

| Area(s) | Potential impact |
|---|---|
| Backups, password security, MFA, user access and permissions | High |
| Software/system updates, network/Wi-Fi, device protection, employee practices | Moderate |

| Answer and impact | Finding and priority |
|---|---|
| Yes | No significant finding for that area (low/no priority). |
| No + high impact | High-priority confirmed gap. |
| No + moderate impact | Medium-priority confirmed gap. |
| Not sure + high impact | High-priority verification finding; do not claim the control is missing. |
| Not sure + moderate impact | Medium-priority verification finding; do not claim the control is missing. |

Rank findings by priority first. Within the same priority, place confirmed **No** findings before **Not sure** verification findings. For any remaining tie, use the fixed assessment area order: Password security, MFA, Backups, Software and system updates, User access and permissions, Network/Wi-Fi security, Device protection, Employee security practices. The dashboard shows the first three findings most prominently and can show remaining findings below them. Each finding explains its area, priority, and potential impact. Identical answers must always produce the same top-three list.

- **Acceptance criteria:** the same eight answers always produce the same score, priority labels, and ordered top-three list; the displayed score equals the sum of the stated points; a **Not sure** result is labeled as uncertainty/verification, not a confirmed vulnerability; AI output cannot change the score, severity, ranking, or risk-to-action mapping.

### Results and Action Plan

- The results dashboard displays the self-reported security-controls score, status label, explanation, and most important risks without requiring the owner to read dense technical text. It says the result is based on the owner’s answers, not a measured or verified security level.
- The owner can continue to **Get AI Guidance**. The guidance presents up to three prioritized risks again, each tied to a plain-language explanation and corresponding practical action.
- The action plan includes what to do, why it matters, the risk addressed, and how to get started. Actions follow the structured risk priorities.
- If there are fewer than three findings, show only actual findings on the dashboard. The plan may use remaining action positions for preventive or verification recommendations, clearly labeled as such; do not create extra risks to fill space.
- If there are no findings, show a positive result and explain that no significant gaps were identified from the owner’s self-reported answers. The action plan may recommend maintaining current practices and sensible prevention, without presenting these as remediation for invented risks.
- **Acceptance criteria:** every remediation action links to an actual finding; any preventive action is labeled; the results make clear that they are based on self-report, not an audit.

### AI Guidance and Fallback

- Before calling AI, the application fixes the score, findings, severity, ranking, and risk-to-action mapping. AI receives those structured results and relevant assessment answers as context.
- AI output is structured, not chat. It may explain and personalize the application-selected actions, but it cannot create findings, change the score/severity/ranking, or select a different risk-to-action mapping.
- If AI guidance is unavailable, keep the rules-based score, categories, findings, and priorities visible. Show: **“AI guidance is temporarily unavailable, but your security assessment is ready.”**
- In that case, show predefined, risk-linked fallback actions and a clear option to retry AI guidance. The fallback provides useful next steps without claiming AI personalization.
- **Acceptance criteria:** an AI failure never removes the assessment results or leaves the owner without an action; retrying is available; fallback actions correspond to identified risks or are labeled preventive; AI output cannot modify rule-based results or their mapped actions.

## States and Boundaries

- **First use:** the landing screen explains the service and presents **Start Assessment**; no account or login is required.
- **Question unanswered:** highlight the missing item and explain that it needs an explicit answer; return to the first missing question if analysis is attempted.
- **Not sure:** award partial score credit and create a verification finding at the area’s potential-impact priority; do not claim a vulnerability is confirmed.
- **Results with findings:** show the score/status, all applicable risk areas, and up to three top risks prominently.
- **Fewer than three findings:** show only actual findings; use clearly labeled preventive/verification actions for any remaining action positions.
- **No findings:** show a positive, self-report-qualified result and maintenance/prevention actions; never fabricate a risk.
- **AI unavailable:** preserve all rule-based results, show the supplied notice and predefined fallback actions, and offer retry.
- **Assessment basis:** the score describes self-reported controls, not a measured security level. The app does not scan systems or claim technical verification or a full audit; a high score is not proof that systems are secure.

## Product Decisions

- The POC is an eight-question assessment, one focused question per agreed area, designed for a 3–5-minute completion.
- The overall score is 0–100 with equal contribution from each area: **Yes = 12.5**, **Not sure = 6.25**, **No = 0**.
- Score bands are **80–100 Strong**, **50–79 Needs Attention**, and **0–49 High Risk**.
- Risk priorities are separate from the score and use the agreed high/moderate impact classification. **Not sure** means verification, not a confirmed gap.
- The dashboard labels the value as a self-reported security-controls score; it is not a measured or verified security level, and a high score does not imply technical verification.
- AI explains and personalizes recommendations but cannot score, change risk priorities, or add unrelated risks. The application fixes the risk-to-action mapping before the AI call.
- The experience is direct and login-free; AI guidance is structured rather than a chatbot. Tied findings sort by priority, confirmed No before Not sure, then the fixed assessment area order; this rule carries into the technical specification.
- The no-risk case must be positive and useful without fabricated findings.
- Codex may choose exact colors and typography within the learner’s visual direction.

## What We're Building

A polished, login-free web experience that takes a small-business owner through the landing screen, eight-question assessment, deterministic score/risk dashboard, and structured AI action plan, with clear validation, no-finding handling, and useful AI-unavailable fallback. The experience is demonstrable in about one minute after the assessment inputs are entered, while a typical owner should complete the questions in 3–5 minutes.

## Deferred From the POC

- A full cybersecurity platform or broader SaaS capability; the POC proves one self-assessment-to-action-plan journey.
- Automated system/network scanning or a full technical audit; the proof is explicitly based on self-reported answers.
- Additional questions beyond the eight-question baseline are deferred. Revisit only if one area cannot produce a meaningful risk signal with one focused question, and agree on any change before adding it.

## Possible Later Enhancements

A broader SaaS offering for small businesses, if the POC demonstrates that the assessment and prioritized actions are useful.

## Non-Goals

- Creating accounts or requiring login for this POC.
- Scanning or verifying business systems, devices, or networks.
- Letting AI calculate or modify scores, severity, or priorities.
- Building a generic cybersecurity chatbot or a complete security platform.
- Inventing risks to make the dashboard or action plan appear fuller.

## Resolved During Build Review

- Final question wording and helper text were reviewed and approved by the learner during Final Review. The eight areas, one-question-per-area baseline, answer meanings, score points, and impact bands remain as defined.
- Fallback action text for each risk was reviewed alongside the questions and helper text and approved by the learner during Final Review.
