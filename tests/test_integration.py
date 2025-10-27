from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_api_add():
    response = client.get("/calculate/add?a=2&b=3")
    assert response.status_code == 200
    assert response.json()["result"] == 5

def test_api_subtract():
    response = client.get("/calculate/subtract?a=10&b=4")
    assert response.status_code == 200
    assert response.json()["result"] == 6
