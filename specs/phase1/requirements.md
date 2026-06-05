# Phase 1 — Project Skeleton: Requirements

## Scope

Phase 1 establishes the project skeleton only. No real data is fetched, no LLM is called. Every node and endpoint returns hardcoded or no-op responses. The goal is a runnable, importable, testable foundation that all subsequent phases build on.

---

## What is in scope

- Top-level directory structure (`app/`, `ui/`, `tests/`, `specs/`)
- Dependency management with `pip` and `requirements.txt`
- A running FastAPI app with a stub `POST /brief` endpoint
- A LangGraph `StateGraph` with the correct node topology but no-op node logic
- A working test suite directory with at least two passing tests
- A `GET /health` endpoint

## What is out of scope for this phase

- Any real HTTP calls to PubMed or ClinicalTrials.gov
- Any call to the Claude API
- CORS configuration (added in Phase 7 when the React UI is built)
- The `/ui` React app (scaffolded in Phase 7)
- Authentication, caching, or persistence

---

## Decisions

### Dependency management: pip + requirements.txt

Use `pip` with a flat `requirements.txt`. All packages must be pinned to exact versions after the initial install (`pip freeze > requirements.txt`). This keeps the setup familiar and portable without introducing additional tooling.

Virtual environment: standard `python -m venv venv`. The `venv/` directory is gitignored.

### Python version: 3.11+

LangGraph and the Anthropic SDK require 3.10 minimum. 3.11 is the target for this project — it is widely available, stable, and offers meaningful performance improvements over 3.10.

### LangGraph state: TypedDict

`BriefingState` is defined as a `TypedDict` (not a dataclass or Pydantic model). LangGraph's `StateGraph` works with `TypedDict` natively and this is the idiomatic approach in LangGraph documentation.

### Stub response shape

The hardcoded stub from `POST /brief` must match the final `BriefResponse` schema exactly — same fields, same types. This ensures the test written in Phase 1 remains valid when real data replaces the stub in Phase 6, with no changes to the test contract.

`BriefResponse` schema:
```json
{
  "condition": "string",
  "standard_of_care": ["string"],
  "emerging_treatments": ["string"],
  "key_organizations": ["string"],
  "sources": ["string"]
}
```

### Graph topology locked in Phase 1

The node names and edge structure of the LangGraph graph are defined in this phase and must not change in later phases — only the node implementations change. This prevents breaking imports or state field names across phases.

---

## Context

This phase corresponds to **Phase 1** in `specs/roadmap.md`. The tech choices here are governed by `specs/techstack.md`. Key reference points:

- Backend: Python 3.11 + FastAPI + LangGraph
- The graph topology (parallel PubMed + ClinicalTrials nodes → synthesis → format) is defined in `specs/techstack.md`
- Success criteria are defined in `specs/phase1/validation.md`
