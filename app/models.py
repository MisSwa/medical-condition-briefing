from pydantic import BaseModel


class BriefRequest(BaseModel):
    condition: str


class BriefResponse(BaseModel):
    condition: str
    standard_of_care: list[str]
    emerging_treatments: list[str]
    key_organizations: list[str]
    sources: list[str]
