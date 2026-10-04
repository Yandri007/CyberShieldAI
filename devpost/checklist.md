---
doc: checklist
status: approved
---

# CyberShield AI Build Checklist

Build mode: learn — after each verified slice, explain the change and key files, guide the learner through a local hands-on check, compare behavior with the PRD/spec, then commit before continuing.

## Slices

- [x] **1. You can complete the assessment and see deterministic results**
  Becomes usable: The local Django app has a polished landing screen, the eight-question guided flow, and a results dashboard whose self-reported score and ordered findings come from the Python rules.
  Why now: Project setup stays inside the first usable behavior. This delivers the unique kernel early: answers produce transparent, repeatable results before any AI is involved, and the learner can give feedback on the main assessment journey.
  PRD ref: `prd.md > The Core Journey`; `prd.md > Screens and Layout > Landing`; `prd.md > Screens and Layout > Assessment`; `prd.md > Screens and Layout > Results Dashboard`; `prd.md > Features and Behavior > Guided Assessment`; `prd.md > Features and Behavior > Transparent Score and Risk Priorities`
  Spec ref: `spec.md > Stack`; `spec.md > Where It Runs and How Someone Tries It`; `spec.md > Components > Landing and assessment interface`; `spec.md > Components > Django request views`; `spec.md > Components > Assessment catalog`; `spec.md > Components > Deterministic assessment engine`; `spec.md > Components > Results renderer and retry control`; `spec.md > Data Model`; `spec.md > File Structure`; `spec.md > API Contracts > Same-origin assessment analysis`
  Build: Use the verified Python 3.14.8 runtime to create the virtual environment with `py -3.14 -m venv .venv`, then bootstrap the minimal Django project as part of this slice. Install Django 5.2.8 or later in the 5.2 LTS series. Extend `.gitignore` for the virtual environment and Python bytecode. Add the question/impact catalog, exact deterministic scoring and tie-break rules, same-origin analysis endpoint, landing page, guided wizard, browser-memory answers, professional dashboard, and self-report disclaimer. Do not add a database, authentication, React, or permanent answer storage.
  Verify (mechanical): Run `python manage.py check`; run the app and confirm the landing page responds. In one-off Django shell checks, verify each answer gives Yes `12.5`, Not sure `6.25`, and No `0`; all-Yes yields `100 / Strong`, all-Not-sure `50 / Needs Attention`, and all-No `0 / High Risk`; and the sample in `spec.md > API Contracts > Same-origin assessment analysis` yields `62.5` with order `backups, mfa, employee_practices, wifi_security`. Check high before medium, confirmed No before Not sure within a priority, and fixed area order when those tie. Check missing/blank and invalid answers are rejected and identify the first unanswered area. Repeating the same valid input must produce identical results. No test framework is needed.
  Learner check: Open the local app, start the assessment, answer all eight questions, go Back and change an answer, confirm unanswered questions are highlighted, then analyze. Check that the displayed score is self-reported, the top risks are easy to spot, and the sample answers produce 62.5.
  Commit: `Build guided assessment and deterministic dashboard`

- [x] **2. You can get a risk-linked rules-based action plan**
  Becomes usable: The dashboard continues to a structured plan with predefined remediation, verification, or clearly labeled preventive actions tied to the real findings.
  Why now: The app gains useful next steps even with no API key or network access. This makes the full assessment-to-action journey dependable before adding the optional AI explanation layer.
  PRD ref: `prd.md > Screens and Layout > AI Guidance and Action Plan`; `prd.md > Features and Behavior > Results and Action Plan`; `prd.md > Features and Behavior > AI Guidance and Fallback`; `prd.md > States and Boundaries`
  Spec ref: `spec.md > Components > Risk-linked action catalog`; `spec.md > Components > Provider-neutral AI guidance service`; `spec.md > API Contracts > Same-origin guidance request`; `spec.md > Data Model`; `spec.md > Important Failure Modes`
  Build: Add the fixed risk-to-action and fallback catalogs, a provider-neutral guidance service, and the guidance endpoint. Recompute results from the posted answers, select only actions linked to real findings, use labeled preventive/maintenance actions only where the PRD allows, and render the full plan without calling an AI provider.
  Verify (mechanical): Run `python manage.py check`; use the local guidance endpoint with several findings and confirm every remediation/verification action ID and risk ID maps to an actual finding. Confirm any action without a finding is explicitly typed and labeled preventive/maintenance, including when there are one or two findings. With all-Yes answers, confirm a positive result, no invented finding, and only labeled preventive/maintenance actions.
  Learner check: From the dashboard, open the action plan and trace each action to its risk. Then try an all-Yes assessment and check that it does not invent a risk to fill the plan.
  Commit: `Add structured fallback action plan`

- [x] **3. AI can explain the fixed plan, with fallback always available**
  Becomes usable: The same action-plan flow can return concise, answer-aware AI explanations when configured; missing keys, API failures, or unusable output leave the deterministic results and predefined plan intact.
  Why now: The owner already has a complete rules-based journey. The OpenAI adapter can now enhance explanations behind the provider-neutral service without taking control of score, severity, priority, order, or action mapping.
  PRD ref: `prd.md > Features and Behavior > AI Guidance and Fallback`; `prd.md > Features and Behavior > Results and Action Plan`; `prd.md > States and Boundaries`
  Spec ref: `spec.md > Components > Provider-neutral AI guidance service`; `spec.md > Components > OpenAI adapter`; `spec.md > Components > Results renderer and retry control`; `spec.md > API Contracts > Same-origin guidance request`; `spec.md > API Contracts > OpenAI Responses API`; `spec.md > External Services and Cost Check`; `spec.md > Important Failure Modes`
  Build: Add the OpenAI adapter behind the service contract, read the key only from the server environment, request strict structured output limited to approved style identifiers and Django-selected action IDs, set `store=false`, validate output, render all user-facing prose from Django-owned catalogs, preserve server order, and fall back on every failure. Add the guidance retry control. Do not make a live API request until the learner has checked available credits and chosen to enable it.
  Verify (mechanical): Run `python manage.py check` and `python -m compileall cybershield assessment`. With a stub/capture adapter, confirm Django sends only its structured answers, canonical score/findings/priorities, and preselected actions—no identity or free text. The schema and service must reject prose and attempts to add/change score, severity, priority, ranking, risk IDs, or action IDs; confirm fallback and unchanged displayed server values/order. Confirm approved style IDs only select fixed Django copy. With `OPENAI_API_KEY` unset, confirm the rules-based assessment, fixed plan, fallback message, and retry remain available. Confirm the key is absent from browser responses. Only verify a live request after the learner checks credits and chooses to enable one; never print or commit the key.
  Learner check: With no key configured, request guidance and confirm the action plan still appears with the temporary-unavailability message. If live guidance is enabled after the separate credit check, compare its explanation with the fixed risks/actions and confirm it has not changed their order or severity.
  Commit: `Add constrained OpenAI guidance with fallback`

## Hands-on Checkpoints

- [x] Early usable behavior explored — after slice 1, review the landing, question flow, score, and risk hierarchy; use feedback to shape the action-plan presentation.
- [x] Final kick-the-tires exploration and feedback completed — after slice 3, explore the complete assessment, action plan, fallback, and (if enabled) live guidance.

## Final Review

- [x] Medium AI-output issue resolved — strict style identifiers only; Django renders all displayed prose from fixed catalogs, and invalid output falls back.
- [x] Low copy-review issue resolved — learner reviewed and approved the eight question/helper pairs, fallback actions, summaries, and unavailable notice.
- [x] Final review complete — checks pass; learner confirmed the proof of concept is ready for the ship phase on 2026-10-03.

## Code Tour and App Map

- [x] Learning activity complete — on 2026-10-04, learner traced the approved Backups = No example from its catalog entry through the finding, assessment, selected action, and browser rendering.
- [x] Optional edit and transfer reflection addressed — learner requested no code or product changes and stated that they understand the answer-to-rendering flow; no separate transfer question was needed.
- [x] `devpost/app-map.html` generated from finished code, checked offline, and shown; includes a reference route and project-grounded practice to reuse

Activity and evidence: On 2026-10-04, learner completed the walkthrough in the local app and VS Code and reported understanding the route across catalog.py, rules.py, guidance/actions.py, and app.js.
Route and stops: Completed — catalog AREAS → rules _finding_for()/calculate_assessment() → guidance/actions.py select_actions() → app.js renderAction(). See app-map.html for the reference route.
Edit outcome: No code or product edit; learner explicitly requested none.
Reflection: Already covered — learner stated that they understand how the answer moves from area definition through finding, action selection, and browser rendering. Personal note recorded only in the ignored learner profile.
Activity mode: Live local app and VS Code; learner traced the approved Backups = No example.

## Revisions

- Use the learner's already-installed Python 3.14.8 instead of asking them to maintain Python 3.13. Django 5.2.8 added official Python 3.14 support; the current OpenAI Python SDK also supports 3.14. Updated the local setup commands and first-slice runtime requirement.
- Final-review hardening: model-authored prose could contradict the canonical assessment even when its action IDs were valid. The adapter now returns only strict enum identifiers; Django renders all displayed text from approved fixed copy. Fake-adapter validation covers extra prose fields and attempts to change canonical results.
- Final Review copy sign-off: the learner reviewed and approved the implemented question/helper and fallback wording; recorded the completion in the PRD/spec and closed the Low copy-review item.
