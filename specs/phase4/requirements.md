# Phase 4 — Parallel Retrieval in the Graph: Requirements

## Scope

Phase 4 adds observability and fault tolerance to the two retrieval nodes. The graph topology (`app/graph.py`) is unchanged — it has had parallel fan-out from START since Phase 1. This phase confirms it and makes it resilient.

---

## What is in scope

- `app/nodes.py` — thread ID logging added to both retrieval nodes; retry logic added to both nodes
- `app/graph.py` — logging initialised in the `__main__` block only
- `tests/test_parallel.py` — two new tests covering concurrency proof and fault isolation

## What is out of scope for this phase

- Any changes to the graph topology
- Any changes to `app/pubmed.py` or `app/clinicaltrials.py`
- Any changes to FastAPI endpoints
- Claude synthesis (Phase 5)

---

## Decisions

### Parallelism is LangGraph-native

LangGraph's `StateGraph` runs fan-out nodes (multiple edges from one node) in separate threads by default. No threading code needs to be added to the graph. The proof is in the thread IDs logged by the nodes — they will differ, confirming true concurrent execution.

### Error handling: retry once, then return empty list

When a retrieval node's fetch call raises any exception:

1. Log a `WARNING` with the exception message
2. Retry the call once
3. If the retry also raises, log another `WARNING` and return `[]` for that node's field

The graph continues with whatever data the surviving node provided. A brief generated from one source is better than no brief at all.

The retry helper `_fetch_with_retry` lives in `app/nodes.py` since it is only used there. It is a private function.

### Logging with stdlib logging module

Use Python's standard `logging` module. Logger is scoped to the module (`__name__`). No logging configuration is added to application startup — configuration belongs to the caller (`__main__` or a future application entry point), not the library code.

### Fault isolation tested with monkeypatch

The test for fault isolation uses `pytest`'s built-in `monkeypatch` fixture to replace one fetch function with one that raises. This is faster and deterministic compared to network-level simulation, and it tests exactly the error path in the node code.

---

## Context

This phase corresponds to **Phase 4** in `specs/roadmap.md`. Success criteria are in `specs/phase4/validation.md`.
