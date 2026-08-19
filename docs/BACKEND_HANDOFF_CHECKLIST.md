# JDIS Backend Handoff Checklist

This checklist is intended exclusively for Namdeo (Backend Integration). The AI/Research phase is complete, mathematically frozen, and verified.

## 1. What to Read First
You must explicitly review these exact documentation files before writing any backend infrastructure:
1. `docs/data/FINAL_ML_HANDOFF_TO_BACKEND.md`
2. `docs/api/ML_INFERENCE_CONTRACT.md`
3. `research/FINAL_MODEL_CARD.md`
4. `research/experiments/FINAL_MODEL_FEATURE_SPECIFICATION.md`
5. `research/experiments/RISK_SCORE_SPECIFICATION.md`
6. `research/FINAL_XAI_RESULTS.md`

## 2. Authoritative Model Artifacts
- **Classification Pipeline (Production)**: `models/final_calibrated_clf.joblib` (Includes XGBoost model + Isotonic Calibrator + Preprocessors). This is the only endpoint approved for risk banding.
- **Regression Pipeline (Secondary)**: `models/best_ablation_reg.joblib`. 

## 3. The 29 Features
You are required to map frontend/database requests to the **exact 29 features** specified in Config D. A schema mismatch will break the scikit-learn pipeline. See `FINAL_MODEL_FEATURE_SPECIFICATION.md`.

## 4. Input Preprocessing
Do not write custom imputation or One-Hot Encoding logic in the backend API router. The provided `.joblib` pipelines inherently contain `SimpleImputer` and `OneHotEncoder` steps. Pass the 29 raw features straight into `pipeline.predict_proba()` or `pipeline.predict()`.

## 5. Required Endpoints & Outputs

### Filing-Time Classification Output
You must extract and return:
1. **Raw Probability**: From the XGBoost tree.
2. **Calibrated Probability**: (From Isotonic Wrapper).

### Risk Score & Band Output
Calculate the risk score strictly as:
`risk_score = floor(calibrated_probability * 100)`
Map the band strictly as:
- 0–20: Low
- 21–50: Moderate
- 51–80: High
- 81–100: Very High

### SHAP Output
Use `shap.TreeExplainer` on the raw XGBoost tree to extract local contribution weights, returning the top N conceptual features.

### Filing-Time Regression Output
Return the predicted `case_duration_days`. Warning logic must state that predictions heavily underpredict >5-year cases.

### Dataset C (Next-Listing Delay) Status
**ABORT / DO NOT BUILD.** This task yielded a negative experimental result (unpredictable out-of-time) and is banned from production endpoints.

## 6. Immutable Files (DO NOT CHANGE)
Do not alter any files in `research/`, `models/`, `src/ml/`, `src/risk/`, or `src/xai/`. The experimental state is mathematically frozen.

## 7. Running the Pipeline & Tests Locally
To verify the ML environment runs on your machine:
1. Install dependencies listed in `research/REPRODUCIBILITY.md`
2. Run tests: `PYTHONPATH=. pytest tests/ml/` (All 15 tests must pass).
