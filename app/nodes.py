from app.clinicaltrials import fetch_clinical_trials
from app.pubmed import fetch_pubmed_articles
from app.state import BriefingState


def query_pubmed(state: BriefingState) -> dict:
    """Retrieve peer-reviewed literature from PubMed for the given condition."""
    results = fetch_pubmed_articles(state["condition"])
    return {"pubmed_results": results}


def query_clinicaltrials(state: BriefingState) -> dict:
    """Retrieve active Phase 2–4 clinical trials from ClinicalTrials.gov for the given condition."""
    results = fetch_clinical_trials(state["condition"])
    return {"trial_results": results}


def synthesize_brief(state: BriefingState) -> dict:
    """Synthesize retrieved data into a structured brief using Claude. Stub — implemented in Phase 5."""
    return {}


def format_output(state: BriefingState) -> dict:
    """Validate and structure the final brief. Stub — implemented in Phase 5."""
    return {}
