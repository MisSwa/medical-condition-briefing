from app.nodes import query_pubmed
from app.state import BriefingState

_TEST_STATE: BriefingState = {
    "condition": "asthma",
    "pubmed_results": [],
    "trial_results": [],
    "brief": {},
}


def test_query_pubmed_returns_articles():
    result = query_pubmed(_TEST_STATE)

    assert "pubmed_results" in result
    articles = result["pubmed_results"]

    assert isinstance(articles, list)
    assert len(articles) > 0, "Expected at least one article from PubMed"

    for article in articles:
        assert "pmid" in article, f"Missing 'pmid' in article: {article}"
        assert "title" in article, f"Missing 'title' in article: {article}"
        assert "abstract" in article, f"Missing 'abstract' in article: {article}"
        assert article["pmid"], f"Empty pmid in article: {article}"
        assert article["title"], f"Empty title in article: {article}"
