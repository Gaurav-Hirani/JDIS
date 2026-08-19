# JDIS Phase 5: XAI & Risk Analysis Handoff

## 1. Final Model Artifacts
- **Feature Specification**: Config D (29 Features: Basic, Court, Judge, Historical)
- **Classification Model**: `models/final_calibrated_clf.joblib` (XGBoost + Isotonic Calibration). *Note: The calibrator was fitted on the 2015 validation set. Final out-of-sample calibration metrics were strictly evaluated on the 2016 test set.*
- **Regression Model**: `models/best_ablation_reg.joblib` (XGBoost)

## 2. Risk Score Architecture
- **Formula**: `risk_score = floor(calibrated_probability * 100)`
- **Bands**:
  - Low: 0 - 20
  - Moderate: 21 - 50
  - High: 51 - 80
  - Very High: 81 - 100
- **Implementation**: `src/risk/risk_score.py`

## 3. Explainability (SHAP)
SHAP artifacts generated successfully for both global feature importance and 6 representative local test cases (High/Medium/Low risk, TP, FP, FN). 
- Global CSV: `research/results/shap_classification_global.csv`
- Local Plots: `research/figures/shap_local/`

## 4. Error Analysis
Systematic error analysis confirms that the model generalizes robustly but struggles predictably with extreme duration outliers (regression underprediction for >5 yr cases) and borderline false positives.
- Classification Error CSV: `research/results/error_analysis_classification.csv`
- Regression Error CSV: `research/results/error_analysis_regression.csv`

## 5. Next Steps
Phase 5 is complete. The system is fully evaluated, calibrated, and explained. We are now ready to hand off to human review before proceeding to the deployment or next-listing phases.
