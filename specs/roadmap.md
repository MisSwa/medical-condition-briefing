# Roadmap

Each phase is a self-contained, shippable unit of work. Phases build on each other but each produces something runnable and testable.

---

## Phase 1 — Project Skeleton

**Goal:** Runnable FastAPI app with a stub endpoint and LangGraph wired up but not yet doing real work.

- Initialize repo structure (`app/`, `ui/`, `specs/`, `tests/`)
- Install and pin dependencies (`langgraph`, `langchain-anthropic`, `fastapi`, `httpx`, `pydantic`)
- Create `POST /brief` endpoint that accepts `{ "condition": "..." }` and returns a hardcoded stub response
- Define the LangGraph state schema (`BriefingState`)
- Confirm the graph can be imported and invoked end-to-end (even with no-op nodes)

**Done when:** `curl -X POST /brief -d '{"condition":"asthma"}'` returns a valid (stubbed) JSON brief.

---

## Phase 2 — PubMed Retrieval Node

**Goal:** Real literature data flowing in from PubMed for a given condition.

- Implement `query_pubmed` node using NCBI E-utilities (`esearch` + `efetch`)
- Parse article titles, abstracts, and PMIDs from the API response
- Store results in `BriefingState`
- Unit test the node in isolation with a known condition

**Done when:** The node returns structured article data for any condition input.

---

## Phase 3 — ClinicalTrials.gov Retrieval Node

**Goal:** Active and completed trial data flowing in from ClinicalTrials.gov.

- Implement `query_clinicaltrials` node using ClinicalTrials.gov API v2
- Filter for relevant trial phases (Phase 2, 3, 4) and statuses
- Extract trial title, sponsor, status, NCT ID
- Store results in `BriefingState`
- Unit test the node in isolation

**Done when:** The node returns structured trial data for any condition input.

---

## Phase 4 — Parallel Retrieval in the Graph

**Goal:** Both retrieval nodes run in parallel inside the LangGraph, feeding a shared state.

- Wire Phase 2 and Phase 3 nodes into the LangGraph as parallel branches
- Confirm both execute concurrently and results merge correctly into `BriefingState`
- Add basic error handling: if one source fails, the other still completes

**Done when:** A single graph invocation populates state with both PubMed and ClinicalTrials data.

---

## Phase 5 — Claude Synthesis Node

**Goal:** Claude reads retrieved data and produces the three sections of the structured brief.

- Implement `synthesize_brief` node that passes retrieved context to Claude
- Prompt Claude to produce: standard of care, emerging treatments, key organizations
- Return structured JSON (validated with Pydantic)
- Include source citations (PMIDs, NCT numbers) in the output

**Done when:** The full graph produces an accurate, structured brief for a real medical condition.

---

## Phase 6 — REST API Integration and Hardening

**Goal:** The full LangGraph pipeline is exposed cleanly via FastAPI and ready for use.

- Replace the Phase 1 stub with the real graph invocation in `POST /brief`
- Add input validation (condition must be a non-empty string)
- Add error responses for upstream API failures
- Add a `GET /health` endpoint
- Manual accuracy review: run 3–5 real conditions and verify output quality against known sources

**Done when:** The API is stable, handles errors gracefully, and produces accurate briefs on real inputs.

---

## Phase 7 — React UI

**Goal:** A minimal but fully functional web interface that lets users generate and read briefs without touching the API directly.

- Scaffold React app with Vite in `/ui`
- Condition input field and submit button
- `fetch` call to `POST /brief` on form submit
- Loading spinner displayed while awaiting the response
- Render the brief in three clearly labeled sections: Standard of Care, Emerging Treatments, Key Organizations
- Render source citations as links (PubMed URLs from PMIDs, ClinicalTrials.gov URLs from NCT numbers)
- Basic error message if the API call fails
- CORS enabled on the FastAPI backend to allow local development

**Done when:** A user can open the UI in a browser, type a condition, and read a fully formatted brief with clickable source links.

---

## Out of Scope for Now

- Authentication
- Caching / persistence
- Evaluation harness / automated accuracy scoring
- UI component library or design system
