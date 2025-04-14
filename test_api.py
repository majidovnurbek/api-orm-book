from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_users():
    response = client.get("/apps")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "apps"