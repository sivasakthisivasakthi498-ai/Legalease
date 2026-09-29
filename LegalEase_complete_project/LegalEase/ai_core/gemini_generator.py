import os
import time
from typing import Optional
from dotenv import load_dotenv
from google import genai

load_dotenv()

class GeminiDocumentGenerator:
    """Generate legal-document drafts using Google's current GenAI SDK."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        raw_api_key = (api_key or os.getenv("GEMINI_API_KEY") or "").strip()
        self.api_key = raw_api_key or None

        raw_model = (model or os.getenv("GEMINI_MODEL") or "gemini-3.8-flash").strip()
        self.model = raw_model or "gemini-3.8-flash"
        raw_fallback = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-2.5-flash").strip()
        self.fallback_model = raw_fallback or None
        try:
            self.max_retries = max(0, int(os.getenv("GEMINI_MAX_RETRIES", "2")))
        except ValueError:
            self.max_retries = 2
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None

    @staticmethod
    def build_prompt(document_type, parties, terms, effective_date):
        items = [
            item.strip()
            for item in terms.replace("\n", ";").split(";")
            if item.strip()
        ]
        term_text = "\n".join(f"- {x}" for x in items)

        return f"""
You are LegalEase, an AI assistant that drafts legal-document templates.

Create a clear, professional FIRST DRAFT of the requested legal document.

Document type: {document_type}
Parties: {parties}
Effective date: {effective_date}
Requested terms:
{term_text}

Requirements:
1. Use supplied facts only. Never invent names, addresses, amounts, dates, jurisdictions,
   registration numbers, or obligations.
2. Use a title and numbered sections.
3. Include parties and effective date.
4. Add appropriate clauses only when relevant to the document and supplied information.
5. If an important detail is missing, use a placeholder such as [JURISDICTION] instead of guessing.
6. Use neutral professional language.
7. Do not claim universal legal validity.
8. Return only the document draft, with signature blocks at the end.
""".strip()

    def generate_document(self, document_type, parties, terms, effective_date):
        if not self.client:
            raise ValueError("GEMINI_API_KEY is not configured. Add it to .env.")

        prompt = self.build_prompt(document_type, parties, terms, effective_date)
        models = [self.model]
        if self.fallback_model and self.fallback_model not in models:
            models.append(self.fallback_model)

        last_error = None
        for model in models:
            for attempt in range(self.max_retries + 1):
                try:
                    response = self.client.models.generate_content(
                        model=model,
                        contents=prompt,
                    )
                    text = getattr(response, "text", None)
                    if not text or not text.strip():
                        raise RuntimeError("Gemini returned an empty response.")
                    return text.strip()
                except Exception as exc:
                    last_error = exc
                    if self._is_authentication_error(exc):
                        raise RuntimeError(
                            "Gemini authentication failed. Replace GEMINI_API_KEY in .env "
                            "with a valid Google AI Studio API key."
                        ) from exc
                    if not self._is_transient_error(exc) or attempt >= self.max_retries:
                        break
                    time.sleep(2 ** attempt)

        raise RuntimeError(
            f"Gemini API request failed after trying {', '.join(models)}: {last_error}"
        ) from last_error

    @staticmethod
    def _is_transient_error(error: Exception) -> bool:
        message = str(error).upper()
        return any(code in message for code in ("429", "500", "502", "503", "504", "UNAVAILABLE"))

    @staticmethod
    def _is_authentication_error(error: Exception) -> bool:
        message = str(error).upper()
        return any(code in message for code in ("401", "UNAUTHENTICATED", "INVALID API KEY", "API_KEY_INVALID"))
