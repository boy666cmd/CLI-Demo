import json
from typing import Any

from resume_cli.file_io import write_output
from resume_cli.logging_config import setup_logging

logger = setup_logging()


def format_json(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False)


def emit_text(text: str, output_path: str | None = None) -> None:
    print(text)
    if output_path:
        write_output(output_path, text)
        logger.info("Result written to %s", output_path)


def emit_json(data: Any, output_path: str | None = None) -> None:
    formatted = format_json(data)
    print(formatted)
    if output_path:
        write_output(output_path, formatted)
        logger.info("Result written to %s", output_path)
