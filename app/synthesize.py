import anthropic

_MODEL = "claude-sonnet-4-5"
_MAX_TOKENS = 2048
_TOOL_NAME = "create_medical_brief"

_BRIEF_TOOL = {
    "name": _TOOL_NAME,
    "description": (
        "Create a structured medical condition brief with three evidence-based sections "
        "and traceable source citations."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "standard_of_care": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "Current first-line and guideline-endorsed treatments. "
                    "Each item is one self-contained statement."
                ),
            },
            "emerging_treatments": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "Therapies currently in clinical trials or late-stage development. "
                    "Each item is one self-contained statement."
                ),
            },
            "key_organizations": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "Pharma companies, research institutions, and hospitals driving progress. "
                    "Each item is a named organisation only."
                ),
            },
            "sources": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "Source citations from the retrieved evidence. "
                    "Use format 'pmid:XXXXXXXX' for PubMed articles "
                    "and 'nct:NCTXXXXXXXX' for clinical trials."
                ),
            },
        },
        "required": ["standard_of_care", "emerging_treatments", "key_organizations", "sources"],
    },
}


def synthesize_medical_brief(
    condition: str,
    pubmed_results: list[dict],
    trial_results: list[dict],
) -> dict:
    """
    Call Claude with forced tool use to synthesise a structured medical brief.
    Returns the tool input dict with keys:
    standard_of_care, emerging_treatments, key_organizations, sources.
    """
    context = _build_context(condition, pubmed_results, trial_results)
    client = anthropic.Anthropic()

    response = client.messages.create(
        model=_MODEL,
        max_tokens=_MAX_TOKENS,
        tools=[_BRIEF_TOOL],
        tool_choice={"type": "tool", "name": _TOOL_NAME},
        messages=[{"role": "user", "content": context}],
    )

    for block in response.content:
        if block.type == "tool_use" and block.name == _TOOL_NAME:
            return block.input

    raise ValueError("Claude did not return the expected tool use block")


def _build_context(
    condition: str,
    pubmed_results: list[dict],
    trial_results: list[dict],
) -> str:
    """Format retrieved evidence into a prompt context for Claude."""
    lines = [
        f"You are a medical research analyst. Generate a structured brief for: {condition}",
        "",
        "Base your response primarily on the retrieved evidence below. "
        "Cite every claim using the provided source identifiers.",
        "",
    ]

    if pubmed_results:
        lines.append("## Retrieved Literature (PubMed)")
        for i, article in enumerate(pubmed_results, 1):
            lines.append(f"{i}. {article.get('title', '').strip()} — pmid:{article.get('pmid', '')}")
            abstract = article.get("abstract", "").strip()
            if abstract:
                lines.append(f"   {abstract}")
        lines.append("")

    if trial_results:
        lines.append("## Clinical Trials (ClinicalTrials.gov)")
        for i, trial in enumerate(trial_results, 1):
            lines.append(
                f"{i}. {trial.get('title', '').strip()} — nct:{trial.get('nct_id', '')}"
            )
            lines.append(
                f"   Status: {trial.get('status', '')} | Sponsor: {trial.get('sponsor', '')}"
            )
        lines.append("")

    return "\n".join(lines)
