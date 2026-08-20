# JDIS Backend Implementation Plan & Architecture Audit

**Role**: Namdeo — Dedicated Backend Developer / API / Database / ML Serving / Deployment  
**Branch**: `feature/backend`  
**Date**: 2026-08-20  
**Status**: Ready for Human Review  

---

## 1. Executive Summary & Audit Findings

### 1.1 Handoff Documentation Audit

| Document Name | Expected Path | Actual Repository Path | Status | Observations |
| :--- | :--- | :--- | :--- | :--- |
| **Backend Handoff Checklist** | `docs/BACKEND_HANDOFF_CHECKLIST.md` | `docs/BACKEND_HANDOFF_CHECKLIST.md` | **Verified** | Authoritative checklist and rules confirmed. |
| **Final ML Handoff to Backend** | `docs/data/FINAL_ML_HANDOFF_TO_BACKEND.md` | `docs/data/FINAL_ML_HANDOFF_TO_BACKEND.md` | **Verified** | Config D, 29 features, pipeline specs confirmed. |
| **ML Inference Contract** | `docs/api/ML_INFERENCE_CONTRACT.md` | `docs/api/ML_INFERENCE_CONTRACT.md` | **Verified** | JSON input and output schemas confirmed. |
| **Final Model Card** | `research/FINAL_MODEL_CARD.md` | `research/FINAL_MODEL_CARD.md` | **Verified** | Model metrics and target definitions verified. |
| **Final Model Feature Specification** | `research/FINAL_MODEL_FEATURE_SPECIFICATION.md` | `research/experiments/FINAL_MODEL_FEATURE_SPECIFICATION.md` | **Verified (Located)** | Located in `research/experiments/`. 29 features documented. |
| **Risk Score Specification** | `research/RISK_SCORE_SPECIFICATION.md` | `research/experiments/RISK_SCORE_SPECIFICATION.md` | **Verified (Located)** | Located in `research/experiments/`. Thresholds: Low (0-20), Mod (21-50), High (51-80), Very High (81-100). |
| **Final XAI Results** | `research/FINAL_XAI_RESULTS.md` | `research/FINAL_XAI_RESULTS.md` | **Verified** | Global and local SHAP interpretation verified. |
| **Final AI Research Handoff** | `research/FINAL_AI_RESEARCH_HANDOFF.md` | `research/FINAL_AI_RESEARCH_HANDOFF.md` | **Verified** | ML stream frozen. Dataset C negative result confirmed. |
| **Reproducibility Guide** | `research/REPRODUCIBILITY.md` | `research/REPRODUCIBILITY.md` | **Verified** | Pipeline reproducibility and seeds verified. |
| **Architecture Overview** | `docs/ARCHITECTURE.md` | `docs/ARCHITECTURE.md` | **0-byte File** | Existing file is empty; backend architecture documented herein. |
| **Project Scope** | `docs/PROJECT_SCOPE.md` | `docs/PROJECT_SCOPE.md` | **0-byte File** | Existing file is empty; scope established by checklist. |
| **Team Workflow** | `docs/TEAM_WORKFLOW.md` | `docs/TEAM_WORKFLOW.md` | **0-byte File** | Existing file is empty; branch workflow maintained. |

### 1.2 Model Artifact & Serving Verification

Both production model artifacts exist in `models/` and were tested for real-time inference:

1. **Classification Pipeline**: `models/final_calibrated_clf.joblib` (638 KB)
   - **Structure**: `CalibratedClassifierCV` (Isotonic regression wrapper fitted on 2015 validation set) wrapping an underlying `Pipeline` (`ColumnTransformer` with `SimpleImputer` + `OneHotEncoder(handle_unknown='ignore')` + `XGBClassifier`).
   - **Verification Status**: Validated with Python. Ingests 29 raw features without manual pre-encoding. Returns calibrated probability (0.0 to 1.0) and calculates risk score via `floor(calibrated_probability * 100)`.
   - **Dependency Finding**: Model unpickling requires `xgboost<3.0.0` (tested and verified with `xgboost==2.1.4`).

2. **Regression Pipeline**: `models/best_ablation_reg.joblib` (843 KB)
   - **Structure**: Scikit-learn `Pipeline` (`ColumnTransformer` + `XGBRegressor`).
   - **Verification Status**: Validated with Python. Outputs continuous `predicted_case_duration_days`.
   - **Documentation Constraint**: Endpoint will return standard caveat flag: *"Systematically underpredicts extreme outliers (>5 years)."*

3. **SHAP TreeExplainer Local Attribution**:
   - Extracted base estimator tree from `CalibratedClassifierCV` and base pipeline transformer.
   - Tested and verified fast SHAP attribution extraction using `shap.TreeExplainer(model)` on transformed feature representations, mapped to parent conceptual groups via `src/xai/shap_mapping.py`.

4. **Dataset C (Next-Listing Delay)**:
   - Documented negative research result ($R^2 = -1.7032$). Banned from production API endpoints.

---

## 2. Target Backend Architecture

```
                                  +----------------------------------------------------+
                                  |                 Frontend / Client                  |
                                  +-------------------------+--------------------------+
                                                            | HTTP / REST
                                                            v
+-------------------------------------------------------------------------------------------------------------------+
| FastAPI Application (backend/app/main.py)                                                                         |
|                                                                                                                   |
|  [Middleware & Security]                                                                                          |
|   - CORS Middleware (configurable allowed origins)                                                                |
|   - Request ID & Structured Logging Middleware                                                                    |
|   - Global Exception Handlers (Pydantic validation, NotFound, Unprocessable, Internal)                           |
|                                                                                                                   |
|  [API Routers (backend/app/api/v1/)]                                                                              |
|   - /health                      -> HealthCheckRouter (System, DB, ML Models status)                              |
|   - /api/v1/predictions/delay    -> PredictionRouter (Filing delay probability, risk score, band, SHAP)           |
|   - /api/v1/predictions/duration -> DurationRouter (Duration days prediction with limitations)                  |
|   - /api/v1/predictions/{id}/exp -> ExplanationRouter (Detailed SHAP decomposition)                              |
|   - /api/v1/cases                -> CaseRouter (CRUD, list, search, filter)                                       |
|   - /api/v1/analytics            -> AnalyticsRouter (Summary, risk distributions, court & case type metrics)      |
|                                                                                                                   |
|  [Application Services (backend/app/services/)]                                                                   |
|   - PredictionService            -> Orchestrates ML inference, calibration, risk scoring                          |
|   - ExplanationService           -> SHAP tree explanation & conceptual parent feature aggregation                 |
|   - RiskService                  -> Deterministic risk score (floor(p*100)) & band assignment                     |
|   - CaseService                  -> Case lifecycle management, DB persistence & validation                        |
|   - AnalyticsService             -> Aggregate metrics, court throughput, risk clustering                          |
|                                                                                                                   |
|  [ML Model Serving Container (backend/app/ml/)]                                                                   |
|   - ModelManager (Singleton)     -> Loads models once at startup, caches pipelines, health checks, versioning     |
|                                                                                                                   |
|  [Data Access Layer (backend/app/db/ & backend/app/models/)]                                                      |
|   - SQLAlchemy 2.0 Models: Case, Prediction, Explanation                                                          |
|   - Async/Sync Session Management & Repository Pattern                                                            |
+----------------------------------------------------+--------------------------------------------------------------+
                                                     |
                                                     v
                                  +----------------------------------------------------+
                                  |              PostgreSQL 15+ Database               |
                                  |    Tables: cases, predictions, explanations        |
                                  +----------------------------------------------------+
```

---

## 3. Database Design (PostgreSQL + SQLAlchemy 2.0)

### 3.1 `cases` Table
Stores legal case filings and the 29 raw model features.
- `id` (UUID / Integer, Primary Key, indexed)
- `ddl_case_id` (VARCHAR(64), Nullable, external reference index)
- **Filing Attributes**:
  - `filing_month` (INTEGER)
  - `filing_day_of_week` (INTEGER)
  - `filing_quarter` (INTEGER)
  - `type_name` (VARCHAR(128), Not Null, indexed)
  - `case_type_str` (VARCHAR(128))
  - `case_category` (VARCHAR(64))
  - `is_criminal_code` (INTEGER)
  - `statutory_act_count` (INTEGER)
  - `ipc_section_count` (INTEGER)
  - `bailable_ipc_flag` (VARCHAR(32))
  - `primary_act_id` (VARCHAR(128))
- **Party & Representation Attributes**:
  - `female_defendant_clean` (VARCHAR(32))
  - `female_petitioner_clean` (VARCHAR(32))
  - `female_adv_def_clean` (VARCHAR(32))
  - `female_adv_pet_clean` (VARCHAR(32))
- **Court & Geography Attributes**:
  - `state_code` (VARCHAR(32), Not Null, indexed)
  - `dist_code` (VARCHAR(32), Not Null, indexed)
  - `court_no` (VARCHAR(32), Not Null, indexed)
  - `state_str` (VARCHAR(128))
  - `district_str` (VARCHAR(128))
  - `court_str` (VARCHAR(256))
- **Judge Attributes**:
  - `ddl_filing_judge_id` (VARCHAR(64), indexed)
  - `judge_position_clean` (VARCHAR(128))
  - `judge_gender` (VARCHAR(32))
  - `judge_tenure_days` (FLOAT)
- **Historical Throughput Attributes**:
  - `court_prior_delay_rate` (FLOAT)
  - `court_prior_avg_duration` (FLOAT)
  - `court_prior_active_backlog` (FLOAT)
  - `casetype_prior_delay_rate` (FLOAT)
- **Metadata**:
  - `created_at` (TIMESTAMP WITH TIME ZONE, default=now())
  - `updated_at` (TIMESTAMP WITH TIME ZONE, default=now(), onupdate=now())

### 3.2 `predictions` Table
Stores inference outputs and risk assessments linked to cases or generated standalone.
- `id` (UUID, Primary Key)
- `case_id` (UUID, Foreign Key to `cases.id`, Nullable, indexed)
- `model_version` (VARCHAR(64), Not Null)
- `prediction_type` (VARCHAR(32), e.g., 'delay_classification', 'duration_regression')
- `raw_probability` (FLOAT, Nullable)
- `calibrated_probability` (FLOAT, Nullable)
- `risk_score` (INTEGER, Nullable)
- `risk_band` (VARCHAR(32), Nullable, indexed)
- `predicted_duration_days` (FLOAT, Nullable)
- `limitations_flag` (TEXT, Nullable)
- `created_at` (TIMESTAMP WITH TIME ZONE, default=now(), indexed)

### 3.3 `explanations` Table
Stores precomputed SHAP explanations linked to prediction instances.
- `id` (UUID, Primary Key)
- `prediction_id` (UUID, Foreign Key to `predictions.id`, Not Null, indexed)
- `feature_name` (VARCHAR(128), Not Null)
- `parent_feature` (VARCHAR(128), Not Null)
- `feature_group` (VARCHAR(64), Not Null)
- `human_readable_description` (TEXT)
- `contribution` (FLOAT, Not Null)
- `direction` (VARCHAR(16), 'positive' or 'negative')
- `feature_value` (TEXT)
- `rank` (INTEGER, Not Null)
- `created_at` (TIMESTAMP WITH TIME ZONE, default=now())

---

## 4. API Endpoints Specification

### 4.1 Health Check
- `GET /health`
  - Returns `{ "status": "ok", "database": "ok", "models": "ok", "version": "1.0.0" }`

### 4.2 Prediction APIs
- `POST /api/v1/predictions/delay`
  - Input: 29 Config D features (Pydantic schema per `ML_INFERENCE_CONTRACT.md`).
  - Output: `prediction_id`, `raw_probability`, `calibrated_probability`, `risk_score`, `risk_band`, `model_version`, `shap_explanations`.
- `POST /api/v1/predictions/duration`
  - Input: 29 Config D features.
  - Output: `predicted_duration_days`, `limitations_flag`, `model_version`.
- `GET /api/v1/predictions/{prediction_id}/explanation`
  - Output: Top SHAP attributions, parent concepts, direction, human-readable descriptors.

### 4.3 Case Management APIs
- `POST /api/v1/cases`: Create case and optionally trigger initial prediction.
- `GET /api/v1/cases/{case_id}`: Retrieve case by ID with associated prediction history.
- `GET /api/v1/cases`: Paginated list of cases with filtering (`state_code`, `dist_code`, `court_no`, `type_name`, `risk_band`).
- `PATCH /api/v1/cases/{case_id}`: Update case metadata.

### 4.4 Analytics APIs
- `GET /api/v1/analytics/summary`: Aggregate counts (total cases, high/very high risk proportion, avg predicted duration).
- `GET /api/v1/analytics/risk-distribution`: Distribution breakdown across Low, Moderate, High, Very High bands.
- `GET /api/v1/analytics/courts`: Court-level risk summaries and case counts.
- `GET /api/v1/analytics/case-types`: Case-type risk summaries and counts.

---

## 5. Execution Phase Plan

```
Phase 1: Backend Architecture & Directory Scaffold
├── Configure pyproject.toml, requirements.txt, .env.example
├── Setup backend/app/core/config.py (pydantic-settings)
└── Setup structured logging & exception handlers

Phase 2: Database Layer & Migrations
├── Implement SQLAlchemy 2.0 Base & Models (Case, Prediction, Explanation)
├── Configure Alembic environment
└── Generate initial migration (001_initial_schema.py)

Phase 3: Centralized Model Serving Manager
├── Implement backend/app/ml/manager.py (Singleton loading at startup)
├── Implement validation checks & version metadata
└── Add fallback handling for missing artifacts

Phase 4: Prediction & Risk Services
├── Implement PredictionService & DurationService
├── Implement RiskService (floor(p*100) and exact band thresholds)
└── Wire POST /api/v1/predictions/delay & POST /api/v1/predictions/duration

Phase 5: SHAP Explanation Service
├── Implement ExplanationService with shap.TreeExplainer
├── Integrate parent feature mapping & human-readable definitions
└── Wire GET /api/v1/predictions/{id}/explanation

Phase 6: Case Management APIs
├── Implement CaseService & CaseRepository (CRUD, filtering, pagination)
└── Wire /api/v1/cases endpoints

Phase 7: Analytics APIs
├── Implement AnalyticsService with PostgreSQL aggregation queries
└── Wire /api/v1/analytics endpoints

Phase 8: Comprehensive Testing
├── Unit tests: Schemas, risk score, services
├── API tests: Health, predictions, duration, explanations, cases, analytics
├── Database tests: CRUD, persistence, constraints
└── ML integration tests: Frozen pipeline verification without raw parquet requirement

Phase 9: Docker Deployment & Setup
├── Create production Dockerfile
├── Create docker-compose.yml (FastAPI + PostgreSQL + Migrations)
└── Write docs/BACKEND_SETUP.md

Phase 10: Frontend Integration Contract Documentation
└── Author docs/api/FRONTEND_API_GUIDE.md for Shukla
```

---

## 6. Verification Plan

### 6.1 Automated Testing
- Execute full test suite: `.venv\Scripts\pytest backend/tests/ -v`
- Verify 100% endpoint coverage across health, predictions, explanations, cases, analytics.
- Verify schema validation on invalid inputs (missing required fields, out-of-range numerics).

### 6.2 ML Semantic Integrity
- Calibrated probability formula: strictly preserved.
- Risk score: strictly `floor(calibrated_probability * 100)`.
- Risk bands: Low (0–20), Moderate (21–50), High (51–80), Very High (81–100).
- Regressor: includes explicit limitations disclaimer.
- Dataset C: strictly excluded from production endpoints.

---

## 7. Approval Request
This plan and audit are submitted for human review prior to implementing production backend code.
