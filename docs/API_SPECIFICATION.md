# JDIS Backend API Specification

Complete reference for the FastAPI application. Every route, schema, parameter, and
status code below is transcribed from the implementation in `backend/app/`.

- **Base URL** — `http://localhost:8000`
- **API prefix** — `/api/v1`
- **Interactive docs** — `GET /docs` (Swagger UI) and `GET /redoc` (ReDoc)
- **OpenAPI schema** — `GET /api/v1/openapi.json`
- **Model version** — `v1.0-config-d`

---

## Authentication and configuration

There is **no authentication layer**. The application is intended for internal
decision-support use on a trusted network, not for public exposure.

CORS is enabled for `settings.BACKEND_CORS_ORIGINS` with `allow_credentials=True`,
`allow_methods=["*"]`, `allow_headers=["*"]`. Defaults are the four localhost origins on
ports 3000 and 8000.

Every request is logged with method, path, status code, and latency in milliseconds.

## Error model

All errors return a consistent envelope:

```json
{
  "error": true,
  "message": "Case with ID 'uuid' was not found",
  "details": {},
  "path": "/api/v1/cases/uuid"
}
```

| Condition | Status | Exception |
| :--- | :--- | :--- |
| Malformed or out-of-range request body | `422` | `RequestValidationError` → `validation_exception_handler` |
| Inference failure on supplied features | `422` | `InferenceException` |
| Unknown case ID | `404` | `CaseNotFoundException` |
| Unknown prediction ID | `404` | `PredictionNotFoundException` |
| Model artifact missing or unloadable | `503` | `ModelNotFoundException` |
| Anything else | `500` | `generic_exception_handler` (returns a generic message, no internals) |

The `500` handler deliberately does not echo the exception text to the client.

---

## Route index

| Method | Path | Summary |
| :--- | :--- | :--- |
| `GET` | `/` | Root info (excluded from schema) |
| `GET` | `/health` | System health check |
| `GET` | `/api/v1/health` | System health check (mounted at both paths) |
| `POST` | `/api/v1/predictions/delay` | Predict filing-time delay and risk score |
| `POST` | `/api/v1/predictions/duration` | Predict expected case duration |
| `GET` | `/api/v1/predictions/{prediction_id}/explanation` | SHAP explanation for a prediction |
| `POST` | `/api/v1/cases` | Create case and run initial prediction |
| `GET` | `/api/v1/cases/{case_id}` | Get case details |
| `GET` | `/api/v1/cases` | List and filter cases |
| `PATCH` | `/api/v1/cases/{case_id}` | Update case metadata |
| `GET` | `/api/v1/analytics/summary` | System analytics summary |
| `GET` | `/api/v1/analytics/risk-distribution` | Risk band distribution |
| `GET` | `/api/v1/analytics/courts` | Court-level delay analytics |
| `GET` | `/api/v1/analytics/case-types` | Case-type delay analytics |

---

## 1. System

### `GET /`

Not included in the OpenAPI schema. Returns orientation metadata only.

```json
{
  "project": "Judicial Delay Intelligence System (JDIS)",
  "version": "1.0.0",
  "docs_url": "/docs",
  "health_url": "/health",
  "api_v1_url": "/api/v1"
}
```

### `GET /health` · `GET /api/v1/health`

Both paths are live. Each performs a live `SELECT 1` against the database and reads the
ML manager's in-memory status — a slow or failing response indicates a real problem.

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

`status` is `ok` only when both the database probe and the ML manager report `ok`;
otherwise `degraded`. On database failure `database` carries the exception text
directly, e.g. `"error: connection refused"`.

---

## 2. Predictions

### `POST /api/v1/predictions/delay`

Computes the calibrated delay probability, risk score, risk band, and top SHAP
contributions from the 29 Config D features.

**Query parameters**

| Name | Type | Default | Notes |
| :--- | :--- | :--- | :--- |
| `save` | `bool` | `true` | When `false`, no prediction row is written and `prediction_id` is returned as `null` |
| `case_id` | `str` | `null` | Optional link to an existing case record |

**Request body** — `CaseFilingFeatures` (see [schemas](#casefilingfeatures))

**Response** — `200 OK`, `RiskPredictionResponse`

```json
{
  "prediction_id": "8f3c…",
  "case_id": null,
  "raw_probability": 0.81,
  "calibrated_probability": 0.74,
  "risk_score": 74,
  "risk_band": "High",
  "model_version": "v1.0-config-d",
  "timestamp": "2026-10-16T10:24:00",
  "shap_explanations": [
    {
      "feature_name": "court_prior_delay_rate",
      "contribution": 1.92,
      "direction": "positive",
      "feature_group": "Historical Throughput",
      "human_readable_description": "Historical delay rate of the court at filing"
    }
  ]
}
```

`raw_probability` and `calibrated_probability` are both constrained to `[0.0, 1.0]`.
`risk_score` is `floor(calibrated_probability * 100)`, constrained to `[0, 100]`.
`risk_band` is the literal enum `Low` | `Moderate` | `High` | `Very High`.

### `POST /api/v1/predictions/duration`

Same request body and query parameters as `/delay`.

**Response** — `200 OK`, `DurationPredictionResponse`

```json
{
  "prediction_id": "9b1a…",
  "predicted_duration_days": 712.4,
  "model_version": "v1.0-config-d",
  "limitations_flag": "Systematically underpredicts extreme outliers (>5 years). Associational estimate only.",
  "timestamp": "2026-10-16T10:24:00.123456+00:00"
}
```

`limitations_flag` is a fixed string, always populated, and returned verbatim. Clients
should surface it alongside the number rather than the number alone. The model also
clamps output to a minimum of 1.0 day, so a sub-day prediction will not appear.

### `GET /api/v1/predictions/{prediction_id}/explanation`

**Path parameter** — `prediction_id: str`

Returns `404` via `PredictionNotFoundException` if the ID is unknown.

**Response** — `200 OK`, `PredictionExplanationResponse`

```json
{
  "prediction_id": "8f3c…",
  "model_version": "v1.0-config-d",
  "calibrated_probability": 0.74,
  "risk_score": 74,
  "risk_band": "High",
  "top_contributors": [
    {
      "feature_name": "court_prior_delay_rate",
      "parent_feature": "Court Delay History",
      "feature_group": "Historical Throughput",
      "human_readable_description": "Historical delay rate of the court at filing",
      "contribution": 1.92,
      "direction": "positive",
      "feature_value": "0.72",
      "rank": 1
    }
  ],
  "summary": "Primary factors driving delay risk higher include: Court Delay History, Case Backlog. Mitigating factors pulling delay risk lower include: Statutory Category.",
  "timestamp": "2026-10-16T10:24:00.123456+00:00"
}
```

`summary` is assembled server-side from the top-2 positive and top-2 negative
`parent_feature` values. When neither exists it falls back to a neutral throughput
sentence. `direction` is `positive` (raises delay risk) or `negative` (lowers it).

---

## 3. Cases

### `POST /api/v1/cases`

**Query parameter** — `auto_predict: bool = true`. When `false`, the case is stored with
`latest_prediction` set to `null`.

**Request body** — `CaseCreate` (all `CaseFilingFeatures` fields, plus optional
`ddl_case_id`)

**Response** — `201 Created`, `CaseResponse`

An automatic prediction failure is caught and logged as a warning; the case is still
created and the request still returns `201` with `latest_prediction: null`. This is
deliberate — case registration should not fail because the model did.

### `GET /api/v1/cases/{case_id}`

**Response** — `200 OK`, `CaseDetailResponse` — the case with its full prediction
history. `latest_prediction` is set to the first (most recent) entry in `predictions`.
`404` if unknown.

### `GET /api/v1/cases`

**Query parameters**

| Name | Type | Default | Bounds | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `page` | `int` | `1` | `>= 1` | 1-indexed |
| `page_size` | `int` | `20` | `1–100` | Items per page |
| `state_code` | `str` | `null` | — | Exact match |
| `dist_code` | `str` | `null` | — | Exact match |
| `court_no` | `str` | `null` | — | Exact match |
| `type_name` | `str` | `null` | — | Case-insensitive substring (`ilike %value%`) |
| `risk_band` | `str` | `null` | — | Exact match, joins to `Prediction.risk_band` |

Results are ordered by `created_at` descending. `total` is the pre-pagination count, so
it is correct even on an empty page.

**Response** — `200 OK`, `CaseListResponse`

```json
{
  "total": 137,
  "page": 2,
  "page_size": 20,
  "items": [ { "id": "uuid", "state_code": "01", "risk_score": 61 } ]
}
```

### `PATCH /api/v1/cases/{case_id}`

**Request body** — `CaseUpdate`. Only supplied fields change (`exclude_unset=True`), so
partial updates are safe.

**Response** — `200 OK`, `CaseResponse`. `404` if unknown.

**Predictions are not regenerated.** A case edit never invalidates, recomputes, or
rewrites its stored risk score — predictions are immutable once written. If you need a
re-evaluation, call `/api/v1/predictions/delay` with `save=false` or against the case.

---

## 4. Analytics

All four are read-only aggregates over persisted case and prediction rows. An empty
database returns valid responses with zero counts rather than errors.

### `GET /api/v1/analytics/summary`

**Response** — `200 OK`, `AnalyticsSummaryResponse`

```json
{
  "total_cases": 137,
  "total_predictions": 204,
  "high_risk_cases_count": 41,
  "high_risk_cases_percentage": 29.93,
  "average_risk_score": 52.4,
  "average_predicted_duration_days": 611.2
}
```

`average_predicted_duration_days` falls back to `0.0` when no duration predictions exist.
A `0.0` therefore means "no data", not "zero days" — clients should not render it as a
meaningful duration.

### `GET /api/v1/analytics/risk-distribution`

**Response** — `200 OK`, `RiskDistributionItem[]`

```json
[
  { "risk_band": "Low",       "count": 33, "percentage": 24.09 },
  { "risk_band": "Moderate",  "count": 52, "percentage": 37.96 },
  { "risk_band": "High",      "count": 28, "percentage": 20.44 },
  { "risk_band": "Very High", "count": 24, "percentage": 17.52 }
]
```

### `GET /api/v1/analytics/courts`

**Query parameter** — `limit: int = 15`, bounds `1–50`

**Response** — `200 OK`, `CourtRiskItem[]`

```json
[
  {
    "court_identifier": "01-01-01",
    "state_code": "01",
    "dist_code": "01",
    "court_no": "01",
    "case_count": 18,
    "average_risk_score": 68.3,
    "high_risk_percentage": 55.56,
    "average_duration_days": 702.1
  }
]
```

### `GET /api/v1/analytics/case-types`

**Query parameter** — `limit: int = 15`, bounds `1–50`

**Response** — `200 OK`, `CaseTypeRiskItem[]`

```json
[
  {
    "type_name": "criminal appeal",
    "case_count": 47,
    "average_risk_score": 64.1,
    "high_risk_percentage": 42.55
  }
]
```

---

## Schemas

### `CaseFilingFeatures`

The canonical 29-feature input. Only four fields are required; every other field has a
safe default. `extra="ignore"`, so unknown keys are dropped rather than rejected — which
keeps older clients working if the feature set grows.

**Required**

| Field | Type | Example |
| :--- | :--- | :--- |
| `state_code` | `str` | `"01"` |
| `dist_code` | `str` | `"01"` |
| `court_no` | `str` | `"01"` |
| `type_name` | `str` | `"criminal appeal"` |

**Calendar**

| Field | Type | Default | Constraints |
| :--- | :--- | :--- | :--- |
| `filing_month` | `int` | `1` | `1–12` |
| `filing_day_of_week` | `int` | `1` | `0–6` |
| `filing_quarter` | `int` | `1` | `1–4` |

**Case category**

| Field | Type | Default |
| :--- | :--- | :--- |
| `case_type_str` | `str` | `"unknown"` |
| `case_category` | `str` | `"unknown"` |
| `is_criminal_code` | `int` | `0` (`0/1`) |
| `statutory_act_count` | `int` | `0` (>= 0) |
| `ipc_section_count` | `int` | `0` (>= 0) |
| `bailable_ipc_flag` | `str` | `"unknown"` |
| `primary_act_id` | `str` | `"unknown"` |

**Demographics / representation**

| Field | Type | Default |
| :--- | :--- | :--- |
| `female_defendant_clean` | `str` | `"0"` |
| `female_petitioner_clean` | `str` | `"0"` |
| `female_adv_def_clean` | `str` | `"0"` |
| `female_adv_pet_clean` | `str` | `"0"` |

**Geography strings**

| Field | Type | Default |
| :--- | :--- | :--- |
| `state_str` | `str` | `"unknown"` |
| `district_str` | `str` | `"unknown"` |
| `court_str` | `str` | `"unknown"` |

**Judge features**

| Field | Type | Default | Constraints |
| :--- | :--- | :--- | :--- |
| `ddl_filing_judge_id` | `str` | `"unknown"` | — |
| `judge_position_clean` | `str` | `"unknown"` | — |
| `judge_gender` | `str` | `"unknown"` | — |
| `judge_tenure_days` | `float` | `0.0` | `>= 0.0` |

**Historical throughput** — these four carry the majority of the model's signal

| Field | Type | Default | Constraints |
| :--- | :--- | :--- | :--- |
| `court_prior_delay_rate` | `float` | `0.0` | `0.0–1.0` |
| `court_prior_avg_duration` | `float` | `0.0` | `>= 0.0` |
| `court_prior_active_backlog` | `float` | `0.0` | `>= 0.0` |
| `casetype_prior_delay_rate` | `float` | `0.0` | `0.0–1.0` |

The throughput features are computed **strictly before** the filing timestamp — they are
prior history, never derived from the outcome being predicted.

### `CaseCreate`

`CaseFilingFeatures` plus `ddl_case_id: Optional[str] = None` — an external identifier.

### `CaseUpdate`

All optional, all defaulting to `null`. Only the keys present in the request body are
applied.

| Field | Type |
| :--- | :--- |
| `state_code`, `dist_code`, `court_no`, `type_name` | `str` |
| `state_str`, `district_str`, `court_str` | `str` |
| `ddl_filing_judge_id`, `judge_position_clean`, `judge_gender` | `str` |
| `judge_tenure_days`, `court_prior_delay_rate`, `court_prior_avg_duration`, `court_prior_active_backlog`, `casetype_prior_delay_rate` | `float` |

### `CaseResponse`

`CaseFilingFeatures` plus `id`, `ddl_case_id`, `created_at`, `updated_at`, and
`latest_prediction: Optional[PredictionSummary]`.

### `CaseDetailResponse`

`CaseResponse` plus `predictions: PredictionSummary[]`.

### `PredictionSummary`

| Field | Type | Notes |
| :--- | :--- | :--- |
| `id` | `str` | |
| `model_version` | `str` | |
| `prediction_type` | `str` | `delay_classification` or duration |
| `raw_probability` | `float` | Classification only |
| `calibrated_probability` | `float` | Classification only |
| `risk_score` | `int` | Classification only |
| `risk_band` | `str` | Classification only |
| `predicted_duration_days` | `float` | Regression only |
| `limitations_flag` | `str` | Regression only |
| `created_at` | `datetime` | |

Duration and classification fields are mutually exclusive by convention — a
classification row leaves the duration fields `null` and vice versa.

### `RiskPredictionResponse`

See [`POST /predictions/delay`](#post-apiv1predictionsdelay).
Nested `shap_explanations` uses `SHAPExplanationItem`: `feature_name`, `contribution`,
`direction`, `feature_group`, `human_readable_description`.

### `PredictionExplanationResponse`

See [`GET /predictions/{id}/explanation`](#get-apiv1predictionsprediction_idexplanation).
Nested `top_contributors` uses `ExplanationDetail`, which adds `parent_feature`,
`feature_value`, and `rank` to the SHAP item fields.

---

## Notes for integrators

- **Timestamps** are timezone-aware UTC (`datetime.now(timezone.utc)`), serialised as
  ISO 8601 with a `+00:00` offset. Note that `RiskPredictionResponse.timestamp` and
  `DurationPredictionResponse.timestamp` declare `default_factory=datetime.utcnow` in
  the schema, but the services always pass an explicit aware datetime, so `utcnow` is
  never reached.
- **IDs** are UUID4 strings generated server-side.
- **Risk bands** are plain words without any "Risk" suffix. The literal values are
  `Low`, `Moderate`, `High`, `Very High`.
- **The classifier is the useful component.** The duration regressor returns a number
  plus a mandatory `limitations_flag`; its held-out R² is negative. Do not present
  duration output without that flag.
- **Model v1.0-config-d has never seen a case filed after 2016.** Its behaviour on
  newer filings is unmeasured.
