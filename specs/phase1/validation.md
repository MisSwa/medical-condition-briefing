# Phase 1 — Project Skeleton: Validation

Phase 1 is complete when all checks below pass. Each check must be verified manually unless noted.

---

## 1. Server starts cleanly

```bash
uvicorn app.main:app --reload
```

Expected: Server starts with no errors or import warnings. Output should include:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## 2. Health endpoint responds

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "ok"}
```

---

## 3. Stub brief endpoint responds with the correct shape

```bash
curl -X POST http://localhost:8000/brief \
  -H "Content-Type: application/json" \
  -d '{"condition": "asthma"}'
```

Expected: HTTP 200 with a JSON body that contains all five fields:

```json
{
  "condition": "asthma",
  "standard_of_care": ["..."],
  "emerging_treatments": ["..."],
  "key_organizations": ["..."],
  "sources": ["..."]
}
```

The values may be hardcoded placeholders — what is validated here is the shape, not the content.

---

## 4. LangGraph graph runs end-to-end

```bash
python -m app.graph
```

Expected: The script exits without error and prints the final `BriefingState` to stdout (even if all fields are empty/None from no-op nodes). This confirms the graph compiles, all nodes are reachable, and the state flows from START to END.

> Note: run as a module (`-m app.graph`) from the project root, not as a script (`python app/graph.py`), so that the `app` package is on the path.

---

## 5. pytest passes with full test structure in place

```bash
pytest
```

Expected output:
```
collected 2 items

tests/test_api.py::test_health PASSED
tests/test_api.py::test_brief_stub PASSED

2 passed
```

Both of these must pass:

| Test | What it checks |
|---|---|
| `test_health` | GET `/health` returns 200 and `{"status": "ok"}` |
| `test_brief_stub` | POST `/brief` with `{"condition": "asthma"}` returns 200 and a body with all five expected fields present |

The `/tests` directory must be set up such that future phases can add tests without any structural changes.

---

## 6. Directory structure is correct

```
/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── state.py
│   ├── nodes.py
│   └── graph.py
├── ui/               ← exists as an empty placeholder
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_api.py
├── specs/
├── requirements.txt
├── pytest.ini        ← or equivalent config
└── .gitignore
```

---

## Phase 1 is NOT complete if:

- The server fails to start due to import errors or missing dependencies
- `POST /brief` returns any status other than 200
- The response body is missing any of the five fields from `BriefResponse`
- `pytest` fails, errors, or cannot discover the tests
- The LangGraph graph fails to compile or raises an error when invoked
