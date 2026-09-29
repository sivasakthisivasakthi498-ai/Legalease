import html
import os
from datetime import date
import requests
import streamlit as st
from dotenv import load_dotenv
from formatters.docx_formatter import format_docx
from formatters.pdf_formatter import format_pdf
from formatters.text_formatter import format_txt

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")

st.markdown("""
<style>
.stApp { background:#f6f8fb; }
.hero { padding:1.4rem 1.6rem; border-radius:18px; background:linear-gradient(135deg,#0f172a,#1e293b); color:white; margin-bottom:1rem; }
.hero h1 { margin:0; font-size:2.1rem; }
.hero p { margin:.35rem 0 0; color:#cbd5e1; }
.preview { background:#0f172a; color:#e2e8f0; padding:1.25rem; border-radius:14px; max-height:620px; overflow-y:auto; white-space:pre-wrap; font-family:Georgia,serif; line-height:1.55; }
.notice { background:#fff7ed; border:1px solid #fed7aa; color:#7c2d12; padding:.9rem 1rem; border-radius:12px; margin:1rem 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>⚖️ LegalEase</h1>
<p>AI-powered legal document drafting, editing, preview, and export.</p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="notice"><strong>Important:</strong> LegalEase creates drafts for '
    'informational use. It does not replace advice from a qualified legal professional.</div>',
    unsafe_allow_html=True,
)

if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""
if "last_doc_type" not in st.session_state:
    st.session_state.last_doc_type = ""

with st.sidebar:
    st.header("Document Details")
    document_type = st.selectbox(
        "Document type",
        [
            "Employment Contract",
            "Non-Disclosure Agreement",
            "Lease Agreement",
            "Freelance Work Contract",
            "Service Agreement",
            "Employment Offer Letter",
            "General Agreement",
            "Custom",
        ],
    )
    if document_type == "Custom":
        document_type = st.text_input("Custom document type", placeholder="e.g. Partnership Agreement")

    parties = st.text_area(
        "Parties involved", height=120,
        placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)"
    )
    terms = st.text_area(
        "Terms & conditions", height=180,
        placeholder="Payment within 30 days; Confidentiality must be maintained; Either party may terminate with 15 days notice",
        help="Separate multiple terms with semicolons.",
    )
    effective_date = st.date_input("Effective date", value=date.today())
    generate = st.button("✨ Generate Document", type="primary", width="stretch")

if generate:
    if not document_type.strip() or not parties.strip() or not terms.strip():
        st.error("Please complete the document type, parties, and terms.")
    else:
        try:
            with st.spinner("Generating your draft with Gemini..."):
                res = requests.post(
                    f"{BACKEND_URL}/generate",
                    json={
                        "document_type": document_type,
                        "parties": parties,
                        "terms": terms,
                        "effective_date": effective_date.isoformat(),
                    },
                    timeout=120,
                )
            if res.ok:
                data = res.json()
                st.session_state.generated_text = data["content"]
                st.session_state.last_doc_type = document_type
                st.success(f"Draft generated using {data.get('model', 'Gemini')}.")
            else:
                try:
                    detail = res.json().get("detail", res.text)
                except Exception:
                    detail = res.text
                st.error(f"Backend error: {detail}")
        except requests.RequestException as exc:
            st.error("Could not connect to FastAPI. Start the backend first.")
            st.caption(str(exc))

left, right = st.columns([1, 1])

with left:
    st.subheader("Editable document")
    edited = st.text_area(
        "Edit the generated document",
        value=st.session_state.generated_text,
        height=620,
        label_visibility="collapsed",
        placeholder="Your generated document will appear here.",
    )
    st.session_state.generated_text = edited

with right:
    st.subheader("Live preview")
    if st.session_state.generated_text:
        st.markdown(
            f'<div class="preview">{html.escape(st.session_state.generated_text)}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.info("Generate a document to see the preview.")

st.divider()
st.subheader("Download")

if st.session_state.generated_text:
    doc_type = st.session_state.last_doc_type or document_type
    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button(
            "⬇️ Download TXT",
            format_txt(st.session_state.generated_text),
            "legalease_document.txt",
            "text/plain",
            width="stretch",
        )
    with c2:
        st.download_button(
            "⬇️ Download DOCX",
            format_docx(st.session_state.generated_text, doc_type, terms),
            "legalease_document.docx",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            width="stretch",
        )
    with c3:
        st.download_button(
            "⬇️ Download PDF",
            format_pdf(st.session_state.generated_text, doc_type, terms),
            "legalease_document.pdf",
            "application/pdf",
            width="stretch",
        )
else:
    st.caption("Generate a document first to enable downloads.")
