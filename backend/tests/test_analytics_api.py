from fastapi.testclient import TestClient

def test_analytics_summary_endpoint(client: TestClient, sample_case_features):
    # Seed a case & prediction
    client.post("/api/v1/cases", json=sample_case_features)

    res = client.get("/api/v1/analytics/summary")
    assert res.status_code == 200
    data = res.json()
    
    assert "total_cases" in data
    assert "total_predictions" in data
    assert "high_risk_cases_count" in data
    assert "average_risk_score" in data
    assert data["total_cases"] >= 1

def test_risk_distribution_endpoint(client: TestClient):
    res = client.get("/api/v1/analytics/risk-distribution")
    assert res.status_code == 200
    data = res.json()
    
    assert len(data) == 4
    bands = {item["risk_band"] for item in data}
    assert bands == {"Low", "Moderate", "High", "Very High"}

def test_court_analytics_endpoint(client: TestClient, sample_case_features):
    client.post("/api/v1/cases", json=sample_case_features)
    res = client.get("/api/v1/analytics/courts")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)

def test_case_type_analytics_endpoint(client: TestClient, sample_case_features):
    client.post("/api/v1/cases", json=sample_case_features)
    res = client.get("/api/v1/analytics/case-types")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
