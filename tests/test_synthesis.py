import os

import pytest

from app.graph import briefing_graph
from app.state import BriefingState

_TEST_STATE: BriefingState = {
    "condition": "type 2 diabetes",
    "pubmed_results": [],
    "trial_results": [],
    "brief": {},
}

_REQUIRED_KEYS = {"condition", "standard_of_care", "emerging_treatments", "key_organizations", "sources"}


@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)
def test_full_graph_produces_brief():
    result = briefing_graph.invoke(_TEST_STATE)

    brief = result.get("brief", {})
    assert brief, "brief must be a non-empty dict"

    missing = _REQUIRED_KEYS - brief.keys()
    assert not missing, f"brief is missing keys: {missing}"

    assert brief["condition"] == "type 2 diabetes"

    for field in ("standard_of_care", "emerging_treatments", "key_organizations", "sources"):
        assert isinstance(brief[field], list), f"{field} must be a list"
        assert len(brief[field]) > 0, f"{field} must not be empty"

    sources = brief["sources"]
    prefixed = [s for s in sources if s.startswith("pmid:") or s.startswith("nct:")]
    assert prefixed, f"At least one source must use 'pmid:' or 'nct:' prefix. Got: {sources}"
