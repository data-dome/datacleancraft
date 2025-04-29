from fastapi.testclient import TestClient
from datacleancraft.api import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_clean_endpoint(tmp_path):
    """Test /clean API."""
    input_file = tmp_path / "sample.csv"
    input_file.write_text("name,location\nJohn Doe,New York\nJane Smith,London")

    with open(input_file, "rb") as f:
        response = client.post(
            "/clean",
            files={"file": ("sample.csv", f, "text/csv")},
            data={"export_format": "csv", "anomaly_threshold": 0.1}
        )

    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "success"
    assert isinstance(result["data"], list)
