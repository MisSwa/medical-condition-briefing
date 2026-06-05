# Phase 7 — React UI: Validation

Phase 7 is complete when all checks below pass.

---

## 0. Prerequisites

- `ANTHROPIC_API_KEY` is set in the terminal running the backend
- Node.js is available (`node --version`)
- `npm install` has been run inside `ui/`
- Playwright Chromium is installed (`npx playwright install chromium`)

---

## 1. Backend tests still pass

```bash
pytest -v
```

Expected: all 10 tests pass. The CORS middleware must not break any existing test.

---

## 2. Playwright end-to-end tests pass

Start both servers, then run:

```bash
# Terminal 1 — backend
ANTHROPIC_API_KEY=... uvicorn app.main:app --reload

# Terminal 2 — frontend
cd ui && npm run dev

# Terminal 3 — tests
cd ui && npm test
```

Expected:

```
Running 2 tests using 1 worker

  ✓ submit button disabled when input is empty
  ✓ generates and renders a brief for a real condition

  2 passed
```

---

## 3. Manual browser walkthrough

Open `http://localhost:5173` and verify:

| Step | Expected |
|---|---|
| Page loads | Title visible, input and Submit button present |
| Submit with empty input | Button is disabled — cannot submit |
| Type "asthma", click Submit | Button changes to "Generating…", spinner appears |
| Brief arrives | Three sections visible: Standard of Care, Emerging Treatments, Key Organizations |
| Sources section | At least one link present; clicking opens PubMed or ClinicalTrials.gov in a new tab |
| Error path | Stop the backend, submit again — error message appears |

---

## 4. CORS verified

With the Vite dev server running, open the browser DevTools Network tab, submit a condition,
and confirm the `POST /brief` request:
- Origin header is `http://localhost:5173`
- Response includes `access-control-allow-origin: http://localhost:5173`
- No CORS error in the Console

---

## Phase 7 is NOT complete if:

- The Submit button is not disabled when the input is empty
- The spinner does not appear after clicking Submit
- The brief sections do not render after the API responds
- Source links do not open PubMed / ClinicalTrials.gov URLs
- A CORS error appears in the browser console
- Either Playwright test fails
- Any prior backend test breaks
