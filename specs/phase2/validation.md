# Phase 2 — PubMed Retrieval Node: Validation

Phase 2 is complete when all checks below pass.

---

## 1. Existing tests still pass

```bash
pytest tests/test_api.py -v
```

Expected: both Phase 1 tests pass unchanged. Phase 2 must not break the existing API contract.

```
tests/test_api.py::test_health PASSED
tests/test_api.py::test_brief_stub PASSED
```

---

## 2. PubMed node returns structured data for a real condition

```bash
pytest tests/test_pubmed.py -v
```

Expected:

```
tests/test_pubmed.py::test_query_pubmed_returns_articles PASSED
```

This test calls `query_pubmed` with `{"condition": "asthma", "pubmed_results": [], "trial_results": [], "brief": {}}` against the live PubMed API and asserts:

- The return dict contains key `pubmed_results`
- `pubmed_results` is a non-empty list
- Each item in the list has keys `pmid`, `title`, `abstract`
- Each `pmid` is a non-empty string
- Each `title` is a non-empty string

---

## 3. Manual spot-check of result quality

Run the graph module directly and inspect the output:

```bash
python -m app.graph
```

Inspect the printed `BriefingState`. `pubmed_results` should contain 5 or fewer real articles about asthma with readable titles and abstracts. Confirm no garbled text, empty fields, or XML artifacts appear in the output.

---

## 4. Full test suite passes

```bash
pytest -v
```

Expected: all tests collected across `tests/` pass with no failures.

---

## Phase 2 is NOT complete if:

- `query_pubmed` returns an empty list for a common condition like "asthma" or "diabetes"
- Any article dict is missing `pmid`, `title`, or `abstract`
- Abstract text contains raw XML tags or is an empty string for articles that have abstracts
- Any Phase 1 test breaks
- `pytest` reports any failures or errors
