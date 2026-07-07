import pytest
from typer.testing import CliRunner

from resume_cli.cli import app

runner = CliRunner()


def _make_sample_pdf(tmp_path) -> str:
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
    pdf_path = tmp_path / "resume.pdf"
    pdf_path.write_bytes(raw_pdf)
    return str(pdf_path)


@pytest.fixture
def sample_jd(tmp_path):
    jd_path = tmp_path / "jd.txt"
    jd_path.write_text(
        "招聘全栈开发工程师，要求熟悉 Python、React，有大模型 API 经验优先。",
        encoding="utf-8",
    )
    return str(jd_path)


def test_parse_command(tmp_path):
    pdf = _make_sample_pdf(tmp_path)
    result = runner.invoke(app, ["parse", pdf])
    assert result.exit_code == 0
    assert "Hello" in result.stdout or "Resume" in result.stdout


def test_extract_command_mock(tmp_path):
    pdf = _make_sample_pdf(tmp_path)
    result = runner.invoke(app, ["extract", pdf, "--mock"])
    assert result.exit_code == 0
    assert "张三" in result.stdout
    assert "Python" in result.stdout


def test_score_command_mock(tmp_path, sample_jd):
    pdf = _make_sample_pdf(tmp_path)
    result = runner.invoke(app, ["score", pdf, "--jd", sample_jd, "--mock"])
    assert result.exit_code == 0
    assert "overall_score" in result.stdout
    assert "82" in result.stdout
    assert "interview_questions" in result.stdout


def test_extract_with_output(tmp_path):
    pdf = _make_sample_pdf(tmp_path)
    out_file = tmp_path / "result.json"
    result = runner.invoke(
        app, ["extract", pdf, "--mock", "--output", str(out_file)]
    )
    assert result.exit_code == 0
    assert out_file.exists()
    assert "张三" in out_file.read_text(encoding="utf-8")


def test_score_jd_not_found(tmp_path):
    pdf = _make_sample_pdf(tmp_path)
    result = runner.invoke(
        app, ["score", pdf, "--jd", str(tmp_path / "missing.txt"), "--mock"]
    )
    assert result.exit_code == 1
    assert "文件不存在" in result.stdout or "文件不存在" in result.stderr or "Error" in result.stdout
