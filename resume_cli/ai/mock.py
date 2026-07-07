import json

from resume_cli.ai.prompts import PROMPT_TYPE_EXTRACT, PROMPT_TYPE_SCORE

MOCK_EXTRACT_RESPONSE = {
    "name": "张三",
    "phone": "13800138000",
    "email": "zhangsan@example.com",
    "city": "北京",
    "education": [
        {
            "school": "清华大学",
            "major": "计算机科学与技术",
            "degree": "本科",
            "graduation_time": "2020-06",
        }
    ],
    "skills": ["Python", "JavaScript", "React", "FastAPI", "MySQL"],
}

MOCK_SCORE_RESPONSE = {
    "overall_score": 82,
    "skill_score": 88,
    "experience_score": 80,
    "education_score": 75,
    "comment": "候选人具备较好的全栈开发基础，技能与岗位要求较匹配，但缺少明确的大模型应用经验。",
    "interview_questions": [
        "请介绍一个你主导过的全栈项目。",
        "你是否有调用大模型 API 的实际经验？",
    ],
}


def mock_response_for(prompt_type: str) -> str:
    if prompt_type == PROMPT_TYPE_EXTRACT:
        return json.dumps(MOCK_EXTRACT_RESPONSE, ensure_ascii=False)
    if prompt_type == PROMPT_TYPE_SCORE:
        return json.dumps(MOCK_SCORE_RESPONSE, ensure_ascii=False)
    return json.dumps(MOCK_EXTRACT_RESPONSE, ensure_ascii=False)
