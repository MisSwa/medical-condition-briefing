import json
import urllib.parse
import urllib.request

_BASE_URL = "https://clinicaltrials.gov/api/v2/studies"
_MAX_RESULTS = 5
# Pipe-separated — ClinicalTrials.gov API v2 does not accept comma-separated values
_STATUSES = "RECRUITING|ACTIVE_NOT_RECRUITING"
# filter.phase is not a supported v2 API parameter; phase filtering is done in post-processing
_VALID_PHASES = {"PHASE2", "PHASE3", "PHASE4"}
# Request extra results so post-phase-filtering still yields up to _MAX_RESULTS
_FETCH_MULTIPLIER = 4
# urllib is used instead of httpx — ClinicalTrials.gov blocks httpx's TLS fingerprint
_HEADERS = {"User-Agent": "MedicalBriefingSystem/1.0", "Accept": "application/json"}


def fetch_clinical_trials(condition: str, max_results: int = _MAX_RESULTS) -> list[dict]:
    """
    Search ClinicalTrials.gov for active Phase 2–4 trials matching `condition`.
    Returns up to `max_results` trials, each with nct_id, title, status, and sponsor.
    """
    data = _fetch(condition, max_results * _FETCH_MULTIPLIER)
    trials = _parse_trials(data)
    return trials[:max_results]


def _fetch(condition: str, page_size: int) -> dict:
    """Call the ClinicalTrials.gov API v2 and return the parsed JSON response."""
    params = urllib.parse.urlencode({
        "query.cond": condition,
        "filter.overallStatus": _STATUSES,
        "pageSize": page_size,
    })
    url = f"{_BASE_URL}?{params}"
    req = urllib.request.Request(url, headers=_HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def _parse_trials(data: dict) -> list[dict]:
    """
    Parse the ClinicalTrials.gov JSON response into a list of trial dicts.
    Post-filters to Phase 2, 3, and 4 trials only (API v2 has no phase filter parameter).
    Skips records with missing or malformed fields.
    """
    trials = []
    for study in data.get("studies", []):
        protocol = study.get("protocolSection", {})

        identification = protocol.get("identificationModule", {})
        nct_id = identification.get("nctId", "")
        title = identification.get("briefTitle", "")

        status = protocol.get("statusModule", {}).get("overallStatus", "")

        sponsor_module = protocol.get("sponsorCollaboratorsModule", {})
        sponsor = sponsor_module.get("leadSponsor", {}).get("name", "")

        phases = protocol.get("designModule", {}).get("phases", [])
        if not any(p in _VALID_PHASES for p in phases):
            continue

        if nct_id:
            trials.append({
                "nct_id": nct_id,
                "title": title,
                "status": status,
                "sponsor": sponsor,
            })

    return trials
