# Final ML Handoff to Backend (Namdeo)

This document specifies the implementation-ready architecture for the backend integration.

## 1. Primary Filing-Time Classification Endpoint

### Input
The endpoint must receive a vector containing the exact 29 model features (Config D) specified in `FINAL_MODEL_FEATURE_SPECIFICATION.md`.

### Processing
1. Pass input through the saved scikit-learn `Pipeline`.
2. Pipeline performs `SimpleImputer(strategy='median')` on numeric features.
3. Pipeline performs `SimpleImputer(strategy='constant', fill_value='missing')` followed by `OneHotEncoder(handle_unknown='ignore')` on categorical features.
4. Pass transformed vector to XGBoost classifier.
5. Pass XGBoost output probability through Isotonic Regressor wrapper.

### Output
- `raw_probability`: Float (0.0 to 1.0)
- `calibrated_probability`: Float (0.0 to 1.0)
- `risk_score`: Integer (0 to 100) calculated as `floor(calibrated_probability * 100)`
- `risk_band`: String enum ('Low', 'Moderate', 'High', 'Very High') based on score.
- `model_version`: String ID.

### Explanation
Returns the top SHAP contributing categories (e.g. `type_name`, `ddl_filing_judge_id`).

---

## 2. Filing-Time Duration Regression Endpoint

### Input
Exact 29 model features (Config D).

### Processing
Identical pipeline preprocessing applied to the trained XGBoost Regressor.

### Output
- `predicted_duration_days`: Integer
- `limitations_flag`: String indicating "Systematically underpredicts extreme outliers (>5 years)."

---

## 3. Dataset C (Next-Listing Delay)

**Research-only negative result. Not exposed as production prediction.**
Do not build an endpoint for next-listing delay. The models failed to predict the metric out-of-time reliably due to unobservable operational variables.
