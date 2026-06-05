# Phase 3 — ClinicalTrials.gov Retrieval Node: Validation

Phase 3 is complete when all checks below pass.

---

## 1. Existing tests still pass

```bash
pytest tests/test_api.py tests/test_pubmed.py -v
```

Expected: all Phase 1 and Phase 2 tests pass unchanged.

```
tests/test_api.py::test_health PASSED
tests/test_api.py::test_brief_stub PASSED
tests/test_pubmed.py::test_query_pubmed_returns_articles PASSED
```

---

## 2. ClinicalTrials node returns structured trial data

```bash
pytest tests/test_clinicaltrials.py -v
```

Expected:

```
tests/test_clinicaltrials.py::test_query_clinicaltrials_returns_trials PASSED
```

This test calls `query_clinicaltrials` with `{"condition": "diabetes", ...}` against the live ClinicalTrials.gov API and asserts:

- The return dict contains key `trial_results`
- `trial_results` is a non-empty list
- Each item has keys `nct_id`, `title`, `status`, `sponsor`
- Each `nct_id` starts with `"NCT"`
- Each `status` is one of `RECRUITING` or `ACTIVE_NOT_RECRUITING`

---

## 3. Manual spot-check of result quality

Run the graph module directly and inspect the output:

```bash
python -m app.graph
```

Inspect the printed `BriefingState`. `trial_results` should contain up to 5 real trials for "asthma" with readable titles, valid NCT IDs, and recognisable sponsor names (hospitals, universities, or pharma companies). Confirm no empty fields or raw JSON artefacts.

---

## 4. Full test suite passes

```bash
pytest -v
```

Expected: all 4 tests pass with no failures.

```
tests/test_api.py::test_health PASSED
tests/test_api.py::test_brief_stub PASSED
tests/test_pubmed.py::test_query_pubmed_returns_articles PASSED
tests/test_clinicaltrials.py::test_query_clinicaltrials_returns_trials PASSED
```

---

## Phase 3 is NOT complete if:

- `query_clinicaltrials` returns an empty list for a common condition like "diabetes" or "asthma"
- Any trial dict is missing `nct_id`, `title`, `status`, or `sponsor`
- Any `nct_id` does not start with `"NCT"`
- Any returned status is outside the configured filter (`RECRUITING`, `ACTIVE_NOT_RECRUITING`)
- Any Phase 1 or Phase 2 test breaks
- `pytest` reports any failures or errors
