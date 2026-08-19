# Final Model Card: JDIS Predictive System

## 1. Primary Filing-Time Delay Classification Model
- **Model Type**: XGBoost Classifier with Isotonic Probability Calibration
- **Exact Artifact Path**: `models/final_calibrated_clf.joblib`
- **Target**: `delay_24m` (Binary: 1 if `case_duration_days` > 730.5)
- **Prediction Point**: Case Filing ($T_{\text{filing}}$)
- **Training Period**: Filing Years 2010–2014
- **Validation Period**: Filing Year 2015 (Used to fit the calibrator and select hyperparameters)
- **Test Period**: Filing Year 2016 (Strict out-of-sample evaluation)
- **Final Metrics (2016 Test)**:
  - ROC-AUC: 0.7938
  - PR-AUC: 0.6423
  - F1-Score: 0.5157
  - Brier Score: 0.1734
  - ECE: 0.0453
- **Calibration Method**: Isotonic Regression wrapper on XGBoost probabilities.
- **Risk-Score Mapping**: `floor(calibrated_probability * 100)` -> mapped to Low (0-20), Moderate (21-50), High (51-80), Very High (81-100).
- **Exact Feature Specification**: Config D (29 Features). Includes Case Basics, Case Type, Court Geography, Judge Demographics, and Historical Throughput.
- **Preprocessing**: Median imputation for numerics; One-Hot Encoding (`handle_unknown='ignore'`) for categoricals.
- **Known Limitations**: Predictions are associational patterns of historical throughput, not deterministic limits on individual case merit. Cannot foresee future external disruptions.

---

## 2. Filing-Time Duration Regression Model
- **Model Type**: XGBoost Regressor
- **Exact Artifact Path**: `models/best_ablation_reg.joblib`
- **Target**: `case_duration_days`
- **Prediction Point**: Case Filing ($T_{\text{filing}}$)
- **Training Period**: Filing Years 2010–2014
- **Validation Period**: Filing Year 2015
- **Test Period**: Filing Year 2016
- **Final Metrics (2016 Test)**:
  - MAE: 262.88 days
  - RMSE: 324.07 days
  - R²: -0.0887
- **Exact Feature Specification**: Config D (29 Features)
- **Known Limitations**: Systematically underpredicts long-tail outliers (cases taking >5 years) due to MSE variance compression.

---

## 3. Next-Listing Delay Model (Dataset C)
- **Status**: **Research-Only Negative Result.**
- **Artifact Path**: `models/final_hearing_model.joblib`
- **Model Type**: Random Forest Regressor
- **Target**: `next_listing_gap_days`
- **Test Metric (2019)**: R² = -1.7032
- **Known Limitations**: Out-of-time prediction is fundamentally inadequate. Micro-temporal scheduling cannot be consistently predicted from administrative metadata. **NOT FOR PRODUCTION EXPOSURE.**
