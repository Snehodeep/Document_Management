import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_ingest_document():
    response = client.post("/ingest", json={"content": "This is a test document."})
    assert response.status_code == 200
    assert response.json() == {"message": "Document ingested successfully"}
