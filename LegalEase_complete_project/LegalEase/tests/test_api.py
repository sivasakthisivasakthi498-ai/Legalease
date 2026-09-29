from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["name"] == "LegalEase"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_generate_validation():
    response = client.post("/generate", json={
        "document_type": "",
        "parties": "A, B",
        "terms": "Confidentiality",
        "effective_date": "2026-09-28",
    })
    assert response.status_code == 422


def test_generate_rejects_whitespace_only_fields():
    response = client.post("/generate", json={
        "document_type": "   ",
        "parties": "  ",
        "terms": "   ",
        "effective_date": "2026-09-28",
    })
    assert response.status_code == 422
