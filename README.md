# CyberShield AI

A local proof of concept that helps a small-business owner understand self-reported cybersecurity practices, see deterministic findings, and identify what to address first.

## Requirements

- Windows with Python 3.14.8 (64-bit)
- PowerShell

The project uses Django 5.2.17. The rules-based assessment and action plan do not require a database, account, or API key. Optional AI guidance uses the OpenAI Responses API from the Django backend; if no key is configured or the provider cannot return valid guidance, the predefined action plan remains available.

## Run locally

From the project folder in PowerShell:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py runserver
```

Open <http://127.0.0.1:8000/> in your browser. Stop the development server with `Ctrl+C`.

There are no migrations to run. The assessment uses temporary in-page answers; it does not persist business or user data.

## Optional AI guidance

The app works without an OpenAI API key. If you later choose to enable AI-selected guidance styles after checking API billing/credits, copy `.env.example` to `.env`, then set `OPENAI_API_KEY` in `.env`. Keep `.env` private; it is excluded from Git and the key is read only by Django. `AI_PROVIDER` defaults to `openai`, and `OPENAI_MODEL` defaults to `gpt-6-luna`. Restart the development server after editing `.env`.

The adapter sends only categorical answers and Django's structured results and selected actions. It requests strict structured output containing approved style IDs only. Django supplies every displayed sentence and action detail from fixed copy, so model output cannot add or contradict score, findings, or advice. The request uses `store=false`, and the app never lets the model choose or reorder risks. Without a configured key, the app shows the rules-based plan and its AI-unavailable message. Refreshing or closing the page clears the current assessment; the project has no database or permanent assessment storage.

## Assessment rules

- The eight areas are scored equally: Yes = 12.5, Not sure = 6.25, No = 0.
- The total score maps to Strong (80–100), Needs Attention (50–79), or High Risk (0–49).
- A No creates a confirmed finding. Not sure creates a finding that needs verification.
- High-impact findings rank before moderate-impact findings. At the same priority, confirmed No findings rank before Not sure findings. The fixed PRD area order breaks any remaining tie.
- The score and priorities are determined by Python rules. The dashboard identifies the result as self-reported and does not claim a technical scan or audit.

## Build progress

See [`devpost/checklist.md`](devpost/checklist.md) for the approved three-slice build sequence and verification checkpoints.
