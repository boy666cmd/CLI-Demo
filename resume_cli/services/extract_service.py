from pathlib import Path

from pydantic import ValidationError as PydanticValidationError

from resume_cli.ai.client import call_ai
from resume_cli.ai.json_repair import parse_json_response
from resume_cli.ai.prompts import PROMPT_TYPE_EXTRACT, build_extract_prompt
from resume_cli.exceptions import ValidationError
from resume_cli.logging_config import setup_logging
from resume_cli.pdf_parser import extract_text
from resume_cli.schemas.extract import ExtractResult

logger = setup_logging()


def extract_resume(pdf_path: Path, *, mock: bool = False) -> ExtractResult:
    text = extract_text(pdf_path)
    prompt = build_extract_prompt(text)
    raw = call_ai(prompt, prompt_type=PROMPT_TYPE_EXTRACT, mock=mock)
    logger.info("Parsing and validating extract response")
    data = parse_json_response(raw)
    try:
        return ExtractResult.model_validate(data)
    except PydanticValidationError as exc:
        raise ValidationError(f"AI 返回格式不符合预期: {exc}") from exc
