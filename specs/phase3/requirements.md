# Phase 3 — ClinicalTrials.gov Retrieval Node: Requirements

## Scope

Phase 3 replaces the no-op `query_clinicaltrials` LangGraph node with a real implementation that fetches clinical trial data from ClinicalTrials.gov via its v2 API. All other nodes and endpoints remain unchanged from Phase 2.

---

## What is in scope

- `app/clinicaltrials.py` — new module containing the ClinicalTrials.gov fetch logic
- `app/nodes.py` — `query_clinicaltrials` function updated to call the real client
- `tests/test_clinicaltrials.py` — live integration test for the node

## What is out of scope for this phase

- PubMed retrieval (completed in Phase 2)
- Claude synthesis (Phase 5)
- Any changes to the FastAPI endpoints or response shape
- Changes to any other LangGraph node
- Caching or deduplication of trial results

---

## Decisions

### API: ClinicalTrials.gov API v2 (no key required)

Use the public ClinicalTrials.gov REST API v2. No authentication is required.

Base URL: `https://clinicaltrials.gov/api/v2/studies`

### Result limit: 5, filtered to active trial phases and statuses

Fetch a maximum of 5 trials per condition with:
- **Status filter**: `RECRUITING` and `ACTIVE_NOT_RECRUITING` — captures trials currently running or actively enrolling. Excludes completed, terminated, and not-yet-started trials.
- **Phase filter**: `PHASE2`, `PHASE3`, `PHASE4` — excludes early-phase and phase 1 trials that are too early to represent emerging treatments.

### Fields to extract

Each trial is stored as:
```python
{
    "nct_id": str,   # e.g. "NCT05123456"
    "title": str,    # brief title of the trial
    "status": str,   # e.g. "RECRUITING" or "ACTIVE_NOT_RECRUITING"
    "sponsor": str,  # lead sponsor name (institution or company)
}
```

The `sponsor` field populates the "Key Organizations" section in the final brief. It is extracted from `leadSponsor.name` in the API response.

### Response format: JSON (API default)

The v2 API returns JSON by default. No format parameter is needed. Parse with Python's built-in `json` (handled by `httpx` automatically via `.json()`).

### Defensive parsing with `.get()`

The `protocolSection` nested structure can have missing modules for some trials. Use `.get()` at every level so a malformed record is skipped cleanly rather than raising a `KeyError`.

### State field: `trial_results`

Results are stored in `BriefingState["trial_results"]`. This field was defined in Phase 1 and its type (`list[dict[str, Any]]`) remains unchanged.

### HTTP client: urllib.request (standard library)

ClinicalTrials.gov's WAF blocks requests from `httpx` (returns 403) due to TLS fingerprint differences between httpx and libcurl. `urllib.request` from the Python standard library is not blocked and requires no additional dependency. `httpx` remains the client for PubMed (which has no such restriction).

### Structural parity with pubmed.py

`clinicaltrials.py` follows the same module structure as `pubmed.py`:
- One public function
- Private `_fetch` helper for the HTTP call
- Private `_parse_trials` helper for JSON → list[dict]

This keeps the two retrieval modules easy to read and maintain side-by-side.

---

## Context

This phase corresponds to **Phase 3** in `specs/roadmap.md`. The `query_clinicaltrials` node name and its position in the graph topology are locked from Phase 1 — only the implementation changes. `app/graph.py` is not touched.
