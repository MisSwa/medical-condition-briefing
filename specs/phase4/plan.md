# Phase 4 — Parallel Retrieval in the Graph: Plan

The LangGraph topology was locked in Phase 1. The build work here is two things: proving concurrent execution, and adding fault tolerance to both retrieval nodes.

---

## Group 1 — Thread ID Logging

1.1 Add `import logging` and `import threading` to `app/nodes.py`

1.2 Create a module-level logger: `logger = logging.getLogger(__name__)`

1.3 In `query_pubmed`, add log statements at entry and exit:
  - Entry: `logger.info("query_pubmed start thread=%s", threading.get_ident())`
  - Exit: `logger.info("query_pubmed done  thread=%s", threading.get_ident())`

1.4 Do the same in `query_clinicaltrials`

1.5 In `app/graph.py`, add `logging.basicConfig(level=logging.INFO)` inside the `if __name__ == "__main__"` block so thread IDs are visible when the graph is run directly

---

## Group 2 — Retry-Once Error Handling

2.1 Add a private helper `_fetch_with_retry(fetch_fn, *args) -> list` to `app/nodes.py`:
  - First attempt: call `fetch_fn(*args)` and return the result
  - On any exception: log a warning, make one retry
  - If the retry also fails: log a warning and return `[]`

2.2 Update `query_pubmed` to call `_fetch_with_retry(fetch_pubmed_articles, state["condition"])` instead of calling `fetch_pubmed_articles` directly

2.3 Update `query_clinicaltrials` to call `_fetch_with_retry(fetch_clinical_trials, state["condition"])` instead of calling `fetch_clinical_trials` directly

---

## Group 3 — Tests

3.1 Create `tests/test_parallel.py` with two tests:

  **`test_parallel_thread_ids_differ`**
  - Patch both retrieval functions to record their thread ID and return `[]`
  - Invoke `briefing_graph` with a test state
  - Assert the two recorded thread IDs are different

  **`test_clinicaltrials_failure_does_not_block_pubmed`**
  - Monkeypatch `fetch_clinical_trials` to raise a `RuntimeError`
  - Invoke `briefing_graph` against the live PubMed API
  - Assert `pubmed_results` is non-empty
  - Assert `trial_results` is `[]`

3.2 Run the full test suite (`pytest -v`) and confirm all tests pass
