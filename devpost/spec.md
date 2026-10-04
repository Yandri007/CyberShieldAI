---
doc: spec
status: approved
---

# CyberShield AI — Technical Spec

## How This Works, In Plain Language

CyberShield AI will be one Django web app. Django serves the page and receives the answers. A small amount of regular JavaScript in the browser moves the owner through the eight questions and keeps the answers while the page is open.

When the owner analyzes the assessment, Django checks all eight answers, calculates the score, ranks findings with the approved tie-break rule, and selects the matching action cards. Those results come from Python rules, never from AI. When the owner asks for guidance, Django calculates the same results again and sends only the structured answers, findings, and already-selected actions to a small AI service. That service initially uses OpenAI, but the rest of the app speaks to the service through a provider-neutral shape.

The AI can return only short explanations and first steps for action IDs Django already selected. Django checks the response before displaying it. If the key is missing, the API fails, or the response is unusable, Django returns the predefined rule-based action cards. The dashboard and plan still work.

Answers and results live only in browser memory during the current visit. The app does not write user or business assessment data to a database or keep permanent assessment records; refreshing or closing the page starts a new assessment. OpenAI receives the minimum structured context only when guidance is requested; provider-side abuse-monitoring retention is described below. The only external call is the optional AI guidance request; no account, scanner, cloud database, or frontend framework is needed.

## The Core Journey Through the System

Implements PRD: The Core Journey, Guided Assessment, Transparent Score and Risk Priorities, Results and Action Plan, and AI Guidance and Fallback.

1. **Arrive.** The browser requests the Django page. The template shows the landing screen and its Assess → Understand → Act path.
2. **Assess.** JavaScript shows one question at a time, keeps selected answers in memory, preserves them on Back, and prevents unanswered submissions.
3. **Calculate.** Analyze My Security sends the eight answer IDs to Django. Django validates the payload and runs the deterministic scoring and risk-ranking functions.
4. **Understand.** Django returns the score, status, eight area states, ordered findings, and selected action IDs. JavaScript displays the self-report disclaimer, score, area breakdown, and top risks.
5. **Get AI Guidance.** The browser sends the answers again. Django recomputes canonical results and action selection; it ignores any client-supplied score, risk priority, or action mapping.
6. **Explain or fall back.** The provider-neutral guidance service calls OpenAI once using the server-side key. Django validates the returned text and IDs, then displays guidance in the existing dashboard flow. On missing key, timeout, billing/rate limit, refusal, or invalid output, it displays the rules-based action plan and the approved temporary-unavailability message. The owner can retry.

## Stack

| Part | Choice | Why it fits |
|---|---|---|
| Server | Python 3.14.8 and Django 5.2 LTS (5.2.8 or later) | Django is familiar to the learner and handles the page, validation, and rules in one place. Django 5.2.8 added official Python 3.14 support, so the learner can use the runtime already installed instead of maintaining another version. The current OpenAI Python SDK also supports Python 3.14. [Django 5.2 release notes](https://docs.djangoproject.com/en/5.2/releases/5.2/) · [Python/Django compatibility](https://docs.djangoproject.com/en/5.2/faq/install/) · [OpenAI Python version policy](https://github.com/openai/openai-python/blob/main/PYTHON_VERSION_POLICY.md) |
| Browser | Django template, HTML, CSS, and vanilla JavaScript | Reuses the learner’s existing web skills. One small script is enough for the guided flow; React and a separate frontend build are unnecessary for this POC. |
| AI client | Official OpenAI Python SDK, behind the app’s own guidance service | Keeps provider-specific request details in one adapter. A later provider can implement the same small contract. [OpenAI Python SDK](https://github.com/openai/openai-python) |
| Local secrets | python-dotenv loads a local .env file into Django’s server environment | Convenient in VS Code; the existing .gitignore already ignores .env and allows .env.example. Keep the real key out of source control and browser code. [python-dotenv](https://pypi.org/project/python-dotenv/) |
| Database | None for assessment results | The POC has no accounts, history, or saved business profiles. Do not add Postgres, MySQL, or Supabase. |
| Styling | Custom CSS and local SVG/CSS details; no UI framework or external font/CDN requirement | Keeps the visual identity polished while working locally and offline. |

Install the latest compatible Django 5.2 patch and pin the resolved package versions in requirements.txt during the build. Use the current stable OpenAI SDK release and record the installed version there as well; exact package patch numbers should be checked at build time.

## Where It Runs and How Someone Tries It

**Primary runtime:** local Windows development in VS Code. Python and Django run on the learner’s computer; the browser opens the local Django site. Internet access is needed only for live OpenAI guidance. If OpenAI is not configured, the rules-based flow still runs.

Planned PowerShell setup:

    py -3.14 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt
    Copy-Item .env.example .env
    python manage.py runserver

Open http://127.0.0.1:8000. Put a personal API key only in the ignored local .env file if the account has credits or the learner chooses to fund API use. Leave OPENAI_API_KEY blank to use fallback guidance. Never paste the key into HTML, JavaScript, GitHub, or chat. The Django development server is for local use, not a production host.

No database migration is required for the assessment. For a one-minute recording, start on the landing screen, use a prepared set of answers, show the self-reported score and highest risks, then select Get AI Guidance and show the action cards. If no key or credit is available, demonstrate the real rule-based fallback and its notice.

The required Devpost submission still needs a short demo video and a public GitHub repository. Deployment is optional and comes after the local journey works; no hosting platform is selected in this spec. Revisit public deployment in 6-ship, including secret configuration and a spend cap before exposing an AI endpoint.

## Look and Feel

Carry forward PRD: Look and Feel and scope: Inspiration & Identity. Use deep navy/blue for the product frame, cyan/light-blue for focus and actions, and white or pale-gray content surfaces. Keep the page calm and spacious, with a clear score/status hierarchy, compact eight-area cards, and a small number of readable risk/action cards. Use green, amber, and red for semantic risk states, with text labels as well as color. Use a legible system sans-serif stack, visible keyboard focus, and accessible contrast. Keep copy professional, plain-language, and reassuring; avoid hacker imagery and dense technical jargon.

## Components

### Landing and assessment interface

The Django template contains the landing view, one-question wizard, progress, answer choices, helper text, field errors, and results/action-plan containers. JavaScript stores the current question and eight selected answer values in memory, preserves values when moving Back, and sends requests to Django. It does not calculate risk scores. On refresh, the wizard restarts.

Implements PRD: Landing, Assessment, and Guided Assessment.

### Django request views

The root view serves the page. Two same-origin JSON POST endpoints handle analysis and guidance. Both validate the request shape and allowed answer values on the server, use Django CSRF protection, and return JSON with a clear client error for malformed or incomplete answers. The guidance endpoint recomputes canonical results from answers rather than trusting browser-supplied derived fields.

Implements PRD: Guided Assessment, Results Dashboard, and AI Guidance and Fallback.

### Assessment catalog

A small Python catalog holds the fixed area IDs and order, question/helper copy, impact bands, fixed risk descriptions, risk-to-action IDs, fallback action copy, and preventive/verification action copy. The learner reviewed and approved the final question/helper wording and fallback action copy during Final Review.

Implements PRD: Assessment, Transparent Score and Risk Priorities, and Results and Action Plan.

### Deterministic assessment engine

Pure Python functions validate the eight answers, assign Yes = 12.5, Not sure = 6.25, No = 0, sum the score, assign the PRD status band, create findings, and sort them. Use Decimal values or exact quarter-point units so sums such as 56.25 are stable.

The score bands are 80–100 Strong, 50–79 Needs Attention, and 0–49 High Risk; implementation uses score >= 80, else >= 50, else High Risk. The area order and impacts are fixed:

| Order | Area ID | Area | Impact |
|---:|---|---|---|
| 1 | password_security | Password security | High |
| 2 | mfa | Multi-factor authentication | High |
| 3 | backups | Backups | High |
| 4 | software_updates | Software and system updates | Moderate |
| 5 | user_access | User access and permissions | High |
| 6 | wifi_security | Network/Wi-Fi security | Moderate |
| 7 | device_protection | Device protection | Moderate |
| 8 | employee_practices | Employee security practices | Moderate |

Yes creates no finding. No + High impact creates a high-priority confirmed gap; No + Moderate impact creates a medium-priority confirmed gap. Not sure uses the same impact-based priority, but is labeled “needs verification” rather than a confirmed gap. Rank high before medium, then confirmed No before Not sure at the same priority, then use the fixed area order above. Identical answers must return identical results. The dashboard makes the first three findings prominent and may show other real findings below them; the action plan contains up to three mapped actions. The score measures the owner’s self-reported controls, not a technical audit or verified security level.

This component is the sole authority for score, status, findings, priorities, ranking, and selected action IDs. AI is never called to calculate any of those values. The same eight answers must return identical results.

Implements PRD: Transparent Score and Risk Priorities.

### Risk-linked action catalog

For each possible finding, the catalog provides a fixed remediation or verification action. If there are fewer than three findings, it selects only enough predefined preventive/verification actions to fill the plan and labels them as such. If there are no findings, it returns a positive result plus maintenance/prevention actions. It never adds a risk to fill a slot.

Each action has a stable action ID, a linked risk ID when remediating, a fixed “what to do” description, a plain-language risk rationale, a fallback first step, and a kind of remediation, verification, or prevention. AI may personalize the explanation and first step, but cannot select another action or unlink the risk.

Implements PRD: Results and Action Plan.

### Provider-neutral AI guidance service

The rest of Django calls one internal function such as generate_guidance(context). The context contains canonical score/status, relevant categorical answers, ordered findings, and the action IDs and fixed action descriptions already selected by Django. The service returns a consistent application-owned structure. It chooses an adapter from server settings and validates the response. No other application component imports OpenAI classes or names.

The accepted initial adapter is OpenAI. The app setting identifies the provider and model, for example AI_PROVIDER=openai and OPENAI_MODEL=gpt-6-luna. A future adapter can replace the provider-specific request while preserving the same service input/output. This is a small seam for changing providers, not a multi-provider framework.

Implements PRD: AI Guidance and Fallback.

### OpenAI adapter

The adapter uses the official Python SDK and Responses API. It sends the system instructions plus the structured assessment context and requests a strict JSON schema containing only approved `summary_style`, selected `action_id`, and `explanation_style` identifiers. It sets `store=false`, caps output length, and uses a finite timeout. The action ID enum is limited to the IDs selected by Django. One button press makes one request; a retry is a new user-initiated request. It sends no name, email, free-text field, network data, or credentials. It does not enable web search, function calling, or other tools.

The model generates no user-facing prose. Django validates the style identifiers and exact action ID set, then renders all displayed wording from fixed server-owned summary, explanation-prefix, and action catalogs in Django’s original order. The only AI choice is whether to use an approved general or contextual phrasing variant. The output schema contains no score, severity, priority, ranking, finding, prose, or action-selection fields. AI must never calculate the score, change severity or priority, reorder findings, alter the risk-to-action mapping, or invent an unrelated risk. If the response is refused, malformed, incomplete, mismatched, or contains unexpected fields, the service uses the rules-based fallback copy.

OpenAI states API data is not used for model training by default. The Responses API can retain response application state for 30 days by default, so the adapter must set store=false. Abuse-monitoring logs may still retain customer content for up to 30 days; the POC therefore sends only the categorical answers and the minimum structured context needed. [OpenAI data controls](https://developers.openai.com/api/docs/guides/your-data) · [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs) · [API key handling](https://developers.openai.com/api/reference/overview)

Implements PRD: AI Guidance and Fallback.

### Results renderer and retry control

JavaScript displays the server’s score and statuses without recalculating them. It visually distinguishes confirmed gaps from verification findings, labels preventive actions, presents the approved self-report disclaimer, shows fallback messaging, and offers a retry control. Changing an answer clears the old result and guidance before the owner analyzes again.

Implements PRD: Results Dashboard, AI Guidance and Action Plan, and States and Boundaries.

## Data Model

There is no persistent application data model or database table. CyberShield AI does not keep permanent user, business, assessment, or action-plan records.

- **Answers:** eight area IDs with values yes, no, or not_sure. Created through the wizard and held in JavaScript memory only.
- **Analysis result:** returned by Django after validation; contains score, status, per-area answer/points/state, ordered findings, and selected action IDs. Kept in JavaScript memory for the current visit.
- **Guidance:** returned after the guidance request; contains a short explanation and first step keyed to the preselected action IDs, plus a mode of ai or fallback and the notice state. Kept in memory only.
- **Catalog/rules:** fixed Python constants, not user records. These are the source of deterministic priorities and fallback copy.

The browser posts only the eight answers to both endpoints. Django validates and recomputes; it does not persist them. Closing or refreshing the page clears the journey. The AI request goes from Django to OpenAI over HTTPS; OpenAI receives only the categorical answers and rule-generated context. With store=false, response application state is not retained by the Responses API. OpenAI’s separate abuse-monitoring logs may retain prompts and responses for up to 30 days; the spec does not imply that data sent to an external provider is never retained.

## File Structure

The existing Devpost planning files stay at the project root. The app files below are the planned build; there is no frontend package build and no assessment database.

    CyberShieldAI/
    ├── manage.py                         # Django local entry point
    ├── requirements.txt                  # Django, OpenAI SDK, python-dotenv
    ├── .env.example                      # blank server-side settings template
    ├── .gitignore                        # existing rules exclude .env
    ├── README.md                         # local setup and demo steps
    ├── cybershield/
    │   ├── __init__.py
    │   ├── settings.py                   # Django, template/static, environment settings
    │   ├── urls.py                       # root page and assessment routes
    │   ├── asgi.py
    │   └── wsgi.py
    ├── assessment/
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── catalog.py                    # question, impact, action, fallback definitions
    │   ├── rules.py                      # validation, score, findings, stable ordering
    │   ├── views.py                      # page and JSON request endpoints
    │   ├── urls.py
    │   └── guidance/
    │       ├── __init__.py
    │       ├── service.py                # provider-neutral contract, validation, fallback
    │       └── openai_adapter.py         # initial OpenAI implementation only
    ├── templates/assessment/
    │   └── index.html                    # landing, wizard, dashboard, action plan
    ├── static/assessment/
    │   ├── css/app.css
    │   └── js/app.js                     # navigation, answer memory, fetch, rendering
    └── devpost/
        ├── learner-profile.md
        ├── scope.md
        ├── scope.html
        ├── prd.md
        ├── prd.html
        ├── spec.md
        └── spec.html

## API Contracts

### Same-origin assessment analysis

POST /api/assessment/analyze/ accepts JSON:

    {
      "answers": {
        "password_security": "yes",
        "mfa": "not_sure",
        "backups": "no",
        "software_updates": "yes",
        "user_access": "yes",
        "wifi_security": "not_sure",
        "device_protection": "yes",
        "employee_practices": "no"
      }
    }

Success response:

    {
      "score": 62.5,
      "status": "Needs Attention",
      "areas": [
        {
          "id": "backups",
          "answer": "no",
          "points": 0,
          "signal": "confirmed_gap"
        }
      ],
      "findings": [
        {
          "risk_id": "backups",
          "area": "Backups",
          "answer": "no",
          "priority": "high",
          "certainty": "confirmed",
          "reason": "Important business data may not be recoverable.",
          "action_id": "backups-recovery"
        }
      ]
    }

The production response contains all eight area objects and every actual finding in deterministic order, not only the sample entries above. It contains no AI-generated fields. Invalid requests return an error object with a human-readable message and, when relevant, the first unanswered question ID.

### Same-origin guidance request

POST /api/assessment/guidance/ accepts the same answer shape. Django recomputes the canonical analysis and selected actions before calling the guidance service. Client-supplied derived scores/findings/actions are ignored. The response shape is:

    {
      "mode": "ai",
      "summary": "Server-owned summary copy selected by an approved AI style identifier.",
      "actions": [
        {
          "action_id": "catalog-id",
          "kind": "remediation",
          "risk_id": "backups",
          "risk_addressed": "Backups",
          "priority": "high",
          "what_to_do": "The fixed action text selected by Django.",
          "why_it_matters": "Fixed plain-language explanation from the server action catalog.",
          "how_to_start": "Fixed realistic first step from the server action catalog."
        }
      ],
      "notice": null,
      "can_retry": false
    }

The adapter’s constrained response contains only a summary style and per-action ID/style identifiers. The guidance service validates those identifiers and supplies every displayed summary and action string from Django’s fixed catalogs, preserving server order. For fallback mode, Django fills all fields from the same fixed action catalog, sets mode to fallback, and includes the approved notice. The response is validated before rendering.

### OpenAI Responses API

- **Endpoint:** POST https://api.openai.com/v1/responses, called through the official Python SDK.
- **Authentication:** project-scoped Bearer key from the server’s OPENAI_API_KEY environment variable.
- **Request:** configurable model (initial value gpt-6-luna); strict JSON-schema output through Responses API text.format; score/status/findings/answers/selected actions from Django; store=false; bounded output; no external tools. The schema permits only `summary_style` (`reassuring` or `direct`) and an exact set of selected `action_id` values paired with `explanation_style` (`standard` or `contextual`).
- **Response:** JSON identifiers only. The adapter converts them to the provider-neutral guidance structure; Django renders all user-facing text from fixed copy.
- **Validation:** exact fields, known style IDs, exact expected action IDs and count, with no duplicates. A failed validation takes the fallback path.

As checked on 2026-10-02, OpenAI’s model page describes GPT-6 Luna as its efficient model for focused tasks, supports Structured Outputs and Responses, and lists $0.10 per million input tokens and $0.50 per million output tokens. It does not list a free rate-limit tier. These rates and model availability can change; check again before enabling the key. [GPT-6 Luna model](https://developers.openai.com/api/docs/models/gpt-6-luna) · [OpenAI API pricing](https://developers.openai.com/api/docs/pricing)

## External Services and Cost Check

The assessment engine, score, dashboard, and fallback work without an OpenAI account, API key, or network call.

The user’s account credit balance is account-specific and cannot be checked from this workspace. Before enabling live guidance, open the correct organization in the [OpenAI API billing overview](https://platform.openai.com/account/billing) and check the available credit balance. If the account has free API credits, OpenAI says they are consumed before purchased credits. ChatGPT subscription billing is separate from API billing. Current prepaid-account guidance says new API accounts use prepaid credits and the minimum initial purchase is $5; this is not required to build or use fallback mode. Do not buy credits unless the owner decides to enable paid guidance. Use a dedicated project and a project-scoped key for this app. [Prepaid API billing](https://help.openai.com/en/articles/8264644-setting-up-and-managing-prepaid-api-billing) · [ChatGPT/API billing separation](https://help.openai.com/en/articles/9039756-managing-billing-for-chatgpt-and-the-api-platform)

Before any paid demo, create/use a dedicated API project, inspect usage, and consider a low project hard spend limit plus an alert. A hard limit causes requests to stop after the configured amount, though enforcement can lag and slightly exceed it. Cost is token-based; the app makes one short request only when the owner asks for guidance, caps output, and never calls AI to compute a score. [OpenAI spend limits](https://developers.openai.com/api/docs/guides/spend-limits)

## Important Failure Modes

- **Missing or invalid answer payload** → Django returns a clear field-level error; no score or AI request is produced. The browser highlights the first unanswered question.
- **No API key, unavailable API, timeout, exhausted credits, rate limit, refusal, or invalid model output** → Django retains the deterministic analysis, displays “AI guidance is temporarily unavailable, but your security assessment is ready.” and returns predefined actions; retry stays available.
- **Page refresh or close** → the app’s current answers/results are cleared and the owner restarts; the app keeps no assessment record. If an AI request was made, OpenAI’s separately documented abuse-monitoring retention may still apply for up to 30 days.

## What Was Simplified and Why

- One Django app with templates and vanilla JavaScript instead of separate React frontend and API projects — fits the learner’s existing skills and lets one local command run the demo.
- No accounts, database, persistent assessment history, or Supabase — the PRD proves a single anonymous journey, so persistence adds no value to the demo.
- A fixed eight-area catalog and transparent Python rules instead of a general risk engine — it makes scoring and tie-breaks inspectable and repeatable.
- One OpenAI adapter behind a small internal contract instead of a provider framework — keeps a later swap possible without building multiple integrations now.
- One bounded synchronous guidance request instead of streaming, tools, or a chatbot — matches the single-click action-plan journey and makes the fallback easy to explain.
- Local development first; deployment remains optional and is considered only after the complete local experience works.

## Decisions and Open Issues

### Learner decisions carried into this spec

- Django/Python is the server-side stack; local VS Code use is the priority; deployment is optional and secondary.
- The learner chose the already-installed Python 3.14.8; use Django 5.2.8 or later in the 5.2 LTS series. No separate Python 3.13 installation is needed.
- The learner approved Django templates plus vanilla JavaScript for the browser experience.
- The learner approved temporary browser-memory answer/result state with no database or persistent assessment storage; refreshing or closing restarts the journey.
- No authentication, database, Supabase, or React is part of the POC unless a concrete approved PRD requirement makes one necessary.
- Django owns score, findings, priorities, ranking, and action mapping before AI is called.
- OpenAI is the first provider, behind a small provider-neutral service. The key remains in a server environment variable and is never sent to the browser.
- Rules-based fallback must preserve the assessment if AI is absent or fails.
- The overall project remains a hackathon POC, not a SaaS platform.

### Implementation details to verify during build

- Use Django 5.2 LTS and keep provider/model names in server environment settings rather than embedding them in the rules or UI.
- GPT-6 Luna is the initial low-cost model setting checked for this draft; confirm current availability, account credits, and pricing before enabling a live API call.
- Keep the AI call disabled when OPENAI_API_KEY is missing; this provides a working fallback demo without requiring a purchase.

### Decisions and checks before live API use

- The learner’s actual API credits are unknown. Check the API billing overview before creating a key or purchasing credits. The current GPT-6 Luna page lists no free API tier; the currently listed token rates are low, and account credits, if present, are applied first.
- If live guidance is enabled, use a server-only key, set store=false, send only categorical answers and necessary rule results, and set a project hard spend limit/alert chosen by the owner.
- Use the verified Python 3.14.8 runtime and confirm the current compatible Django 5.2 and SDK package patches in the first build step.
- Revisit public hosting only after local verification. Before a public AI endpoint is exposed, review deployment secrets, spend limits, and basic request-abuse protection.
- Copy review is complete: the learner reviewed and approved all eight questions/helpers, fallback actions, summaries, and the AI-unavailable notice during Final Review. The priority rules, scoring, tie-break, and fallback behavior are fixed.

The learner’s stated uncertainty was whether API credits are available and whether a suitable low-cost option exists. The model and current pricing have been checked; the individual balance cannot be read from this workspace. The learner can verify it in the API billing overview without sharing a key or account credentials. Until then, the app can be built and demonstrated in fallback mode.
