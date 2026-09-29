from formatters.docx_formatter import format_docx
from formatters.pdf_formatter import format_pdf
from formatters.text_formatter import format_txt

SAMPLE = """NON-DISCLOSURE AGREEMENT

1. CONFIDENTIALITY
The parties agree to protect confidential information.

2. TERM
The agreement starts on the effective date.

SIGNATURES
Disclosing Party: ____________________
Receiving Party: ____________________
"""

def test_txt():
    assert format_txt(SAMPLE).startswith(b"NON-DISCLOSURE")

def test_docx():
    assert format_docx(SAMPLE, "Non-Disclosure Agreement", "Confidentiality; Term")[:2] == b"PK"

def test_pdf():
    assert format_pdf(SAMPLE, "Non-Disclosure Agreement", "Confidentiality; Term").startswith(b"%PDF")
