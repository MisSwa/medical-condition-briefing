# Phase 5 — Claude Synthesis Node: Requirements

## Scope

Phase 5 replaces both stub synthesis nodes with real implementations. `synthesize_brief` calls
Claude to produce the three brief sections. `format_output` validates the result with Pydantic
and attaches the `condition` field. After this phase the full graph is end-to-end functional.

---

## What is in scope

- `app/synthesize.py` — new module containing the Claude synthesis logic
- `app/nodes.py` — `synthesize_brief` and `format_output` updated to real implementations
- `tests/test_synthesis.py` — end-to-end integration test with a real Claude API call

## What is out of scope for this phase

- Wiring the graph output into the FastAPI endpoint (Phase 6)
- Any changes to the retrieval nodes or graph topology
- Prompt tuning beyond the initial working version
- Streaming responses

---

## Decisions

### Structured output via tool use

Claude is called with a single tool (`create_medical_brief`) and `tool_choice` forced to that
tool. This guarantees the response matches the schema exactly — no parsing, no fallbacks, no
hallucinated field names. The tool `input_schema` is the authoritative shape of the brief output.

### Model: claude-sonnet-4-5

Accuracy is the primary success measure (per `specs/mission.md`). Sonnet-class models offer
the best accuracy/latency balance for medical synthesis. Haiku is not used here.

### ANTHROPIC_API_KEY required

The Anthropic client reads `ANTHROPIC_API_KEY` from the environment automatically. The key must
be set before running the application or tests. No `.env` loading is added — that is the
operator's responsibility.

### Brief tool schema

The tool produces four fields (condition is added by `format_output`):

```json
{
  "standard_of_care":   ["string"],
  "emerging_treatments": ["string"],
  "key_organizations":   ["string"],
  "sources":             ["pmid:XXXXXXXX", "nct:NCTXXXXXXXX"]
}
```

Each string in `standard_of_care` and `emerging_treatments` is a single self-contained
statement. Each `key_organizations` entry is a named organisation. Sources must use the prefixed
format so they can be rendered as links in the React UI (Phase 7).

### Context format

Claude receives the retrieved evidence structured as:

```
You are a medical research analyst...

## Retrieved Literature (PubMed)
1. [Title] — pmid:XXXXXXXX
   [Abstract]

## Clinical Trials (ClinicalTrials.gov)
1. [Title] — nct:NCTXXXXXXXX
   Status: ... | Sponsor: ...
```

If either source returns no results (e.g., due to an API failure handled in Phase 4), the
corresponding section is omitted from the context. Claude synthesises from whatever is available.

### format_output responsibility

`format_output` is the single point where `condition` is attached and Pydantic validation runs.
If `synthesize_brief` returns a malformed dict (tool use guarantees this won't happen in
practice), `format_output` raises a `ValidationError` which surfaces as a 500 from the API.

### BriefingState.brief field

After `format_output`, `state["brief"]` contains the full validated `BriefResponse.model_dump()`
dict. This is what Phase 6 will read to build the API response.

---

## Context

This phase corresponds to **Phase 5** in `specs/roadmap.md`. After this phase the full pipeline
(retrieval → synthesis → validation) is working. Phase 6 wires it into the REST API.
