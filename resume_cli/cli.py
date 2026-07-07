from pathlib import Path
import sys
from typing import Optional

import typer

if sys.platform == "win32":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

from resume_cli.exceptions import ResumeCliError
from resume_cli.logging_config import setup_logging
from resume_cli.output import emit_json, emit_text
from resume_cli.pdf_parser import extract_text
from resume_cli.services.extract_service import extract_resume
from resume_cli.services.score_service import score_resume

app = typer.Typer(
    name="resume-cli",
    help="AI 简历解析 CLI 工具 — 支持 PDF 解析、结构化提取与 JD 匹配评分",
    no_args_is_help=True,
)
logger = setup_logging()


def _handle_error(exc: ResumeCliError) -> None:
    typer.secho(f"Error: {exc}", fg=typer.colors.RED, err=True)
    raise typer.Exit(code=1)


@app.command("parse")
def parse_command(
    pdf_path: Path = typer.Argument(..., help="PDF 简历文件路径", exists=False),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="将结果保存到文件"
    ),
    mock: bool = typer.Option(False, "--mock", help="使用 mock 模式（parse 命令忽略此选项）"),
) -> None:
    """读取 PDF 简历并提取文本内容。"""
    try:
        text = extract_text(pdf_path)
        emit_text(text, str(output) if output else None)
    except ResumeCliError as exc:
        _handle_error(exc)


@app.command("extract")
def extract_command(
    pdf_path: Path = typer.Argument(..., help="PDF 简历文件路径", exists=False),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="将结果保存为 JSON 文件"
    ),
    mock: bool = typer.Option(False, "--mock", help="使用 mock AI 响应，无需 API Key"),
) -> None:
    """从简历中提取结构化信息（姓名、联系方式、教育、技能等）。"""
    try:
        result = extract_resume(pdf_path, mock=mock)
        emit_json(result.model_dump(), str(output) if output else None)
    except ResumeCliError as exc:
        _handle_error(exc)


@app.command("score")
def score_command(
    pdf_path: Path = typer.Argument(..., help="PDF 简历文件路径", exists=False),
    jd: Path = typer.Option(..., "--jd", help="岗位描述文本文件路径"),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="将结果保存为 JSON 文件"
    ),
    mock: bool = typer.Option(False, "--mock", help="使用 mock AI 响应，无需 API Key"),
) -> None:
    """根据岗位描述对简历进行匹配评分。"""
    try:
        result = score_resume(pdf_path, jd, mock=mock)
        emit_json(result.model_dump(), str(output) if output else None)
    except ResumeCliError as exc:
        _handle_error(exc)


if __name__ == "__main__":
    app()


def main() -> None:
    app()
