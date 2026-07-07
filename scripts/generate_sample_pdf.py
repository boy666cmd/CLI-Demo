"""Generate a sample PDF resume for testing."""

from pathlib import Path

RAW_PDF = b"""%PDF-1.4
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Contents 4 0 R/Resources<</Font<</F1 5 0 R>>>>>>endobj
4 0 obj<</Length 200>>stream
BT /F1 12 Tf 100 750 Td (Zhang San) Tj ET
BT /F1 10 Tf 100 730 Td (Phone: 13800138000) Tj ET
BT /F1 10 Tf 100 710 Td (Email: zhangsan@example.com) Tj ET
BT /F1 10 Tf 100 690 Td (City: Beijing) Tj ET
BT /F1 10 Tf 100 670 Td (Skills: Python, JavaScript, React, FastAPI) Tj ET
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
0000000480 00000 n 
trailer<</Size 6/Root 1 0 R>>
startxref
560
%%EOF"""


def main() -> None:
    out = Path(__file__).resolve().parent.parent / "samples" / "resume.pdf"
    out.write_bytes(RAW_PDF)
    print(f"Generated: {out}")


if __name__ == "__main__":
    main()
