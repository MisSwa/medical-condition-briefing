# Phase 6 — REST API Integration and Hardening: Validation

Phase 6 is complete when all checks below pass.

---

## 1. Existing tests still pass

```bash
pytest tests/test_pubmed.py tests/test_clinicaltrials.py tests/test_parallel.py tests/test_synthesis.py -v
```

Expected: all 5 tests from Phases 2–5 pass unchanged.

---

## 2. API unit tests pass (9 total)

```bash
pytest tests/test_api.py -v
```

Expected tests and assertions:

| Test | Asserts |
|---|---|
| `test_health` | GET /health → 200, `{"status":"ok"}` |
| `test_brief_returns_correct_shape` | POST /brief (mocked graph) → 200, all 5 fields present |
| `test_brief_empty_condition_returns_422` | POST with `""` → 422 |
| `test_brief_whitespace_condition_returns_422` | POST with `"   "` → 422 |
| `test_brief_upstream_failure_returns_503` | POST (graph raises) → 503, detail contains "Brief generation failed" |

---

## 3. Full test suite passes

```bash
pytest -v
```

Expected: 9 tests collected, 9 passed.

---

## 4. Manual accuracy review

Run with the API key set:

```bash
ANTHROPIC_API_KEY=... uvicorn app.main:app --reload
```

Then POST each condition and assess:

| Condition | Standard of Care accurate? | Emerging Treatments accurate? | Sources present? | Verdict |
|---|---|---|---|---|
| Asthma | ✓ ICS/LABA, corticosteroids | ✓ Biologics, MOTS-c, lipid targeting | 5 pmid + 3 nct | PASS |
| Type 2 Diabetes | ✓ GLP-1, SGLT2, neuropathy Mx | ✓ Finerenone, VX-264, apabetalone | 5 pmid + 5 nct | PASS |
| Breast Cancer | ✓ Subtype stratification, BCS, axillary Mx | ✓ Dato-DXd, sacituzumab, ENLIGHT algorithm | 5 pmid + 5 nct | PASS |
| Alzheimer's Disease | ✓ Amyloid-β targeting, tau-PET staging | ✓ BIIB080, MK-2214, trontinemab, VY7523 | 5 pmid + 5 nct | PASS |
| Parkinson's Disease | ✓ Symptom Mx, UK Brain Bank criteria | ✓ RNDP-001 implant, CVN424, microbiome therapy | 5 pmid + 2 nct | PASS |

All five conditions returned 200 with non-empty sections and correctly prefixed sources.

---

## Phase 6 is NOT complete if:

- `POST /brief` with a valid condition returns anything other than 200
- `POST /brief` with an empty string returns anything other than 422
- `POST /brief` when the graph raises returns anything other than 503
- Any prior test breaks
- `pytest` reports any failures or errors
