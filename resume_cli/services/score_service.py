from pathlib import Path

from pydantic import ValidationError as PydanticValidationError

from resume_cli.ai.client import call_ai
from resume_cli.ai.json_repair import parse_json_response
from resume_cli.ai.prompts import PROMPT_TYPE_SCORE, build_score_prompt
from resume_cli.exceptions import ValidationError
from resume_cli.file_io import read_text_file
from resume_cli.logging_config import setup_logging
from resume_cli.pdf_parser import extract_text
from resume_cli.schemas.score import ScoreResult

logger = setup_logging()


def score_resume(pdf_path: Path, jd_path: Path, *, mock: bool = False) -> ScoreResult:
    resume_text = extract_text(pdf_path)
    jd_text = read_text_file(jd_path)
    prompt = build_score_prompt(resume_text, jd_text)
    raw = call_ai(prompt, prompt_type=PROMPT_TYPE_SCORE, mock=mock)
    logger.info("Parsing and validating score response")
    data = parse_json_response(raw)
    try:
        return ScoreResult.model_validate(data)
    except PydanticValidationError as exc:
        raise ValidationError(f"AI 返回格式不符合预期: {exc}") from exc
