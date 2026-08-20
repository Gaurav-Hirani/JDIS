import httpx
import json

BASE_URL = "http://127.0.0.1:8000"

payload = {
    "state_code": "01",
    "dist_code": "01",
    "court_no": "01",
    "type_name": "criminal appeal",
    "filing_month": 5,
    "filing_day_of_week": 2,
    "filing_quarter": 2,
    "case_type_str": "criminal",
    "case_category": "criminal",
    "is_criminal_code": 1,
    "statutory_act_count": 1,
    "ipc_section_count": 2,
    "bailable_ipc_flag": "bailable",
    "primary_act_id": "act_ipc",
    "female_defendant_clean": "0",
    "female_petitioner_clean": "0",
    "female_adv_def_clean": "0",
    "female_adv_pet_clean": "0",
    "state_str": "Maharashtra",
    "district_str": "Mumbai",
    "court_str": "Chief Metropolitan Magistrate",
    "ddl_filing_judge_id": "judge_101",
    "judge_position_clean": "magistrate",
    "judge_gender": "male",
    "judge_tenure_days": 500.0,
    "court_prior_delay_rate": 0.45,
    "court_prior_avg_duration": 650.0,
    "court_prior_active_backlog": 1200.0,
    "casetype_prior_delay_rate": 0.38
}

print("=== STARTING JDIS RUNTIME SMOKE TEST ===\n")

with httpx.Client(base_url=BASE_URL, timeout=10.0) as client:
    # 1. Health Check
    print("1. GET /health")
    res = client.get("/health")
    print(f"Status: {res.status_code}")
    print(json.dumps(res.json(), indent=2))
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
    print("-> HEALTH CHECK PASSED\n")

    # 2. Prediction Delay Endpoint
    print("2. POST /api/v1/predictions/delay")
    res = client.post("/api/v1/predictions/delay", json=payload)
    print(f"Status: {res.status_code}")
    delay_data = res.json()
    print(json.dumps(delay_data, indent=2))
    assert res.status_code == 200
    assert "calibrated_probability" in delay_data
    assert "risk_score" in delay_data
    assert "risk_band" in delay_data
    pred_id = delay_data["prediction_id"]
    print("-> DELAY PREDICTION ENDPOINT PASSED\n")

    # 3. Prediction Duration Endpoint
    print("3. POST /api/v1/predictions/duration")
    res = client.post("/api/v1/predictions/duration", json=payload)
    print(f"Status: {res.status_code}")
    duration_data = res.json()
    print(json.dumps(duration_data, indent=2))
    assert res.status_code == 200
    assert "predicted_duration_days" in duration_data
    assert "limitations_flag" in duration_data
    print("-> DURATION PREDICTION ENDPOINT PASSED\n")

    # 4. Explanation Endpoint
    print(f"4. GET /api/v1/predictions/{pred_id}/explanation")
    res = client.get(f"/api/v1/predictions/{pred_id}/explanation")
    print(f"Status: {res.status_code}")
    exp_data = res.json()
    print(json.dumps(exp_data, indent=2))
    assert res.status_code == 200
    assert "top_contributors" in exp_data
    assert len(exp_data["top_contributors"]) > 0
    print("-> EXPLANATION ENDPOINT PASSED\n")

    # 5. Case CRUD API
    print("5. POST /api/v1/cases")
    case_payload = payload.copy()
    case_payload["ddl_case_id"] = "smoke_test_case_001"
    res = client.post("/api/v1/cases", json=case_payload)
    print(f"Status: {res.status_code}")
    case_data = res.json()
    print(json.dumps(case_data, indent=2))
    assert res.status_code == 201
    case_id = case_data["id"]

    print(f"\n6. GET /api/v1/cases/{case_id}")
    res = client.get(f"/api/v1/cases/{case_id}")
    print(f"Status: {res.status_code}")
    assert res.status_code == 200

    print("\n7. GET /api/v1/cases")
    res = client.get("/api/v1/cases?state_code=01")
    print(f"Status: {res.status_code}")
    print(f"Cases Count: {res.json()['total']}")
    assert res.status_code == 200

    print(f"\n8. PATCH /api/v1/cases/{case_id}")
    res = client.patch(f"/api/v1/cases/{case_id}", json={"court_str": "Smoke Test High Court"})
    print(f"Status: {res.status_code}")
    assert res.status_code == 200
    assert res.json()["court_str"] == "Smoke Test High Court"
    print("-> CASE CRUD ENDPOINTS PASSED\n")

    # 6. Analytics API
    print("9. GET /api/v1/analytics/summary")
    res = client.get("/api/v1/analytics/summary")
    print(f"Status: {res.status_code}")
    print(json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    print("\n10. GET /api/v1/analytics/risk-distribution")
    res = client.get("/api/v1/analytics/risk-distribution")
    print(f"Status: {res.status_code}")
    print(json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    print("\n11. GET /api/v1/analytics/courts")
    res = client.get("/api/v1/analytics/courts")
    print(f"Status: {res.status_code}")
    print(json.dumps(res.json(), indent=2))
    assert res.status_code == 200

    print("\n12. GET /api/v1/analytics/case-types")
    res = client.get("/api/v1/analytics/case-types")
    print(f"Status: {res.status_code}")
    print(json.dumps(res.json(), indent=2))
    assert res.status_code == 200
    print("-> ANALYTICS ENDPOINTS PASSED\n")

print("=== ALL RUNTIME SMOKE TESTS COMPLETED SUCCESSFULLY ===")
