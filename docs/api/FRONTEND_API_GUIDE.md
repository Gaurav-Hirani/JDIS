# JDIS Frontend API Integration Guide

**Target Audience**: Shukla (Frontend Engineering Team)  
**Base URL**: `http://localhost:8000/api/v1`  
**Interactive Swagger Docs**: `http://localhost:8000/docs`  
**ReDoc Specification**: `http://localhost:8000/redoc`  

---

## 1. System Overview & Health Check

### `GET /health`
Verifies backend operational status, PostgreSQL database connectivity, and ML model loading state.

#### Response JSON (`200 OK`)
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

## 2. Prediction Endpoints

### 2.1 Filing-Time Case Delay Classification & Risk Score
#### `POST /api/v1/predictions/delay`
Evaluates the probability of severe delay (>24 months) at the time of case filing, computes the JDIS 0–100 integer risk score, assigns an interpretable risk band, and returns top SHAP explainability drivers.

#### Request Headers
`Content-Type: application/json`

#### Request Body Schema (29 Config D Features)
```json
{
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
```

#### Field Validation Rules
- `state_code`, `dist_code`, `court_no`, `type_name`: **Required** strings.
- `filing_month`: Integer `1` to `12` (Default: `1`).
- `filing_day_of_week`: Integer `0` to `6` (Default: `1`).
- `filing_quarter`: Integer `1` to `4` (Default: `1`).
- `is_criminal_code`: Integer `0` or `1`.

#### Response JSON (`200 OK`)
```json
{
  "prediction_id": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
  "case_id": null,
  "raw_probability": 0.8129,
  "calibrated_probability": 0.8129,
  "risk_score": 81,
  "risk_band": "Very High",
  "model_version": "v1.0-config-d",
  "timestamp": "2026-08-20T09:45:00Z",
  "shap_explanations": [
    {
      "feature_name": "type_name",
      "contribution": 2.0657,
      "direction": "positive",
      "feature_group": "Basic Case",
      "human_readable_description": "Granular case type identifier"
    },
    {
      "feature_name": "ddl_filing_judge_id",
      "contribution": -1.0135,
      "direction": "negative",
      "feature_group": "Judge Attributes",
      "human_readable_description": "Filing judge historical assignment ID"
    }
  ]
}
```

---

### 2.2 Filing-Time Case Duration Estimation
#### `POST /api/v1/predictions/duration`
Predicts expected case duration in days.

#### Response JSON (`200 OK`)
```json
{
  "prediction_id": "b32d4fae-7dec-11d0-a765-00a0c91e6bf6",
  "predicted_duration_days": 540.0,
  "model_version": "v1.0-config-d",
  "limitations_flag": "Systematically underpredicts extreme outliers (>5 years). Associational estimate only.",
  "timestamp": "2026-08-20T09:45:00Z"
}
```

---

### 2.3 Detailed SHAP Decomposition
#### `GET /api/v1/predictions/{prediction_id}/explanation`
Retrieves stored local SHAP explanation breakdown with conceptual parent feature groups and human-readable summary.

#### Response JSON (`200 OK`)
```json
{
  "prediction_id": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
  "model_version": "v1.0-config-d",
  "calibrated_probability": 0.8129,
  "risk_score": 81,
  "risk_band": "Very High",
  "top_contributors": [
    {
      "feature_name": "type_name",
      "parent_feature": "type_name",
      "feature_group": "Basic Case",
      "human_readable_description": "Granular case type identifier",
      "contribution": 2.0657,
      "direction": "positive",
      "rank": 1
    }
  ],
  "summary": "Primary factors driving delay risk higher include: type_name.",
  "timestamp": "2026-08-20T09:45:00Z"
}
```

---

## 3. Case Management Endpoints

### 3.1 Create Case Filing Record
#### `POST /api/v1/cases`
Creates a case record in PostgreSQL and automatically executes the delay prediction.

#### Response JSON (`201 Created`)
```json
{
  "id": "c12d4fae-7dec-11d0-a765-00a0c91e6bf6",
  "ddl_case_id": "case_987654",
  "state_code": "01",
  "dist_code": "01",
  "court_no": "01",
  "type_name": "criminal appeal",
  "created_at": "2026-08-20T09:45:00Z",
  "updated_at": "2026-08-20T09:45:00Z",
  "latest_prediction": {
    "id": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
    "model_version": "v1.0-config-d",
    "prediction_type": "delay_classification",
    "calibrated_probability": 0.8129,
    "risk_score": 81,
    "risk_band": "Very High",
    "created_at": "2026-08-20T09:45:00Z"
  }
}
```

---

### 3.2 List & Filter Cases
#### `GET /api/v1/cases?page=1&page_size=20&risk_band=Very High`
Returns paginated cases filtered by state, court, case type, or risk band.

#### Response JSON (`200 OK`)
```json
{
  "total": 42,
  "page": 1,
  "page_size": 20,
  "items": [
    {
      "id": "c12d4fae-7dec-11d0-a765-00a0c91e6bf6",
      "type_name": "criminal appeal",
      "state_code": "01",
      "dist_code": "01",
      "court_no": "01",
      "latest_prediction": {
        "risk_score": 81,
        "risk_band": "Very High"
      }
    }
  ]
}
```

---

## 4. Analytics & Dashboard Endpoints

### 4.1 System Analytics Summary
#### `GET /api/v1/analytics/summary`
```json
{
  "total_cases": 150,
  "total_predictions": 180,
  "high_risk_cases_count": 45,
  "high_risk_cases_percentage": 25.0,
  "average_risk_score": 48.5,
  "average_predicted_duration_days": 580.2
}
```

### 4.2 Risk Band Distribution
#### `GET /api/v1/analytics/risk-distribution`
```json
[
  { "risk_band": "Low", "count": 45, "percentage": 30.0 },
  { "risk_band": "Moderate", "count": 60, "percentage": 40.0 },
  { "risk_band": "High", "count": 30, "percentage": 20.0 },
  { "risk_band": "Very High", "count": 15, "percentage": 10.0 }
]
```

---

## 5. Standard Error Responses

All API errors return a uniform error structure:

#### Example: `422 Unprocessable Entity` (Validation Error)
```json
{
  "error": true,
  "message": "Input validation error",
  "details": [
    {
      "loc": ["body", "state_code"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ],
  "path": "/api/v1/predictions/delay"
}
```

#### Example: `404 Not Found`
```json
{
  "error": true,
  "message": "Case with ID 'nonexistent-uuid' was not found",
  "details": {},
  "path": "/api/v1/cases/nonexistent-uuid"
}
```
