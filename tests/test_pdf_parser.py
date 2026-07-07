import pytest

from resume_cli.exceptions import (
    EmptyPdfTextError,
    InvalidPdfError,
    ResumeFileNotFoundError,
)
from resume_cli.pdf_parser import extract_text


def _make_pdf_with_text(text: str, tmp_path) -> str:
    """Create a minimal PDF without extractable text."""
    from pypdf import PageObject, PdfWriter

    pdf_path = tmp_path / "resume.pdf"
    writer = PdfWriter()
    page = PageObject.create_blank_page(width=612, height=792)
    writer.add_page(page)
    writer.write(str(pdf_path))
    return str(pdf_path)


def test_extract_text_file_not_found(tmp_path):
    missing = tmp_path / "missing.pdf"
    with pytest.raises(ResumeFileNotFoundError, match="文件不存在"):
        extract_text(missing)


def test_extract_text_invalid_extension(tmp_path):
    txt_file = tmp_path / "resume.txt"
    txt_file.write_text("not a pdf", encoding="utf-8")
    with pytest.raises(InvalidPdfError, match="不是有效的 PDF"):
        extract_text(txt_file)


def test_extract_text_invalid_magic_bytes(tmp_path):
    fake_pdf = tmp_path / "fake.pdf"
    fake_pdf.write_bytes(b"NOTPDF content")
    with pytest.raises(InvalidPdfError, match="不是有效的 PDF"):
        extract_text(fake_pdf)


def test_extract_text_empty_pdf(tmp_path):
    pdf_path = _make_pdf_with_text("", tmp_path)
    with pytest.raises(EmptyPdfTextError, match="文本为空"):
        extract_text(pdf_path)


def test_extract_text_success(tmp_path):
    pdf_path = tmp_path / "valid.pdf"
    raw_pdf = b"""%PDF-1.4
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Contents 4 0 R/Resources<</Font<</F1 5 0 R>>>>>>endobj
4 0 obj<</Length 44>>stream
BT /F1 12 Tf 100 700 Td (Hello Resume) Tj ET
endstream
endobj
5 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000052 00000 n 
0000000101 00000 n 
0000000228 00000 n 
0000000320 00000 n 
trailer<</Size 6/Root 1 0 R>>
startxref
400
%%EOF"""
    pdf_path.write_bytes(raw_pdf)
    result = extract_text(pdf_path)
    assert "Hello Resume" in result or "Hello" in result
