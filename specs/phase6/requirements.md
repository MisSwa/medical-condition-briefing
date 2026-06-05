# Phase 6 — REST API Integration and Hardening: Requirements

## Scope

Phase 6 replaces the `POST /brief` stub with the real LangGraph pipeline and hardens the API
with input validation and error handling. After this phase the backend is production-ready.

---

## What is in scope

- `app/models.py` — `BriefRequest` gains a field validator for non-empty condition
- `app/main.py` — real graph invocation with 503 error handling
- `tests/test_api.py` — updated and expanded API unit tests (graph mocked)

## What is out of scope for this phase

- CORS (added in Phase 7 for the React UI)
- Authentication
- Request timeouts (graph has its own network timeouts per node)
- Response caching

---

## Decisions

### Input validation via Pydantic field_validator (422)

Validation lives in `BriefRequest`, not in the endpoint handler. FastAPI converts any Pydantic
`ValueError` into a `422 Unprocessable Entity` automatically, with a structured JSON error body
locating the offending field. The validator strips whitespace before the empty check, so
`"  "` (spaces only) is also rejected.

### Upstream failures → 503 Service Unavailable

If `briefing_graph.invoke()` raises for any reason — Claude API error, network failure not
caught by Phase 4's retry logic, unexpected exception — the endpoint catches it and returns
`503 Service Unavailable` with a `detail` string prefixed `"Brief generation failed: ..."`.

503 is the correct code: the server is functional but a downstream dependency is unavailable.
The caller can retry. A 500 would imply a bug in the server itself.

Note: empty `pubmed_results` or `trial_results` (source API returned nothing) is **not** an
error — Phase 4's retry logic handles that gracefully and the graph completes. Only an
unhandled exception from the graph itself triggers the 503.

### API unit tests mock the graph

`tests/test_api.py` tests endpoint behaviour in isolation. Since Phases 2–5 already have their
own live integration tests, the API unit tests mock `briefing_graph.invoke` to avoid redundant
live API calls in every `pytest` run. The mock is patched on `app.main.briefing_graph` — the
object as imported into the main module's namespace.

### BriefResponse is the single response schema

`state["brief"]` after `format_output` is already a fully validated `BriefResponse.model_dump()`
dict. The endpoint simply unpacks it: `BriefResponse(**state["brief"])`. No re-validation or
field mapping is needed.

---

## HTTP status codes

| Scenario | Code |
|---|---|
| Success | 200 OK |
| Empty or whitespace condition | 422 Unprocessable Entity |
| Graph raises any exception | 503 Service Unavailable |
| Any other unhandled exception | 500 (FastAPI default) |

---

## Context

This phase corresponds to **Phase 6** in `specs/roadmap.md`. After this phase the backend is
fully functional. Phase 7 adds the React UI and CORS.
