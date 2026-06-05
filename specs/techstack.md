# Tech Stack

## Core Framework

| Layer | Choice | Rationale |
|---|---|---|
| Language | Python 3.11+ | Strong ecosystem for medical data APIs and LLM tooling |
| Agent Orchestration | LangGraph | Graph-based stateful agent; models multi-step retrieval and synthesis cleanly |
| LLM | Claude (via Anthropic SDK) | High accuracy on medical synthesis; strong instruction-following for structured output |
| API Layer | FastAPI | Lightweight, async-native REST API with automatic schema docs |
| Frontend | React | Component-based UI; simple to wire to a REST API; easy to extend later |

## Data Sources

| Source | What It Provides | Access Method |
|---|---|---|
| PubMed / NCBI E-utilities | Peer-reviewed literature on standard of care and treatments | Free REST API (no key required, rate-limited) |
| ClinicalTrials.gov API v2 | Active and completed clinical trials, pipeline treatments | Free REST API |

## LangGraph Agent Design

The briefing pipeline is modeled as a LangGraph state graph with the following nodes:

```
[START]
  └─> query_pubmed        — searches PubMed for condition + treatment literature
  └─> query_clinicaltrials — searches ClinicalTrials.gov for active trials
        ↓
  synthesize_brief        — Claude synthesizes retrieved data into structured sections
        ↓
  format_output           — validates and structures final JSON/Markdown brief
        ↓
[END]
```

Parallel retrieval nodes (PubMed + ClinicalTrials) feed into a single synthesis node.

## Output Format

Structured JSON response consumable by the REST API, with optional Markdown rendering:

```json
{
  "condition": "string",
  "standard_of_care": ["..."],
  "emerging_treatments": ["..."],
  "key_organizations": ["..."],
  "sources": ["pmid:...", "nct:..."]
}
```

## Repo Structure

```
/
├── app/        — FastAPI backend + LangGraph agent
├── ui/         — React frontend
├── specs/      — Constitution documents
└── tests/      — Backend unit and integration tests
```

## Frontend Design (React)

The UI is minimal but fully functional. Day-one scope:

- **Condition input** — a single text field and submit button
- **Loading state** — spinner displayed while the backend processes the brief
- **Structured brief display** — three clearly labeled sections: Standard of Care, Emerging Treatments, Key Organizations
- **Source citations** — PubMed and ClinicalTrials.gov links rendered alongside each section

The React app calls `POST /brief` on the FastAPI backend. No state management library needed for v1; React's built-in `useState` and `fetch` are sufficient.

## Backend Dependencies

```
langgraph
langchain-anthropic
anthropic
fastapi
uvicorn
httpx
pydantic
```

## Frontend Dependencies

```
react
react-dom
vite          (build tooling)
```

No UI component library in v1 — plain HTML elements styled with CSS to keep the build minimal.

## What is Out of Scope

- Authentication / user management (not needed for v1)
- A database or caching layer (not needed for v1)
- A frontend component library or design system (not needed for v1)
