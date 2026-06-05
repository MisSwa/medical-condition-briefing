# Phase 7 — React UI: Requirements

## Scope

Phase 7 adds a minimal but fully functional React web interface and enables CORS on the
FastAPI backend. After this phase a non-technical user can open a browser, type a medical
condition, and read a structured brief with clickable source citations.

---

## What is in scope

- `app/main.py` — CORS middleware for `http://localhost:5173`
- `ui/` — complete React + Vite frontend
- `ui/tests/brief.spec.js` — Playwright end-to-end tests

## What is out of scope

- Authentication or user accounts
- UI component library or design system
- Mobile / responsive optimisation
- Production deployment or build pipeline
- Backend-served static files

---

## Decisions

### Structure: App.jsx + App.css

Two files — logic and styles are separated for readability but not further decomposed. At this
scope (one page, one state machine) sub-components would be premature. Both files live in
`ui/src/`.

### CORS: localhost:5173 only

Vite's default dev server port. Only this origin is added to `allow_origins`. Wildcard (`*`)
is not used. Adding further origins requires an explicit change — this is the right default.

### API base URL: hardcoded to http://localhost:8000

For v1 the backend and frontend are both local. No environment variable abstraction is added —
that belongs in a deployment phase, not here.

### Source link URL construction

| Prefix | URL pattern |
|---|---|
| `pmid:XXXXXXXX` | `https://pubmed.ncbi.nlm.nih.gov/XXXXXXXX/` |
| `nct:NCTXXXXXXXX` | `https://clinicaltrials.gov/study/NCTXXXXXXXX` |
| anything else | rendered as plain text, no link |

### CSS spinner: pure CSS keyframe

No animation library. A `@keyframes` rotating border spinner is sufficient and adds no
dependency.

### Error display

On a non-2xx response, the UI reads `response.json().detail` if present, otherwise falls back
to `"Something went wrong. Please try again."`. The error is shown in a `.error` div above the
form results area.

### Playwright for E2E validation

Playwright is the most reliable way to validate that the full user journey works — from input
to rendered brief with clickable links. It is installed as a dev dependency in `ui/`. Only
Chromium is installed to keep setup lean.

---

## Context

This phase corresponds to **Phase 7** in `specs/roadmap.md`. It is the final phase. After this
the system is fully functional across both its delivery surfaces (API and UI).
