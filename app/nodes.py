import logging
import threading
from typing import Callable

from app.clinicaltrials import fetch_clinical_trials
from app.models import BriefResponse
from app.pubmed import fetch_pubmed_articles
from app.state import BriefingState
from app.synthesize import synthesize_medical_brief

logger = logging.getLogger(__name__)


def _fetch_with_retry(fetch_fn: Callable, *args) -> list:
    """Call fetch_fn(*args), retrying once on failure. Returns [] if both attempts fail."""
    try:
        return fetch_fn(*args)
    except Exception as exc:
        logger.warning("%s failed (%s), retrying once...", fetch_fn.__name__, exc)
    try:
        return fetch_fn(*args)
    except Exception as exc:
        logger.warning("%s retry also failed (%s), returning empty list", fetch_fn.__name__, exc)
        return []


def query_pubmed(state: BriefingState) -> dict:
    """Retrieve peer-reviewed literature from PubMed for the given condition."""
    logger.info("query_pubmed start  thread=%s", threading.get_ident())
    results = _fetch_with_retry(fetch_pubmed_articles, state["condition"])
    logger.info("query_pubmed done   thread=%s", threading.get_ident())
    return {"pubmed_results": results}


def query_clinicaltrials(state: BriefingState) -> dict:
    """Retrieve active Phase 2–4 clinical trials from ClinicalTrials.gov for the given condition."""
    logger.info("query_clinicaltrials start  thread=%s", threading.get_ident())
    results = _fetch_with_retry(fetch_clinical_trials, state["condition"])
    logger.info("query_clinicaltrials done   thread=%s", threading.get_ident())
    return {"trial_results": results}


def synthesize_brief(state: BriefingState) -> dict:
    """Call Claude to synthesise the retrieved data into the three brief sections."""
    result = synthesize_medical_brief(
        state["condition"],
        state["pubmed_results"],
        state["trial_results"],
    )
    return {"brief": result}


def format_output(state: BriefingState) -> dict:
    """Attach condition, validate with Pydantic, and store the final brief in state."""
    full = {**state["brief"], "condition": state["condition"]}
    validated = BriefResponse(**full)
    return {"brief": validated.model_dump()}
