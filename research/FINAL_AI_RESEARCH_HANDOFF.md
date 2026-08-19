# Final AI/Research Handoff

## 1. Executive Summary
The AI/Research stream for JDIS has formally concluded. The data processing, baseline validation, advanced classification/regression, feature ablation, risk calibration, and XAI experiments have been executed according to strict out-of-sample temporal constraints. The filing-time classification model is approved for backend integration. The duration regression model and the hearing-delay module are documented as systematically underpredicting long-tail extreme variance and must be handled with stated limitations.

## 2. Final Models
- **Filing-Time Classifier (Production Ready)**: XGBoost + Isotonic Calibrator (`models/final_calibrated_clf.joblib`).
- **Filing-Time Regressor**: XGBoost Regressor (`models/best_ablation_reg.joblib`).

## 3. Final Metrics (2016 Test cohort)
- **Classification**: ROC-AUC = 0.7938 | PR-AUC = 0.6423 | F1 = 0.5157 | ECE = 0.0453
- **Regression**: MAE = 262.88 days | R² = -0.0887

## 4. Final Feature Set
Both models utilize **Config D**: Exactly 29 meta-features representing Case Basics, Case Type, Court Geography, Judge Demographics, and Historical Throughput. Full specification is available in `FINAL_MODEL_FEATURE_SPECIFICATION.md`.

## 5. Calibration
The classifier probabilities are wrapped in an Isotonic Regressor fitted on the 2015 cohort, ensuring strict empirical alignment. The raw outputs must not be used without passing through this wrapper.

## 6. Risk Score
The 0–100 integer score maps to:
- 0–20: Low Risk
- 21–50: Moderate Risk
- 51–80: High Risk
- 81–100: Very High Risk
*Specification in `RISK_SCORE_SPECIFICATION.md`.*

## 7. XAI (Explainable AI)
SHAP identifies structural Court identifiers (`court_no`), Case Types (`type_name`), and specific Filing Judges as the predominant drivers of risk scoring. These are associative, not causal, attributions.

## 8. Dataset C (Hearing Next-Listing) Result
**Negative Result.** The module achieved an R² of -1.70 out-of-time. Due to unobservable daily operational constraints, predicting the exact day gap between hearings using macro administrative data is structurally unfeasible. It will not be integrated into production.

## 9. Known Limitations
- Extreme long-tail delays (>5 years) are structurally underpredicted by regression.
- Models reflect historical throughput; they cannot foresee exogenous shocks (e.g., legislation changes, pandemic lockdowns, new judge appointments).

## 10. Backend Requirements
The backend API inference contract strictly expects the 29 input features formatted per `ML_INFERENCE_CONTRACT.md`. The pipeline will automatically handle median/constant imputation and One-Hot Encoding. 

## 11. Reproducibility
Random seeds (`42`) and specific pipeline scripts guarantee reproducibilty from raw DDL datasets to final evaluation, as documented in `REPRODUCIBILITY.md`. 15/15 unit tests pass locally.

## 12. Artifacts & Hand-Off Files
All final models reside in `models/`.
All final research summaries, tables, matrices, and limitations are centralized in `research/`.
All API schemas and backend specs are located in `docs/`.

**Research Freeze is Active. Proceed to Backend implementation.**
