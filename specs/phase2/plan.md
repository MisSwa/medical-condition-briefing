# Phase 2 — PubMed Retrieval Node: Plan

Tasks are organized by layer. Complete each group before moving to the next.

---

## Group 1 — PubMed Client

1.1 Create `app/pubmed.py` with a single public function:
  `fetch_pubmed_articles(condition: str, max_results: int = 5) -> list[dict]`

1.2 Implement the **esearch step** inside that function:
  - Call `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`
  - Parameters: `db=pubmed`, `term={condition} treatment`, `retmax={max_results}`, `reldate=1825`, `datetype=pdat`, `retmode=json`
  - Extract the `IdList` (list of PMIDs) from the JSON response

1.3 Early-exit if `IdList` is empty — return `[]` immediately rather than calling efetch with no IDs

1.4 Implement the **efetch step** inside that function:
  - Call `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi`
  - Parameters: `db=pubmed`, `id={comma-joined PMIDs}`, `retmode=xml`
  - Parse the returned XML with `xml.etree.ElementTree` (standard library, no new dependency)

1.5 For each `<PubmedArticle>` in the XML, extract:
  - `pmid` — from `MedlineCitation/PMID`
  - `title` — from `MedlineCitation/Article/ArticleTitle`
  - `abstract` — from `MedlineCitation/Article/Abstract/AbstractText`; join multiple `AbstractText` elements with a space if the abstract is structured

1.6 Return a `list[dict]` with one entry per article: `{"pmid": str, "title": str, "abstract": str}`

---

## Group 2 — Wire into LangGraph Node

2.1 Update `query_pubmed` in `app/nodes.py`:
  - Import `fetch_pubmed_articles` from `app.pubmed`
  - Call it with `state["condition"]`
  - Return `{"pubmed_results": results}` as a partial state update

2.2 Confirm the existing tests still pass (the stub endpoint is unchanged)

---

## Group 3 — Tests

3.1 Create `tests/test_pubmed.py` with a live integration test:
  - Call `query_pubmed` with a state dict containing `condition = "asthma"`
  - Assert the return value has key `pubmed_results`
  - Assert `pubmed_results` is a non-empty list
  - Assert each item has keys `pmid`, `title`, `abstract`
  - Assert each `pmid` is a non-empty string

3.2 Run the full test suite (`pytest -v`) and confirm all tests pass
