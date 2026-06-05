# Phase 3 — ClinicalTrials.gov Retrieval Node: Plan

Tasks are organized by layer. Complete each group before moving to the next.

---

## Group 1 — ClinicalTrials Client

1.1 Create `app/clinicaltrials.py` with a single public function mirroring the pubmed.py pattern:
  `fetch_clinical_trials(condition: str, max_results: int = 5) -> list[dict]`

1.2 Implement the **fetch step** — a private `_fetch(condition, max_results)` helper that calls:
  `https://clinicaltrials.gov/api/v2/studies`
  with parameters:
  - `query.cond` = condition
  - `filter.overallStatus` = `RECRUITING,ACTIVE_NOT_RECRUITING`
  - `filter.phase` = `PHASE2,PHASE3,PHASE4`
  - `pageSize` = max_results
  Returns the raw JSON response dict.

1.3 Implement the **parse step** — a private `_parse_trials(data)` helper that extracts from each study in `data["studies"]`:
  - `nct_id` — from `protocolSection.identificationModule.nctId`
  - `title` — from `protocolSection.identificationModule.briefTitle`
  - `status` — from `protocolSection.statusModule.overallStatus`
  - `sponsor` — from `protocolSection.sponsorCollaboratorsModule.leadSponsor.name`

1.4 Return a `list[dict]` with one entry per trial:
  `{"nct_id": str, "title": str, "status": str, "sponsor": str}`

1.5 Guard against missing nested keys — use `.get()` at each level so a malformed study record is skipped rather than raising a `KeyError`

---

## Group 2 — Wire into LangGraph Node

2.1 Update `query_clinicaltrials` in `app/nodes.py`:
  - Import `fetch_clinical_trials` from `app.clinicaltrials`
  - Call it with `state["condition"]`
  - Return `{"trial_results": results}` as a partial state update

2.2 Confirm existing tests still pass

---

## Group 3 — Tests

3.1 Create `tests/test_clinicaltrials.py` with a live integration test:
  - Call `query_clinicaltrials` with a state dict containing `condition = "diabetes"`
  - Assert the return dict has key `trial_results`
  - Assert `trial_results` is a non-empty list
  - Assert each item has keys `nct_id`, `title`, `status`, `sponsor`
  - Assert each `nct_id` starts with `"NCT"`

3.2 Run the full test suite (`pytest -v`) and confirm all tests pass
