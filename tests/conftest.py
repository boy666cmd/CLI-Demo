import pytest

from resume_cli.schemas.extract import ExtractResult
from resume_cli.schemas.score import ScoreResult


@pytest.fixture
def sample_extract_data():
    return {
        "name": "张三",
        "phone": "13800138000",
        "email": "zhangsan@example.com",
        "city": "北京",
        "education": [
            {
                "school": "清华大学",
                "major": "计算机",
                "degree": "本科",
                "graduation_time": "2020-06",
            }
        ],
        "skills": ["Python", "JavaScript"],
    }


@pytest.fixture
def sample_score_data():
    return {
        "overall_score": 82,
        "skill_score": 88,
        "experience_score": 80,
        "education_score": 75,
        "comment": "匹配度较好",
        "interview_questions": ["问题1", "问题2"],
    }
