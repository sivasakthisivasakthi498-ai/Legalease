import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import router

load_dotenv()

app = FastAPI(
    title="LegalEase API",
    description="AI-powered legal document draft generator.",
    version="1.0.0",
)

origins = [
    x.strip() for x in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:8501,http://127.0.0.1:8501"
    ).split(",") if x.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {"name": "LegalEase", "status": "running", "docs": "/docs", "health": "/health"}

@app.get("/health")
def health():
    return {"status": "ok"}
