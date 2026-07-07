from pydantic import BaseModel, Field


class EducationItem(BaseModel):
    school: str | None = None
    major: str | None = None
    degree: str | None = None
    graduation_time: str | None = None


class ExtractResult(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: str | None = None
    city: str | None = None
    education: list[EducationItem] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
