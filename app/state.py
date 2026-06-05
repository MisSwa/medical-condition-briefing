from typing import Any, TypedDict


class BriefingState(TypedDict):
    condition: str
    pubmed_results: list[dict[str, Any]]
    trial_results: list[dict[str, Any]]
    brief: dict[str, Any]
