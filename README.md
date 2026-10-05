# CyberShield AI

CyberShield AI is a guided cybersecurity self-assessment for small-business owners and managers without dedicated cybersecurity staff.

It helps them understand which everyday cybersecurity practices need attention and what to address first.

## How it works

The experience follows **Assess → Understand → Act**:

1. **Assess:** Answer eight plain-language questions about passwords, multi-factor authentication, backups, software and system updates, user access, network and Wi-Fi security, device protection, and employee security practices. The assessment is designed to take about 3–5 minutes.
2. **Understand:** Django applies transparent rules to calculate a self-reported score and identify and rank findings. The dashboard distinguishes confirmed gaps from areas that need verification.
3. **Act:** Review a structured plan of up to three actions. Each action explains what to do, why it matters, which finding it addresses, and how to get started. When there are fewer than three findings, any additional recommendations are labeled as preventive or verification guidance.

No account is required. The assessment reflects the answers provided; it does not verify the business’s actual systems or controls.

## Assessment and scoring

Each of the eight areas contributes equally to the 0–100 score:

- **Yes:** 12.5 points
- **Not sure:** 6.25 points
- **No:** 0 points

The score maps to these statuses:

- **80–100:** Strong
- **50–79:** Needs Attention
- **0–49:** High Risk

A **No** answer creates a confirmed-gap finding. **Not sure** creates a finding that needs verification, rather than claiming that a control is missing. A **Yes** answer creates no finding.

Priorities are assigned by area impact: backups, password security, multi-factor authentication, and user access are high impact; updates, Wi-Fi, device protection, and employee practices are moderate impact. High-priority findings rank before medium-priority findings. At the same priority, confirmed gaps rank before verification findings; a fixed area order resolves any remaining ties.

The displayed score is based on self-reported answers. It is not a measured or technically verified security level.

## Optional AI guidance

The assessment, score, findings, priorities, action selection, and fallback plan are determined by Django rules. AI is an optional explanation layer and cannot change those results or introduce unrelated risks.

When enabled, the initial provider is OpenAI, called from a provider-neutral Django service. The model can return only approved style identifiers for explanations; Django validates them and renders all user-visible wording and actions from fixed catalogs. The model does not write displayed prose, calculate scores, assign priorities, reorder findings, or select different actions.

The OpenAI API key is read by Django from the server-side `OPENAI_API_KEY` environment variable and is never sent to the browser. Requests use `store=false`. If no key is configured or AI guidance is unavailable, the rules-based assessment and predefined action plan remain available.

## Run locally

### Requirements

- Windows
- Python 3.14.8 (64-bit)
- PowerShell

From the project folder in PowerShell:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py runserver
```

Open <http://127.0.0.1:8000/> in your browser. Stop the development server with `Ctrl+C`.

The project uses Django 5.2.17. No database setup or migrations are required. Current answers and results stay in browser memory and are cleared when the page is refreshed or closed; the application does not keep permanent assessment records.

## Proof-of-concept boundary

CyberShield AI is a self-assessment demonstration, not a full cybersecurity platform. It does not scan devices or networks, perform penetration testing, or conduct a technical security audit. Its results depend on the owner’s answers and should not be read as technical verification of the business’s security.

## Build checklist

See [`devpost/checklist.md`](devpost/checklist.md) for the approved build sequence and verification checkpoints.

## License

Open source under the MIT License.
