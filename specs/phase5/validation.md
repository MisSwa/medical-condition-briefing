# Phase 5 — Claude Synthesis Node: Validation

Phase 5 is complete when all checks below pass.

---

## 0. Prerequisite — API key is set

```bash
echo $ANTHROPIC_API_KEY
```

Must return a non-empty string. All subsequent checks depend on this.

---

## 1. Existing tests still pass

```bash
pytest tests/test_api.py tests/test_pubmed.py tests/test_clinicaltrials.py tests/test_parallel.py -v
```

Expected: all 6 prior tests pass unchanged.

---

## 2. End-to-end synthesis test passes

```bash
pytest tests/test_synthesis.py -v
```

Expected:

```
tests/test_synthesis.py::test_full_graph_produces_brief PASSED
```

This test runs the full graph for `condition = "type 2 diabetes"` and asserts:

- `result["brief"]` is a non-empty dict
- Keys present: `condition`, `standard_of_care`, `emerging_treatments`, `key_organizations`, `sources`
- `standard_of_care`, `emerging_treatments`, `key_organizations`, `sources` are all non-empty lists
- At least one source starts with `"pmid:"` or `"nct:"`

---

## 3. Full test suite passes

```bash
pytest -v
```

Expected: 7 tests collected, 7 passed, 0 failed.

---

## 4. Manual quality review

```bash
python -m app.graph
```

Read the `brief` field in the printed `BriefingState`. Manually verify:

| Section | Quality bar |
|---|---|
| `standard_of_care` | Names at least one real, commonly used treatment for asthma |
| `emerging_treatments` | References at least one drug, biologic, or approach currently in trials |
| `key_organizations` | Names at least one real hospital, university, or pharma company |
| `sources` | At least one `pmid:` and one `nct:` entry that match data retrieved in the run |

---

## Phase 5 is NOT complete if:

- `ANTHROPIC_API_KEY` is not set or the Claude API call fails
- Any brief field is an empty list
- No sources use the `pmid:` or `nct:` prefix format
- The brief content is generic boilerplate unrelated to the retrieved PubMed / trial data
- Any prior test breaks
- `pytest` reports any failures or errors
