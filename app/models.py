from pydantic import BaseModel, field_validator


class BriefRequest(BaseModel):
    condition: str

    @field_validator("condition")
    @classmethod
    def condition_must_not_be_empty(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("condition must not be empty or whitespace")
        return stripped


class BriefResponse(BaseModel):
    condition: str
    standard_of_care: list[str]
    emerging_treatments: list[str]
    key_organizations: list[str]
    sources: list[str]
