# LegalEase — Complete AI Legal Document Generator

This implementation follows the supplied LegalEase documentation: Streamlit frontend, FastAPI backend, Gemini AI generation, editable preview, and TXT/DOCX/PDF export. The source documentation describes inputs for document type, parties, terms and dates, plus the `/generate` endpoint and the three export formats. 

The original document specifies Gemini 1.5 Pro and the older `google-generativeai` package. This project uses the current Google `google-genai` SDK and a configurable Gemini model. The default is `gemini-3.8-flash`; change `GEMINI_MODEL` in `.env` if needed.

## Run in VS Code

### 1. Create environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configure API key

Copy `.env.example` to `.env` and set:

```text
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-3.8-flash
BACKEND_URL=http://127.0.0.1:8000
```

Never commit `.env`.

### 3. Start FastAPI

```powershell
uvicorn main:app --reload --port 8000
```

Open `http://127.0.0.1:8000/docs`.

### 4. Start Streamlit in a second terminal

```powershell
streamlit run app.py
```

Open `http://localhost:8501`.

### 5. Run tests

```powershell
pytest -q
```

The tests do not call Gemini.

## Features

- Employment Contract
- NDA
- Lease Agreement
- Freelance Work Contract
- Service Agreement
- Offer Letter
- General/custom document type
- Parties and effective date
- Semicolon-separated terms
- Gemini generation
- Editable text
- Dark preview
- TXT export
- DOCX export with Times New Roman, headings, terms table and footer
- PDF export with header/footer and terms
- FastAPI validation and API documentation
- Environment-variable configuration
- Dockerfile and Procfile

## Safety

LegalEase produces drafts for informational purposes. It should not claim that a generated document is universally valid. Missing jurisdiction-specific information is represented with placeholders instead of being invented. Users should have documents reviewed by a qualified legal professional before signing or relying on them.
