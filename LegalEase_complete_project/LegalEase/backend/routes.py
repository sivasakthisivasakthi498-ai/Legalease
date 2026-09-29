import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
generator = GeminiDocumentGenerator()

class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=120)
    parties: str = Field(..., min_length=2, max_length=5000)
    terms: str = Field(..., min_length=2, max_length=10000)
    effective_date: str = Field(..., min_length=2, max_length=120)

    @field_validator("document_type", "parties", "terms", "effective_date")
    @classmethod
    def strip_and_validate(cls, value: str) -> str:
        if value is None:
            raise ValueError("Field cannot be empty.")
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Field cannot be empty or whitespace only.")
        return cleaned

class DocumentResponse(BaseModel):
    document_type: str
    content: str
    model: str

@router.post("/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest):
    try:
        content = generator.generate_document(
            request.document_type,
            request.parties,
            request.terms,
            request.effective_date,
        )
        return DocumentResponse(
            document_type=request.document_type,
            content=content,
            model=generator.model,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected generation error: {exc}") from exc
