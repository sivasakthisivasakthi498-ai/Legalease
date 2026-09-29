from io import BytesIO
import re
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
from formatters.text_formatter import sanitize_text

def _footer(document):
    p = document.sections[0].footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("LegalEase - AI-generated draft. Review with a qualified legal professional.")
    r.font.name = "Times New Roman"
    r.font.size = Pt(8)

def _cell(cell, text, bold=False):
    cell.text = ""
    r = cell.paragraphs[0].add_run(text)
    r.bold = bold
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)

def format_docx(text: str, doc_type: str, terms: str = "") -> bytes:
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(.75)
        s.bottom_margin = Inches(.75)
        s.left_margin = Inches(.9)
        s.right_margin = Inches(.9)
    doc.styles["Normal"].font.name = "Times New Roman"
    doc.styles["Normal"].font.size = Pt(11)
    _footer(doc)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(sanitize_text(doc_type).upper())
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("LEGAL DOCUMENT DRAFT")
    r.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(10)

    for raw in sanitize_text(text).splitlines():
        line = raw.strip()
        if not line:
            continue
        p = doc.add_paragraph()
        if re.match(r"^(SECTION\s+)?\d+[\.\):\-]\s+", line, re.I) or (
            line.upper() == line and len(line) <= 90
        ):
            r = p.add_run(line)
            r.bold = True
            r.font.size = Pt(12)
        elif line.startswith(("- ", "• ")):
            p.style = "List Bullet"
            r = p.add_run(line[2:].strip())
        else:
            r = p.add_run(line)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    if terms.strip():
        doc.add_page_break()
        h = doc.add_paragraph()
        r = h.add_run("TERMS PROVIDED BY USER")
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        items = [x.strip() for x in terms.replace("\n", ";").split(";") if x.strip()]
        table = doc.add_table(rows=1, cols=2)
        table.style = "Table Grid"
        _cell(table.rows[0].cells[0], "#", True)
        _cell(table.rows[0].cells[1], "Term", True)
        for i, item in enumerate(items, 1):
            cells = table.add_row().cells
            _cell(cells[0], str(i))
            _cell(cells[1], item)

    out = BytesIO()
    doc.save(out)
    return out.getvalue()
