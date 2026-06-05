from app.state import BriefingState


def query_pubmed(state: BriefingState) -> dict:
    """Retrieve literature from PubMed. Stub — implemented in Phase 2."""
    return {}


def query_clinicaltrials(state: BriefingState) -> dict:
    """Retrieve trial data from ClinicalTrials.gov. Stub — implemented in Phase 3."""
    return {}


def synthesize_brief(state: BriefingState) -> dict:
    """Synthesize retrieved data into a structured brief using Claude. Stub — implemented in Phase 5."""
    return {}


def format_output(state: BriefingState) -> dict:
    """Validate and structure the final brief. Stub — implemented in Phase 5."""
    return {}
