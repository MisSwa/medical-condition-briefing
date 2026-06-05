# Phase 2 — PubMed Retrieval Node: Requirements

## Scope

Phase 2 replaces the no-op `query_pubmed` LangGraph node with a real implementation that fetches peer-reviewed literature from PubMed via NCBI E-utilities. All other nodes and endpoints remain unchanged from Phase 1.

---

## What is in scope

- `app/pubmed.py` — new module containing the PubMed fetch logic
- `app/nodes.py` — `query_pubmed` function updated to call the real client
- `tests/test_pubmed.py` — live integration test for the node

## What is out of scope for this phase

- ClinicalTrials.gov retrieval (Phase 3)
- Claude synthesis (Phase 5)
- Any changes to the FastAPI endpoints or response shape
- Changes to any other LangGraph node
- Caching or deduplication of PubMed results

---

## Decisions

### API: NCBI E-utilities (no key required)

Use the public NCBI E-utilities REST API. No API key is needed. The unauthenticated rate limit is ~3 requests/second; since each call to `query_pubmed` makes exactly 2 HTTP requests (esearch + efetch), no rate-limiting logic is required in Phase 2.

Base URL: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`

### Result limit: 5, filtered to last 5 years

Fetch a maximum of 5 articles per condition. Filter to the last 5 years using `reldate=1825&datetype=pdat` on the esearch call. This prioritises recency and keeps the payload small for the synthesis step.

### Search term construction

The esearch `term` parameter is constructed as `{condition} treatment` to bias results toward treatment-relevant literature. This is intentionally simple; search term tuning is out of scope for Phase 2.

### Fields to extract: PMID, title, abstract

Each article is stored as:
```python
{
    "pmid": str,      # e.g. "38123456"
    "title": str,     # full article title
    "abstract": str,  # full abstract text; structured abstracts are joined with a space
}
```

### XML parsing with standard library

efetch returns XML. Parse with `xml.etree.ElementTree` (Python standard library). No additional dependency required.

### State field: `pubmed_results`

Results are stored in `BriefingState["pubmed_results"]`. This field was defined in Phase 1 and its type (`list[dict[str, Any]]`) remains unchanged.

### HTTP client: httpx (already a dependency)

Use `httpx` (synchronous client) for all HTTP calls. It is already pinned in `requirements.txt`.

---

## Context

This phase corresponds to **Phase 2** in `specs/roadmap.md`. The `query_pubmed` node name and its position in the graph topology are locked — only the implementation changes. The graph structure defined in `app/graph.py` is not touched.
