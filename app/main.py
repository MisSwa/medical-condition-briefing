from fastapi import FastAPI

from app.graph import briefing_graph  # noqa: F401 — imported to catch startup errors
from app.models import BriefRequest, BriefResponse

app = FastAPI(title="Medical Condition Briefing System")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/brief", response_model=BriefResponse)
def create_brief(request: BriefRequest) -> BriefResponse:
    return BriefResponse(
        condition=request.condition,
        standard_of_care=["Stub: standard of care placeholder"],
        emerging_treatments=["Stub: emerging treatment placeholder"],
        key_organizations=["Stub: key organization placeholder"],
        sources=["Stub: source placeholder"],
    )
