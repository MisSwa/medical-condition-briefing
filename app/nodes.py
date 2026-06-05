from app.pubmed import fetch_pubmed_articles
from app.state import BriefingState


def query_pubmed(state: BriefingState) -> dict:
    """Retrieve peer-reviewed literature from PubMed for the given condition."""
    results = fetch_pubmed_articles(state["condition"])
    return {"pubmed_results": results}


def query_clinicaltrials(state: BriefingState) -> dict:
    """Retrieve trial data from ClinicalTrials.gov. Stub — implemented in Phase 3."""
    return {}


def synthesize_brief(state: BriefingState) -> dict:
    """Synthesize retrieved data into a structured brief using Claude. Stub — implemented in Phase 5."""
    return {}


def format_output(state: BriefingState) -> dict:
    """Validate and structure the final brief. Stub — implemented in Phase 5."""
    return {}
