# CashClaw Sprint1000

CashClaw Sprint1000 is an open-source project that helps ordinary people earn their first **$1,000 in 30 days** by combining OpenClaw automation with practical service-delivery playbooks.

This project ships with:
- An OpenClaw Skill focused on income execution (finding demand, crafting offers, handling outreach, and delivering work)
- A deployable orchestration service (local or cloud) that routes tasks across different AI models
- A feedback loop to evolve strategies from real community outcomes

## Design principle: MMP validation engine

The project is designed as a **Minimum Money Path (MMP) validation engine**:
- Start from the smallest sellable offer that can close quickly
- Run short experiments with measurable targets
- Keep only what improves close rate, delivery speed, or collected revenue
- Continuously iterate until the $1,000 target is reached

OpenClaw + the orchestration service should behave like a daily execution machine:
**Hypothesis -> Experiment -> Metrics -> Decision -> Next experiment**.

## Why this project exists

Most people do not fail because they lack talent; they fail because they lack:
- A clear 30-day execution system
- Fast, repeatable workflows for lead generation and delivery
- Lightweight automation that can run every day

CashClaw Sprint1000 turns those missing pieces into a reusable stack.

## Core architecture

1. `openclaw-skills/sprint1000/SKILL.md`
   - Teaches OpenClaw how to run the 30-day revenue sprint
   - Includes prompts, guardrails, and daily operating loops
2. `service/`
   - FastAPI app for model orchestration
   - Works with local models (Ollama-compatible) and online models (OpenAI-compatible APIs)
   - Provides endpoints for plan generation and execution
3. `community/`
   - Templates and process for collecting and integrating GitHub feedback into weekly strategy upgrades
4. `service /v1/experiment`
   - Generates one MMP experiment with pass/fail thresholds and next-step rules

## "Frontier pattern" principles used

This project borrows from current high-performance solo-business AI patterns:
- **Offer-first loops**: start with a sellable micro-offer before building assets
- **Distribution before perfection**: daily outreach > perfect branding
- **Model routing**: cheap models for drafting, stronger models for conversion-critical outputs
- **Human-in-the-loop QA**: AI drafts, human verifies, then ships
- **Weekly feedback compounding**: update the playbook from user outcomes and issue reports

## Quick start

### 1) Configure environment

```bash
cp .env.example .env
```

Fill in your provider credentials (at least one online provider or one local model endpoint).

Place `.env` in the **repository root** (next to `docker-compose.yml`). If you run `uvicorn` manually, the service still loads that file automatically (it searches repo root, then `service/`, then the current working directory).

For **Alibaba DashScope** (OpenAI-compatible), set:

```env
ONLINE_MODEL_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
ONLINE_MODEL_NAME=qwen-plus
ONLINE_MODEL_API_KEY=your-dashscope-api-key
MODEL_ROUTING_POLICY=quality_first
```

You can also use `OPENAI_BASE_URL` / `OPENAI_API_KEY` / `OPENAI_MODEL` as aliases when `ONLINE_*` is unset.

**Local Ollama (no API key)** — ensure Ollama is running (`ollama serve`) and a model is pulled, then in `.env`:

```env
LOCAL_MODEL_BASE_URL=http://127.0.0.1:11434/v1
LOCAL_MODEL_NAME=qwen2.5:3b
MODEL_ROUTING_POLICY=local_first
```

`POST /v1/plan` can take **60–120 seconds** on small local models; the service uses a 120s upstream timeout.

### Landing page (promotion site)

A static promo page is available in `web/`:

```bash
open web/index.html
```

Or serve it with any static server for deployment.

### 2) Run locally

```bash
docker compose up --build
```

Or run directly with Python:

```bash
cd service
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### 3) Test orchestration API

```bash
curl -X POST http://localhost:8080/v1/plan \
  -H "Content-Type: application/json" \
  -d '{
    "profile": "I can do basic automation and writing.",
    "hours_per_day": 2,
    "target_usd": 1000,
    "days": 30
  }'
```

```bash
curl -X POST http://localhost:8080/v1/experiment \
  -H "Content-Type: application/json" \
  -d '{
    "current_offer": "48-hour landing page rewrite package",
    "channel": "cold email",
    "last_metrics": "20 outreach, 3 replies, 0 closed, 0 USD",
    "constraint_hours_per_day": 2
  }'
```

## Roadmap

- v0: Baseline sprint system + model orchestration service
- v1: Marketplace-specific templates (Upwork, Fiverr, local SMB outreach)
- v2: Telemetry-backed strategy ranking based on conversion and delivery quality
- v3: Auto-generated weekly retrospectives from GitHub issue data

## Responsible use

This project is for legal, ethical service work. Do not use it for spam, scams, or deceptive claims.

## Contributing

Please open issues with:
- Your market/channel
- What you tried
- What failed and why
- Evidence (redacted screenshots, metrics, response rates)

See `community/FEEDBACK_LOOP.md` for the feedback integration process.
