from fastapi.testclient import TestClient

def test_predict_delay_endpoint(client: TestClient, sample_case_features):
    response = client.post("/api/v1/predictions/delay", json=sample_case_features)
    assert response.status_code == 200
    data = response.json()
    
    assert "prediction_id" in data
    assert "calibrated_probability" in data
    assert "risk_score" in data
    assert "risk_band" in data
    assert "model_version" in data
    assert "shap_explanations" in data
    assert data["risk_band"] in ["Low", "Moderate", "High", "Very High"]
    assert 0 <= data["risk_score"] <= 100
    assert len(data["shap_explanations"]) > 0

def test_predict_duration_endpoint(client: TestClient, sample_case_features):
    response = client.post("/api/v1/predictions/duration", json=sample_case_features)
    assert response.status_code == 200
    data = response.json()
    
    assert "prediction_id" in data
    assert "predicted_duration_days" in data
    assert "limitations_flag" in data
    assert "underpredicts extreme outliers" in data["limitations_flag"]
    assert data["predicted_duration_days"] > 0

def test_get_explanation_endpoint(client: TestClient, sample_case_features):
    # 1. Create prediction first
    pred_res = client.post("/api/v1/predictions/delay", json=sample_case_features)
    pred_id = pred_res.json()["prediction_id"]

    # 2. Query explanation
    exp_res = client.get(f"/api/v1/predictions/{pred_id}/explanation")
    assert exp_res.status_code == 200
    data = exp_res.json()
    
    assert data["prediction_id"] == pred_id
    assert "top_contributors" in data
    assert "summary" in data
    assert len(data["top_contributors"]) > 0

def test_get_nonexistent_explanation(client: TestClient):
    response = client.get("/api/v1/predictions/nonexistent-id-12345/explanation")
    assert response.status_code == 404
    assert response.json()["error"] is True
