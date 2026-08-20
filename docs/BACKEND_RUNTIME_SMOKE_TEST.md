# JDIS Backend Runtime Smoke Test Report

**Environment**: Local Uvicorn + SQLite/PostgreSQL Database  
**Branch**: `feature/backend`  
**Date**: 2026-08-20  
**Status**: **PASSED — All Live Runtime API Smoke Tests Verified**

---

## 1. Environment & Container Setup Audit

- **Docker Environment**: Windows host system does not have Docker Desktop daemon installed. The container definition in `Dockerfile` and service orchestration in `docker-compose.yml` were statically validated.
- **Live Runtime Server**: Live server executed via `.venv\Scripts\python -m uvicorn backend.app.main:app --port 8000`.
- **Database Migration**: Alembic migration (`alembic upgrade head`) executed cleanly, establishing tables `cases`, `predictions`, and `explanations`.

---

## 2. Live Runtime Test Results

### 2.1 Health Check Endpoint (`GET /health`)
- **Status Code**: `200 OK`
- **Response**:
```json
{
  "status": "ok",
  "database": "ok",
  "models": "ok",
  "model_version": "v1.0-config-d",
  "details": {
    "classifier_loaded": true,
    "regressor_loaded": true,
    "shap_ready": true
  }
}
```

---

### 2.2 Filing Delay Prediction Endpoint (`POST /api/v1/predictions/delay`)
- **Status Code**: `200 OK`
- **Response**:
```json
{
  "prediction_id": "45147c5b-0147-4253-b982-70c4e4d6e629",
  "case_id": null,
  "raw_probability": 0.8003,
  "calibrated_probability": 0.8129,
  "risk_score": 81,
  "risk_band": "Very High",
  "model_version": "v1.0-config-d",
  "timestamp": "2026-08-20T04:50:21.402084Z",
  "shap_explanations": [
    {
      "feature_name": "case_type_str",
      "contribution": -6.0263,
      "direction": "negative",
      "feature_group": "Basic Case",
      "human_readable_description": "Standardized case type category"
    },
    {
      "feature_name": "ddl_filing_judge_id",
      "contribution": -4.3727,
      "direction": "negative",
      "feature_group": "Judge Attributes",
      "human_readable_description": "Filing judge historical assignment ID"
    },
    {
      "feature_name": "type_name",
      "contribution": 1.7175,
      "direction": "positive",
      "feature_group": "Basic Case",
      "human_readable_description": "Granular case type identifier"
    },
    {
      "feature_name": "female_defendant_clean",
      "contribution": -0.4574,
      "direction": "negative",
      "feature_group": "Demographics",
      "human_readable_description": "Presence of female defendant"
    },
    {
      "feature_name": "female_adv_def_clean",
      "contribution": 0.4041,
      "direction": "positive",
      "feature_group": "Demographics",
      "human_readable_description": "Female defense legal counsel representation"
    }
  ]
}
```

---

### 2.3 Case Duration Endpoint (`POST /api/v1/predictions/duration`)
- **Status Code**: `200 OK`
- **Response**:
```json
{
  "prediction_id": "a1c56a4d-0129-46f5-ac7b-0e7bc8983041",
  "predicted_duration_days": 540.0,
  "model_version": "v1.0-config-d",
  "limitations_flag": "Systematically underpredicts extreme outliers (>5 years). Associational estimate only.",
  "timestamp": "2026-08-20T04:50:21.484287Z"
}
```

---

### 2.4 SHAP Explanation Endpoint (`GET /api/v1/predictions/{id}/explanation`)
- **Status Code**: `200 OK`
- **Response**:
```json
{
  "prediction_id": "45147c5b-0147-4253-b982-70c4e4d6e629",
  "model_version": "v1.0-config-d",
  "calibrated_probability": 0.8128842711448669,
  "risk_score": 81,
  "risk_band": "Very High",
  "top_contributors": [
    {
      "feature_name": "case_type_str",
      "parent_feature": "case_type_str",
      "feature_group": "Basic Case",
      "human_readable_description": "Standardized case type category",
      "contribution": -6.0263,
      "direction": "negative",
      "feature_value": null,
      "rank": 1
    },
    {
      "feature_name": "type_name",
      "parent_feature": "type_name",
      "feature_group": "Basic Case",
      "human_readable_description": "Granular case type identifier",
      "contribution": 1.7175,
      "direction": "positive",
      "feature_value": null,
      "rank": 3
    }
  ],
  "summary": "Primary factors driving delay risk higher include: type_name, female_adv_def_clean. Mitigating factors pulling delay risk lower include: case_type_str, ddl_filing_judge_id.",
  "timestamp": "2026-08-20T04:50:21.402084"
}
```

---

### 2.5 Case CRUD Operations
- `POST /api/v1/cases`: Created case record `3174b198-1cbb-4964-8894-69832d13096f` with auto-prediction attached (`201 Created`).
- `GET /api/v1/cases/{id}`: Successfully retrieved persisted case (`200 OK`).
- `GET /api/v1/cases`: Successfully listed cases with filtering (`200 OK`).
- `PATCH /api/v1/cases/{id}`: Updated case attribute `court_str` to `"Smoke Test High Court"` (`200 OK`).

---

### 2.6 Analytics Endpoints
- `GET /api/v1/analytics/summary`: Returned `total_cases: 1`, `total_predictions: 3`, `high_risk_cases_count: 2`, `average_risk_score: 81.0` (`200 OK`).
- `GET /api/v1/analytics/risk-distribution`: Returned 4 risk bands with exact counts (`200 OK`).
- `GET /api/v1/analytics/courts`: Aggregated caseload metrics by court (`200 OK`).
- `GET /api/v1/analytics/case-types`: Aggregated caseload metrics by case type (`200 OK`).

---

## 3. Model Compatibility & Handoff Verification

- **Model Artifact Loading**: Loaded `models/final_calibrated_clf.joblib` and `models/best_ablation_reg.joblib` with `xgboost==2.1.4` without errors.
- **Frontend API Documentation**: Verified [`docs/api/FRONTEND_API_GUIDE.md`](file:///d:/JDIS/docs/api/FRONTEND_API_GUIDE.md) accurately reflects all active endpoints and JSON schemas.

---

## 4. Conclusion

All runtime smoke tests passed. The backend is verified and ready for merge into main.
