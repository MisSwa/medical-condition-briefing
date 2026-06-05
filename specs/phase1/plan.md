# Phase 1 — Project Skeleton: Plan

Tasks are organized by layer. Complete each group before moving to the next — later groups depend on earlier ones being in place.

---

## Group 1 — Repo & Environment Setup

1.1 Create top-level directory structure: `app/`, `ui/`, `tests/`
1.2 Create `app/__init__.py` and `tests/__init__.py`
1.3 Create `.gitignore` covering `__pycache__`, `.env`, `venv/`, `*.pyc`
1.4 Create `requirements.txt` with pinned backend dependencies:
  - `fastapi`
  - `uvicorn[standard]`
  - `langgraph`
  - `langchain-anthropic`
  - `anthropic`
  - `httpx`
  - `pydantic`
  - `pytest`
  - `httpx` (used by pytest for test client)

1.5 Create a virtual environment (`python -m venv venv`) and install requirements
1.6 Verify all packages import without error

---

## Group 2 — FastAPI Scaffold

2.1 Create `app/models.py` with two Pydantic models:
  - `BriefRequest` — one field: `condition: str`
  - `BriefResponse` — fields: `condition`, `standard_of_care`, `emerging_treatments`, `key_organizations`, `sources`

2.2 Create `app/main.py` with:
  - FastAPI app instance
  - `POST /brief` endpoint that accepts `BriefRequest` and returns a hardcoded `BriefResponse`
  - `GET /health` endpoint returning `{"status": "ok"}`

2.3 Confirm the server starts: `uvicorn app.main:app --reload`
2.4 Confirm the auto-generated docs are accessible at `/docs`

---

## Group 3 — LangGraph Skeleton

3.1 Create `app/state.py` — define `BriefingState` as a `TypedDict` with fields for condition, raw pubmed results, raw trial results, and the final brief

3.2 Create `app/nodes.py` — define four no-op node functions that accept and return `BriefingState` unchanged:
  - `query_pubmed`
  - `query_clinicaltrials`
  - `synthesize_brief`
  - `format_output`

3.3 Create `app/graph.py` — wire nodes into a `StateGraph`:
  - Parallel edges from `START` to `query_pubmed` and `query_clinicaltrials`
  - Both converge to `synthesize_brief`
  - `synthesize_brief` → `format_output` → `END`
  - Compile the graph and export as `briefing_graph`

3.4 Add a `if __name__ == "__main__"` block in `app/graph.py` to invoke the compiled graph with a test condition and print state — confirms the graph runs end-to-end

3.5 Import `briefing_graph` from `app/main.py` to confirm no import errors on startup

---

## Group 4 — Test Structure

4.1 Create `tests/conftest.py` with a `pytest` fixture that returns a `TestClient` from `fastapi.testclient`

4.2 Create `tests/test_api.py` with two tests:
  - `test_health` — GET `/health` returns 200 and `{"status": "ok"}`
  - `test_brief_stub` — POST `/brief` with `{"condition": "asthma"}` returns 200 and a response body that matches the `BriefResponse` schema

4.3 Confirm `pytest` discovers and runs both tests with no failures

4.4 Create `pytest.ini` (or `[tool.pytest.ini_options]` in a `pyproject.toml`) pointing test discovery at `tests/`
