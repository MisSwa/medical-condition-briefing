# Phase 6 — REST API Integration and Hardening: Plan

---

## Group 1 — Input Validation

1.1 Update `BriefRequest` in `app/models.py`:
  - Add `from pydantic import field_validator`
  - Add a `@field_validator("condition")` class method that:
    - Strips leading/trailing whitespace
    - Raises `ValueError("condition must not be empty")` if the stripped value is empty
    - Returns the stripped value

FastAPI automatically converts Pydantic `ValueError` into a `422 Unprocessable Entity` with a
structured error body — no extra endpoint code required.

---

## Group 2 — Real Endpoint

2.1 In `app/main.py`, remove the noqa comment from the `briefing_graph` import — it is now
  actively used

2.2 Add `from fastapi import HTTPException` to imports

2.3 Add `from app.state import BriefingState` to imports

2.4 Replace the stub body of `create_brief` with:
  - Build `initial_state: BriefingState` from `request.condition` with empty lists/dicts
  - Wrap `briefing_graph.invoke(initial_state)` in a `try / except Exception`
  - On success: return `BriefResponse(**state["brief"])` — the `brief` dict is already fully
    validated and shaped by `format_output` in Phase 5
  - On exception: raise `HTTPException(status_code=503, detail=f"Brief generation failed: {exc}")`

---

## Group 3 — Updated Tests

The existing `test_brief_stub` tested the hardcoded stub. Now that the endpoint runs the real
graph, the unit test must mock graph invocation — otherwise every `pytest` run calls three live
APIs.

3.1 Update `tests/test_api.py`:
  - Rename `test_brief_stub` → `test_brief_returns_correct_shape`
  - Add a `monkeypatch` parameter; patch `briefing_graph.invoke` in `app.main` to return a
    fake `BriefingState` with a fully-populated `brief` dict
  - Add `test_brief_empty_condition_returns_422`: POST with `{"condition": ""}`, assert 422
  - Add `test_brief_whitespace_condition_returns_422`: POST with `{"condition": "   "}`, assert 422
  - Add `test_brief_upstream_failure_returns_503`: patch graph invoke to raise `RuntimeError`,
    assert 503 and that the detail message contains "Brief generation failed"

3.2 Run the full test suite (`pytest -v`) — all 9 tests must pass

---

## Group 4 — Manual Accuracy Review

4.1 Run the server: `ANTHROPIC_API_KEY=... uvicorn app.main:app`

4.2 Call `POST /brief` for all five conditions:
  - asthma
  - type 2 diabetes
  - breast cancer
  - Alzheimer's disease
  - Parkinson's disease

4.3 For each: verify standard_of_care, emerging_treatments, key_organizations are accurate
  and that at least one `pmid:` and one `nct:` source is present

4.4 Record the accuracy verdict (pass/fail per condition) in `specs/phase6/validation.md`
