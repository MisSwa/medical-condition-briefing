# Phase 5 — Claude Synthesis Node: Plan

Tasks are organized by layer. Complete each group before moving to the next.

---

## Group 1 — Claude Synthesis Client

1.1 Create `app/synthesize.py` with a single public function:
  `synthesize_medical_brief(condition, pubmed_results, trial_results) -> dict`

1.2 Define `_BRIEF_TOOL` — an Anthropic tool whose `input_schema` maps to the four output
  fields (standard_of_care, emerging_treatments, key_organizations, sources). Sources must
  use the format `"pmid:XXXXXXXX"` or `"nct:NCTXXXXXXXX"`.

1.3 Implement `_build_context(condition, pubmed_results, trial_results) -> str`:
  - Header: instruct Claude to act as a medical research analyst for the given condition
  - PubMed section: numbered list of title + abstract + `pmid:` citation
  - ClinicalTrials section: numbered list of title + status + sponsor + `nct:` citation
  - Footer: instruct Claude to base its response primarily on the retrieved evidence

1.4 Call `anthropic.Anthropic().messages.create()` with:
  - `model = "claude-sonnet-4-5"`
  - `max_tokens = 2048`
  - `tools = [_BRIEF_TOOL]`
  - `tool_choice = {"type": "tool", "name": "create_medical_brief"}` — forces structured output
  - `messages = [{"role": "user", "content": context}]`

1.5 Extract `block.input` from the tool use block in `response.content` and return it

---

## Group 2 — Wire Both Stub Nodes

2.1 Update `synthesize_brief` in `app/nodes.py`:
  - Import `synthesize_medical_brief` from `app.synthesize`
  - Call it with `state["condition"]`, `state["pubmed_results"]`, `state["trial_results"]`
  - Return `{"brief": result}`

2.2 Update `format_output` in `app/nodes.py`:
  - Import `BriefResponse` from `app.models`
  - Build the full brief dict by merging `state["brief"]` with `{"condition": state["condition"]}`
  - Validate with `BriefResponse(**full_brief)` — raises `ValidationError` if shape is wrong
  - Return `{"brief": validated.model_dump()}`

2.3 Confirm existing tests still pass (all 6)

---

## Group 3 — Tests

3.1 Create `tests/test_synthesis.py` with one end-to-end test:
  - Invoke `briefing_graph` with `condition = "type 2 diabetes"`
  - Assert `brief` is populated (non-empty dict)
  - Assert all five fields are present: `condition`, `standard_of_care`, `emerging_treatments`, `key_organizations`, `sources`
  - Assert each list field is non-empty
  - Assert at least one source follows `pmid:` or `nct:` format

3.2 Run the full test suite (`pytest -v`) and confirm all 7 tests pass

3.3 Manual quality review: run `python -m app.graph` and read the full brief output
  for "asthma" — verify sections are accurate, coherent, and grounded in the retrieved data
