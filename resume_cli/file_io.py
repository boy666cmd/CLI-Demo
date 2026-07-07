from pathlib import Path

from resume_cli.exceptions import EmptyFileError, ResumeFileNotFoundError


def read_text_file(file_path: Path) -> str:
    """Read a text file and validate it is not empty."""
    path = Path(file_path)
    if not path.exists():
        raise ResumeFileNotFoundError(f"文件不存在: {path}")

    try:
        content = path.read_text(encoding="utf-8").strip()
    except UnicodeDecodeError:
        content = path.read_text(encoding="gbk").strip()

    if not content:
        raise EmptyFileError(f"文件内容为空: {path}")

    return content


def write_output(file_path: Path, content: str) -> None:
    """Write content to an output file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
