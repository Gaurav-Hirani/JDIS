from fastapi.testclient import TestClient

def test_create_and_get_case(client: TestClient, sample_case_features):
    # 1. Create case
    case_payload = sample_case_features.copy()
    case_payload["ddl_case_id"] = "test_case_999"

    create_res = client.post("/api/v1/cases", json=case_payload)
    assert create_res.status_code == 201
    case_data = create_res.json()
    
    assert "id" in case_data
    assert case_data["ddl_case_id"] == "test_case_999"
    assert case_data["latest_prediction"] is not None
    assert case_data["latest_prediction"]["risk_score"] is not None
    case_id = case_data["id"]

    # 2. Get case details
    get_res = client.get(f"/api/v1/cases/{case_id}")
    assert get_res.status_code == 200
    detail_data = get_res.json()
    assert detail_data["id"] == case_id
    assert len(detail_data["predictions"]) > 0

def test_list_and_filter_cases(client: TestClient, sample_case_features):
    # Create two cases with different states
    c1 = sample_case_features.copy()
    c1["state_code"] = "10"
    c1["type_name"] = "bail application"
    client.post("/api/v1/cases", json=c1)

    c2 = sample_case_features.copy()
    c2["state_code"] = "20"
    c2["type_name"] = "civil suit"
    client.post("/api/v1/cases", json=c2)

    # Filter by state_code = 10
    res = client.get("/api/v1/cases?state_code=10")
    assert res.status_code == 200
    list_data = res.json()
    assert list_data["total"] >= 1
    for item in list_data["items"]:
        assert item["state_code"] == "10"

def test_update_case(client: TestClient, sample_case_features):
    create_res = client.post("/api/v1/cases", json=sample_case_features)
    case_id = create_res.json()["id"]

    patch_payload = {"court_str": "Updated District High Court"}
    update_res = client.patch(f"/api/v1/cases/{case_id}", json=patch_payload)
    assert update_res.status_code == 200
    assert update_res.json()["court_str"] == "Updated District High Court"

def test_get_nonexistent_case(client: TestClient):
    response = client.get("/api/v1/cases/nonexistent-case-uuid")
    assert response.status_code == 404
