from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

def test_home():
    r = client.get("/")
    assert r.status_code == 200
    assert "EduGenie" in r.text

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
