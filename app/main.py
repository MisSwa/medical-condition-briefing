from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.graph import briefing_graph
from app.models import BriefRequest, BriefResponse
from app.state import BriefingState

app = FastAPI(title="Medical Condition Briefing System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/brief", response_model=BriefResponse)
def create_brief(request: BriefRequest) -> BriefResponse:
    initial_state: BriefingState = {
        "condition": request.condition,
        "pubmed_results": [],
        "trial_results": [],
        "brief": {},
    }
    try:
        state = briefing_graph.invoke(initial_state)
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Brief generation failed: {exc}",
        )
    return BriefResponse(**state["brief"])
