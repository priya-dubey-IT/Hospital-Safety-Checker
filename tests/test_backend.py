import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from main import app
from app.database_sqlite import db

@pytest.fixture
def client():
    # Use a fresh client for each test
    with TestClient(app) as c:
        yield c

def test_health_check(client):
    """Smoke Test: Verify the health endpoint is alive."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_doctors(client):
    """Integration Test: Verify doctor retrieval from database."""
    response = client.get("/api/patient/doctors")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["doctors"], list)

def test_registration_flow(client):
    """Unit/Integration Test: Test the core registration logic."""
    test_data = {
        "doctor_name": "Test Dr. Smith",
        "doctor_category": "Internal Medicine",
        "patient_name": "John Doe Patient"
    }
    response = client.post("/api/registration/main", json=test_data)
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_invalid_registration(client):
    """Negative Test: Verify system handles missing data correctly."""
    response = client.post("/api/registration/main", json={"doctor_name": ""})
    # FastAPI returns 422 for missing required fields in the model
    assert response.status_code == 422

def test_database_connection():
    """Structural Test: Verify SQLite database connection is active."""
    # The database connects via the lifespan of the app in TestClient
    assert db.db is not None
