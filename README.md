# Medical Condition Briefing System

Type a medical condition. Get a structured, evidence-backed briefing in under a minute.

The system searches live data from PubMed and ClinicalTrials.gov in parallel, then uses Claude AI to synthesise the findings into three sections: standard of care, emerging treatments, and key organisations. Every claim links back to its source.

---

## What It Produces

```json
{
  "condition": "type 2 diabetes",
  "standard_of_care": ["Metformin remains the first-line oral agent..."],
  "emerging_treatments": ["Once-weekly insulin icodec in Phase 3 trials..."],
  "key_organizations": ["Novo Nordisk", "Eli Lilly", "Mayo Clinic"],
  "sources": ["pmid:38471203", "nct:NCT05394519"]
}
```

---

## Architecture

```
[START]
  ├─> query_pubmed          — top 5 papers from PubMed (last 5 years)
  └─> query_clinicaltrials  — top 5 active Phase 2–4 trials from ClinicalTrials.gov
              ↓  (parallel, different threads)
        synthesize_brief    — Claude produces structured output via forced tool use
              ↓
        format_output       — Pydantic validation, final JSON
              ↓
         [END]
```

The two retrieval nodes run concurrently via LangGraph's parallel fan-out. Each retries once on failure and returns an empty list rather than blocking the pipeline.

---

## Stack

| Layer | Technology |
|---|---|
| Agent orchestration | LangGraph |
| LLM | Claude (claude-sonnet-4-5) via Anthropic SDK |
| API | FastAPI + Uvicorn |
| Frontend | React + Vite |
| Data sources | PubMed E-utilities, ClinicalTrials.gov API v2 |
| Testing | pytest (backend), Playwright (E2E) |

---

## Project Structure

```
├── app/
│   ├── main.py            # FastAPI app, CORS, POST /brief endpoint
│   ├── graph.py           # LangGraph StateGraph definition
│   ├── nodes.py           # Node functions (retrieval, synthesis, formatting)
│   ├── pubmed.py          # PubMed E-utilities client
│   ├── clinicaltrials.py  # ClinicalTrials.gov API v2 client
│   ├── synthesize.py      # Claude tool-use synthesis
│   ├── models.py          # Pydantic request/response models
│   └── state.py           # LangGraph state TypedDict
├── ui/
│   ├── src/
│   │   ├── App.jsx        # Main React component
│   │   └── App.css        # Styles
│   ├── tests/
│   │   └── brief.spec.js  # Playwright E2E tests
│   └── playwright.config.js
├── tests/                 # pytest backend tests
├── specs/                 # Phase specs (plan, requirements, validation per phase)
└── requirements.txt
```

---

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- An [Anthropic API key](https://console.anthropic.com/)

### Backend

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=sk-ant-...
```

### Frontend

```bash
cd ui
npm install
npx playwright install chromium
```

---

## Running the App

**Terminal 1 — backend:**

```bash
ANTHROPIC_API_KEY=sk-ant-... uvicorn app.main:app --reload
```

**Terminal 2 — frontend:**

```bash
cd ui && npm run dev
```

Open [http://localhost:5173](http://localhost:5173).

---

## Running Tests

**Backend (pytest):**

```bash
python -m pytest tests/
# 9 pass, 1 skipped (integration test requires ANTHROPIC_API_KEY)
```

**Frontend (Playwright E2E):**

```bash
# Backend must be running first
cd ui && npm test
```

---

## API

### `POST /brief`

Request:
```json
{ "condition": "asthma" }
```

Response: see [What It Produces](#what-it-produces) above.

**Errors:**
- `422` — empty or whitespace-only condition
- `503` — upstream retrieval or synthesis failure

### `GET /health`

```json
{ "status": "ok" }
```

---

## Data Sources

| Source | What it provides |
|---|---|
| [PubMed E-utilities](https://www.ncbi.nlm.nih.gov/home/develop/api/) | Peer-reviewed literature (35M+ studies, last 5 years filtered) |
| [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api) | Active and recruiting Phase 2–4 trials |

No API keys required for either source.
