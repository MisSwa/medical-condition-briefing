# Phase 4 — Parallel Retrieval in the Graph: Validation

Phase 4 is complete when all checks below pass.

---

## 1. Existing tests still pass

```bash
pytest tests/test_api.py tests/test_pubmed.py tests/test_clinicaltrials.py -v
```

Expected: all 4 prior tests pass unchanged.

---

## 2. Parallelism confirmed — thread IDs differ

```bash
pytest tests/test_parallel.py::test_parallel_thread_ids_differ -v
```

Expected: `PASSED`. The test asserts that `query_pubmed` and `query_clinicaltrials` run on different threads during a single graph invocation.

> Note: fake functions in the test include a `time.sleep(0.05)` to force genuine thread overlap. Without any pause, both tasks may complete before the thread pool needs a second thread, causing the pool to reuse the same thread for both — a false negative. The sleep is not a workaround; it reflects reality: nodes with real I/O (network calls) will always overlap and always get different threads.

---

## 3. Fault isolation confirmed — one failure does not block the other

```bash
pytest tests/test_parallel.py::test_clinicaltrials_failure_does_not_block_pubmed -v
```

Expected: `PASSED`. With `fetch_clinical_trials` forced to raise, the graph completes and `pubmed_results` is non-empty while `trial_results` is `[]`.

---

## 4. Thread IDs visible in manual run

```bash
python -m app.graph
```

Expected log output contains lines similar to:
```
INFO:app.nodes:query_pubmed start       thread=<id_A>
INFO:app.nodes:query_clinicaltrials start thread=<id_B>
```

Where `<id_A>` and `<id_B>` are different integers, confirming concurrent execution.

---

## 5. Full test suite passes

```bash
pytest -v
```

Expected: 6 tests collected, 6 passed, 0 failed.

---

## Phase 4 is NOT complete if:

- Thread IDs logged by both retrieval nodes are the same (sequential, not parallel)
- `test_clinicaltrials_failure_does_not_block_pubmed` fails (fault isolation broken)
- Any prior test breaks
- `pytest` reports any failures or errors
