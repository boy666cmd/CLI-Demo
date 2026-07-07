from pathlib import Path

from pypdf import PdfReader
from pypdf.errors import PdfReadError as PyPdfReadError

from resume_cli.exceptions import (
    EmptyPdfTextError,
    InvalidPdfError,
    PdfReadError,
    ResumeFileNotFoundError,
)
from resume_cli.logging_config import setup_logging

logger = setup_logging()


def _validate_pdf_path(pdf_path: Path) -> None:
    if not pdf_path.exists():
        raise ResumeFileNotFoundError(f"文件不存在: {pdf_path}")

    if pdf_path.suffix.lower() != ".pdf":
        raise InvalidPdfError(f"文件不是有效的 PDF: {pdf_path}")

    with pdf_path.open("rb") as f:
        header = f.read(4)
    if header != b"%PDF":
        raise InvalidPdfError(f"文件不是有效的 PDF: {pdf_path}")


def extract_text(pdf_path: Path) -> str:
    """Extract text content from a local PDF file."""
    path = Path(pdf_path)
    _validate_pdf_path(path)

    try:
        reader = PdfReader(str(path))
        pages = reader.pages
        logger.info("Reading PDF with %d page(s)", len(pages))
        text_parts: list[str] = []
        for page in pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        text = "\n".join(text_parts).strip()
    except PyPdfReadError as exc:
        raise PdfReadError(f"PDF 无法读取: {exc}") from exc
    except Exception as exc:
        raise PdfReadError(f"PDF 无法读取: {exc}") from exc

    if not text:
        raise EmptyPdfTextError("PDF 文本为空，可能是扫描件或图片 PDF")

    logger.info("Extracted %d characters from PDF", len(text))
    return text
