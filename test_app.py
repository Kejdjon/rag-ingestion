from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_home():
    response = client.get("/")
    assert response.status_code == 200

def test_rag():
    response = client.post(
        "/rag/query",
        json={"question":"AI"}
    )
    assert response.status_code == 200

def test_agent():
    response = client.post(
        "/agent/query",
        json={"question":"Hello"}
    )
    assert response.status_code == 200

def test_document_process():
    response = client.post(
        "/document/process",
        json={"file_name":"INVOICE.pdf"}
    )
    assert response.status_code == 200