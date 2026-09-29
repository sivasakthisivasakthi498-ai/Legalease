from io import BytesIO
import re
from fpdf import FPDF
from formatters.text_formatter import sanitize_text

class LegalEasePDF(FPDF):
    def header(self):
        self.set_font("Times", "B", 12)
        self.cell(self.w - self.l_margin - self.r_margin, 8, "LegalEase", align="C")
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Times", "", 8)
        self.cell(
            self.w - self.l_margin - self.r_margin,
            10,
            "AI-generated draft - review with a qualified legal professional.",
            align="C",
        )

def format_pdf(text: str, doc_type: str, terms: str = "") -> bytes:
    pdf = LegalEasePDF()
    pdf.set_auto_page_break(True, margin=18)
    pdf.add_page()
    page_width = pdf.w - pdf.l_margin - pdf.r_margin

    pdf.set_font("Times", "B", 16)
    pdf.multi_cell(page_width, 9, sanitize_text(doc_type).upper(), align="C")
    pdf.set_font("Times", "I", 10)
    pdf.multi_cell(page_width, 6, "LEGAL DOCUMENT DRAFT", align="C")
    pdf.ln(5)

    for raw in sanitize_text(text).splitlines():
        line = raw.strip()
        if not line:
            pdf.ln(3)
            continue
        if re.match(r"^(SECTION\s+)?\d+[\.\):\-]\s+", line, re.I) or (
            line.upper() == line and len(line) <= 90
        ):
            pdf.set_font("Times", "B", 11)
        else:
            pdf.set_font("Times", "", 11)
        if line.startswith(("- ", "• ")):
            line = "• " + line[2:].strip()
        pdf.multi_cell(page_width, 6, line)

    if terms.strip():
        pdf.ln(5)
        pdf.set_font("Times", "B", 12)
        pdf.cell(page_width, 7, "TERMS PROVIDED BY USER")
        pdf.ln(8)
        for i, item in enumerate(
            [x.strip() for x in terms.replace("\n", ";").split(";") if x.strip()], 1
        ):
            pdf.set_font("Times", "", 10)
            pdf.multi_cell(page_width, 6, f"{i}. {item}")

    out = BytesIO()
    pdf.output(out)
    return out.getvalue()
