# Phase 7 — React UI: Plan

---

## Group 1 — Backend: CORS

1.1 In `app/main.py`, import `CORSMiddleware` from `fastapi.middleware.cors`

1.2 Register the middleware immediately after the `FastAPI()` app is created:
  - `allow_origins=["http://localhost:5173"]`
  - `allow_methods=["GET", "POST"]`
  - `allow_headers=["Content-Type"]`

1.3 Confirm `GET /health` still returns 200 with the existing test suite

---

## Group 2 — Frontend Scaffold

2.1 In `ui/`, create `package.json` with:
  - `react`, `react-dom` as dependencies
  - `vite`, `@vitejs/plugin-react`, `@playwright/test` as devDependencies
  - Scripts: `dev`, `build`, `preview`, `test`

2.2 Create `ui/vite.config.js` using `@vitejs/plugin-react`

2.3 Create `ui/index.html` — standard Vite HTML entry point mounting `#root`

2.4 Create `ui/src/main.jsx` — renders `<App />` into `#root`

2.5 Run `npm install` inside `ui/` and install Playwright browsers:
  `npx playwright install --with-deps chromium`

---

## Group 3 — App.jsx + App.css

3.1 Create `ui/src/App.jsx` with the following behaviour using only `useState` and `fetch`:

  - **Form**: text input bound to `condition` state + Submit button (disabled when loading or empty)
  - **On submit**: POST to `http://localhost:8000/brief`, set `loading=true`, clear previous results
  - **Loading state**: CSS spinner visible while `loading` is true; button label changes to "Generating…"
  - **Success**: render `.brief` div with four `<section>` blocks — Standard of Care, Emerging
    Treatments, Key Organizations, Sources
  - **Sources**: each source rendered as a clickable `<a>` link:
    - `pmid:XXXXXXXX` → `https://pubmed.ncbi.nlm.nih.gov/XXXXXXXX/`
    - `nct:NCTXXXXXXXX` → `https://clinicaltrials.gov/study/NCTXXXXXXXX`
  - **Error**: display the API error `detail` or a fallback message in a `.error` div

3.2 Create `ui/src/App.css` with styles for:
  - `.app` — centred, max-width container
  - `form` — input + button layout, input takes available width
  - `.spinner` — CSS keyframe animation (rotating border)
  - `.brief`, `section`, `h3` — section card styling
  - `.sources a` — source link colour
  - `.error` — red error banner

---

## Group 4 — Playwright Test

4.1 Create `ui/playwright.config.js`:
  - `testDir: './tests'`
  - `use: { baseURL: 'http://localhost:5173' }`
  - Timeout: 90 000ms per test (API calls can take ~30s)

4.2 Create `ui/tests/brief.spec.js` with two tests:

  **`submit button disabled when input is empty`**
  - Navigate to `/`
  - Assert the submit button is disabled

  **`generates and renders a brief for a real condition`**
  - Navigate to `/`
  - Fill the input with `"asthma"`
  - Click Submit
  - Assert the spinner appears
  - Wait up to 90s for `.brief` to appear
  - Assert all four `<h3>` headings are visible
  - Assert at least one `.sources a` link is present and has an `href` starting with `https://`

---

## Group 5 — Run Tests

5.1 In one terminal: start the backend
  `ANTHROPIC_API_KEY=... uvicorn app.main:app --reload`

5.2 In a second terminal: start the Vite dev server
  `cd ui && npm run dev`

5.3 In a third terminal: run Playwright
  `cd ui && npm test`

5.4 All tests must pass
