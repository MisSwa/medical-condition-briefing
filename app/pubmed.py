import xml.etree.ElementTree as ET
from datetime import datetime

import httpx

_ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
_EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
_MAX_RESULTS = 5
_RECENCY_DAYS = 1825  # 5 years


def fetch_pubmed_articles(condition: str, max_results: int = _MAX_RESULTS) -> list[dict]:
    """
    Search PubMed for articles about `condition` published in the last 5 years.
    Returns up to `max_results` articles, each with pmid, title, and abstract.
    """
    pmids = _esearch(condition, max_results)
    if not pmids:
        return []
    return _efetch(pmids)


def _esearch(condition: str, max_results: int) -> list[str]:
    """Call esearch to get PMIDs matching the condition."""
    params = {
        "db": "pubmed",
        "term": f"{condition} treatment",
        "retmax": max_results,
        "reldate": _RECENCY_DAYS,
        "datetype": "pdat",
        "retmode": "json",
    }
    response = httpx.get(_ESEARCH_URL, params=params, timeout=15)
    response.raise_for_status()
    return response.json()["esearchresult"]["idlist"]


def _efetch(pmids: list[str]) -> list[dict]:
    """Call efetch to retrieve full article records for the given PMIDs."""
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
    }
    response = httpx.get(_EFETCH_URL, params=params, timeout=15)
    response.raise_for_status()
    return _parse_articles(response.text)


def _parse_articles(xml_text: str) -> list[dict]:
    """Parse PubMed XML into a list of article dicts."""
    root = ET.fromstring(xml_text)
    articles = []
    for article in root.findall("PubmedArticle"):
        citation = article.find("MedlineCitation")
        if citation is None:
            continue

        pmid_el = citation.find("PMID")
        pmid = pmid_el.text.strip() if pmid_el is not None and pmid_el.text else ""

        art = citation.find("Article")
        if art is None:
            continue

        title_el = art.find("ArticleTitle")
        title = title_el.text or "" if title_el is not None else ""

        abstract_el = art.find("Abstract")
        abstract = ""
        if abstract_el is not None:
            parts = [el.text or "" for el in abstract_el.findall("AbstractText")]
            abstract = " ".join(p.strip() for p in parts if p.strip())

        if pmid:
            articles.append({"pmid": pmid, "title": title.strip(), "abstract": abstract})

    return articles
