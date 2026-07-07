from pydantic import BaseModel, Field, field_validator


class ScoreResult(BaseModel):
    overall_score: int = Field(ge=0, le=100)
    skill_score: int = Field(ge=0, le=100)
    experience_score: int = Field(ge=0, le=100)
    education_score: int = Field(ge=0, le=100)
    comment: str
    interview_questions: list[str]

    @field_validator("comment")
    @classmethod
    def comment_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("comment must not be empty")
        return value

    @field_validator("interview_questions")
    @classmethod
    def questions_not_empty(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("interview_questions must contain at least one item")
        return value
