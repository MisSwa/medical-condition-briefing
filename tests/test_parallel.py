import threading
import time

import app.nodes as nodes_module
from app.graph import briefing_graph
from app.state import BriefingState

_FAKE_BRIEF = {
    "standard_of_care": ["Inhaled corticosteroids"],
    "emerging_treatments": ["Biologic therapy"],
    "key_organizations": ["WHO"],
    "sources": ["pmid:00000001"],
}

_INITIAL_STATE: BriefingState = {
    "condition": "asthma",
    "pubmed_results": [],
    "trial_results": [],
    "brief": {},
}

_FAKE_ARTICLES = [{"pmid": "00000001", "title": "Fake article", "abstract": "Fake abstract"}]
_FAKE_TRIALS = [{"nct_id": "NCT00000001", "title": "Fake trial", "status": "RECRUITING", "sponsor": "Fake Sponsor"}]


def test_parallel_thread_ids_differ(monkeypatch):
    """Both retrieval nodes must run on different threads — proving concurrent execution."""
    recorded: dict[str, int] = {}

    def fake_pubmed(condition):
        time.sleep(0.05)  # small pause so threads overlap and can't be reused
        recorded["pubmed"] = threading.get_ident()
        return _FAKE_ARTICLES

    def fake_clinicaltrials(condition):
        time.sleep(0.05)
        recorded["clinicaltrials"] = threading.get_ident()
        return _FAKE_TRIALS

    # Patch the names as imported into nodes.py, not the source module
    monkeypatch.setattr(nodes_module, "fetch_pubmed_articles", fake_pubmed)
    monkeypatch.setattr(nodes_module, "fetch_clinical_trials", fake_clinicaltrials)
    monkeypatch.setattr(nodes_module, "synthesize_medical_brief", lambda *_: _FAKE_BRIEF)

    briefing_graph.invoke(_INITIAL_STATE)

    assert "pubmed" in recorded, "query_pubmed node did not run"
    assert "clinicaltrials" in recorded, "query_clinicaltrials node did not run"
    assert recorded["pubmed"] != recorded["clinicaltrials"], (
        f"Both nodes ran on the same thread ({recorded['pubmed']}); expected different threads"
    )


def test_clinicaltrials_failure_does_not_block_pubmed(monkeypatch):
    """A ClinicalTrials failure must not prevent PubMed results from flowing into state."""

    def raise_error(condition):
        raise RuntimeError("Simulated ClinicalTrials.gov outage")

    monkeypatch.setattr(nodes_module, "fetch_pubmed_articles", lambda _: _FAKE_ARTICLES)
    monkeypatch.setattr(nodes_module, "fetch_clinical_trials", raise_error)
    monkeypatch.setattr(nodes_module, "synthesize_medical_brief", lambda *_: _FAKE_BRIEF)

    result = briefing_graph.invoke(_INITIAL_STATE)

    assert result["pubmed_results"] == _FAKE_ARTICLES, "PubMed results should be present when CT.gov fails"
    assert result["trial_results"] == [], "trial_results should be empty when CT.gov fails"
