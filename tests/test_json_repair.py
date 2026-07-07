import pytest
from pydantic import ValidationError

from resume_cli.ai.json_repair import parse_json_response
from resume_cli.exceptions import JsonParseError
from resume_cli.schemas.extract import ExtractResult
from resume_cli.schemas.score import ScoreResult


def test_parse_json_normal():
    raw = '{"name": "张三", "skills": ["Python"]}'
    result = parse_json_response(raw)
    assert result["name"] == "张三"


def test_parse_json_with_markdown_fence():
    raw = '```json\n{"name": "李四", "skills": []}\n```'
    result = parse_json_response(raw)
    assert result["name"] == "李四"


def test_parse_json_with_trailing_comma():
    raw = '{"name": "王五", "skills": ["Go",],}'
    result = parse_json_response(raw)
    assert result["name"] == "王五"
    assert result["skills"] == ["Go"]


def test_parse_json_invalid():
    with pytest.raises(JsonParseError):
        parse_json_response("not json at all")


def test_extract_result_valid():
    data = {
        "name": "张三",
        "phone": "13800138000",
        "email": "test@example.com",
        "city": "北京",
        "education": [{"school": "清华大学", "major": "CS", "degree": "本科", "graduation_time": "2020"}],
        "skills": ["Python"],
    }
    result = ExtractResult.model_validate(data)
    assert result.name == "张三"
    assert len(result.education) == 1


def test_score_result_valid():
    data = {
        "overall_score": 82,
        "skill_score": 88,
        "experience_score": 80,
        "education_score": 75,
        "comment": "匹配度较好",
        "interview_questions": ["问题1"],
    }
    result = ScoreResult.model_validate(data)
    assert result.overall_score == 82


def test_score_result_invalid_score():
    data = {
        "overall_score": 150,
        "skill_score": 88,
        "experience_score": 80,
        "education_score": 75,
        "comment": "匹配度较好",
        "interview_questions": ["问题1"],
    }
    with pytest.raises(ValidationError):
        ScoreResult.model_validate(data)


def test_score_result_empty_comment():
    data = {
        "overall_score": 82,
        "skill_score": 88,
        "experience_score": 80,
        "education_score": 75,
        "comment": "   ",
        "interview_questions": ["问题1"],
    }
    with pytest.raises(ValidationError):
        ScoreResult.model_validate(data)
