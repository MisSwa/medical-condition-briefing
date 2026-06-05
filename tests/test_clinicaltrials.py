from app.nodes import query_clinicaltrials
from app.state import BriefingState

_TEST_STATE: BriefingState = {
    "condition": "diabetes",
    "pubmed_results": [],
    "trial_results": [],
    "brief": {},
}

_VALID_STATUSES = {"RECRUITING", "ACTIVE_NOT_RECRUITING"}


def test_query_clinicaltrials_returns_trials():
    result = query_clinicaltrials(_TEST_STATE)

    assert "trial_results" in result
    trials = result["trial_results"]

    assert isinstance(trials, list)
    assert len(trials) > 0, "Expected at least one trial from ClinicalTrials.gov"

    for trial in trials:
        assert "nct_id" in trial, f"Missing 'nct_id' in trial: {trial}"
        assert "title" in trial, f"Missing 'title' in trial: {trial}"
        assert "status" in trial, f"Missing 'status' in trial: {trial}"
        assert "sponsor" in trial, f"Missing 'sponsor' in trial: {trial}"
        assert trial["nct_id"].startswith("NCT"), f"Invalid nct_id: {trial['nct_id']}"
        assert trial["status"] in _VALID_STATUSES, f"Unexpected status: {trial['status']}"
