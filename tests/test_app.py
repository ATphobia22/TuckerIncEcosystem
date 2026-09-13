from fastapi.testclient import TestClient

from tuckerinc82.app import app


client = TestClient(app)


def test_health_endpoint_reports_ready():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_sources_endpoint_exposes_registered_sources():
    response = client.get("/api/sources")
    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 1
    assert any(item["source_id"] == "usgs-03378500" for item in body["sources"])
