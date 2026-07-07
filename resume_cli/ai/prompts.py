PROMPT_TYPE_EXTRACT = "extract"
PROMPT_TYPE_SCORE = "score"


def build_extract_prompt(resume_text: str) -> str:
    return f"""你是一名专业的简历解析助手。请从以下简历文本中提取结构化信息。

要求：
1. 仅返回 JSON，不要包含任何其他文字或 markdown 代码块
2. 缺失的字段使用 null（字符串字段）或 []（列表字段）
3. education 为数组，每项包含 school、major、degree、graduation_time
4. skills 为字符串数组

返回 JSON 格式：
{{
  "name": "姓名",
  "phone": "电话",
  "email": "邮箱",
  "city": "所在城市",
  "education": [
    {{
      "school": "学校",
      "major": "专业",
      "degree": "学历",
      "graduation_time": "毕业时间"
    }}
  ],
  "skills": ["技能1", "技能2"]
}}

简历文本：
{resume_text}
"""


def build_score_prompt(resume_text: str, jd_text: str) -> str:
    return f"""你是一名专业的招聘顾问。请根据岗位描述（JD）对候选人简历进行匹配评分。

要求：
1. 仅返回 JSON，不要包含任何其他文字或 markdown 代码块
2. overall_score、skill_score、experience_score、education_score 均为 0-100 的整数
3. comment 为简要匹配理由（1-2 句话）
4. interview_questions 为 2-3 个面试问题

返回 JSON 格式：
{{
  "overall_score": 82,
  "skill_score": 88,
  "experience_score": 80,
  "education_score": 75,
  "comment": "简要匹配理由",
  "interview_questions": ["问题1", "问题2"]
}}

岗位描述（JD）：
{jd_text}

候选人简历：
{resume_text}
"""
