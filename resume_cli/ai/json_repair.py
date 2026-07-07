import json
import re

from resume_cli.exceptions import JsonParseError


def _strip_markdown_fences(text: str) -> str:
    stripped = text.strip()
    pattern = r"^```(?:json)?\s*\n?(.*?)\n?```$"
    match = re.match(pattern, stripped, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return stripped


def _extract_json_object(text: str) -> str:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise JsonParseError("AI 返回内容中未找到有效的 JSON 对象")
    return text[start : end + 1]


def _remove_trailing_commas(text: str) -> str:
    return re.sub(r",\s*([}\]])", r"\1", text)


def parse_json_response(raw: str) -> dict:
    """Parse AI response text into a JSON dict, repairing common format issues."""
    candidates = [
        raw,
        _strip_markdown_fences(raw),
        _extract_json_object(_strip_markdown_fences(raw)),
    ]

    last_error: Exception | None = None
    for candidate in candidates:
        for text in (candidate, _remove_trailing_commas(candidate)):
            try:
                result = json.loads(text)
                if isinstance(result, dict):
                    return result
            except json.JSONDecodeError as exc:
                last_error = exc
                continue

    message = f"AI 返回内容无法解析为 JSON: {last_error}"
    raise JsonParseError(message)
