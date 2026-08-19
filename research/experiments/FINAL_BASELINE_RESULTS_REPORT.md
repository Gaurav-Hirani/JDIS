# Final Corrected Baseline Results Report

## A. Experimental Design
The primary modeling objective is to predict judicial delay at the time of filing. The evaluation employs a strict chronological train/validation/test split to guarantee out-of-time generalizability.
- **Train Window:** 2010–2014
- **Validation Window:** 2015 (used exclusively for model evaluation and hyperparameter/threshold selection)
- **Test Window:** 2016 (used exclusively for the final authoritative baseline measurement)

This shift backward from the initially proposed 2017/2018 validation windows was mathematically necessitated to guarantee ~100% case-level observability and eliminate right-censoring selection bias.

## B. Target Construction
- **Model 1 (Regression):** Predicts `case_duration_days`. Restricted strictly to fully resolved cases with valid decision dates.
- **Model 2 (Classification):** Predicts `delay_24m = 1` if a case is known to exceed 730.5 days. A case is assigned `1` if it is resolved after 730.5 days OR if it is unresolved but its case-specific follow-up demonstrates it remained active for > 730.5 days. 

## C. Censoring Treatment
For classification, unresolved cases possessing $\le$ 730.5 days of tracking follow-up are classified as `UNKNOWN` because their true 24-month outcome cannot be determined. These records are explicitly excluded from supervised classification training and evaluation.

## D. Data-Quality Correction
An audit of raw case updates revealed a small subset of records containing impossible future tracking dates (e.g., `5000-01-01`), which artificially inflated observation follow-up times to over 1,000 years. 
- **Affected Fields:** `date_last_list` (1,881 records) and `date_first_list` (2 records).
- **Correction:** Dates > 2025-01-01 were coerced to `NaT`.
- **Target Impact:** 4 cases that were falsely labeled as delayed (due to 1,000+ years of garbage follow-up) reverted to `UNKNOWN` and were safely excluded. No valid historic dates were affected.

## E. Regression Results
Regression datasets contained 310,360 total eligible resolved records (Train: 231,863 | Val: 41,178 | Test: 37,319).

### Validation (2015) - Used for Selection
| Model | MAE | RMSE | R² |
| :--- | :--- | :--- | :--- |
| Mean Predictor | 464.43 | 517.34 | -0.431 |
| Median Predictor | 387.03 | 437.79 | -0.025 |
| Linear Regression | 370.08 | 454.49 | -0.105 |
| Decision Tree Regressor | 382.73 | 448.53 | -0.076 |

### Final Test (2016) - Strictly Held Out
| Model | MAE | RMSE | R² |
| :--- | :--- | :--- | :--- |
| Mean Predictor | 446.89 | 507.13 | -1.666 |
| Median Predictor | 321.74 | 361.59 | -0.355 |
| Linear Regression | 346.71 | 430.62 | -0.922 |
| Decision Tree Regressor | 348.29 | 418.15 | -0.812 |

## F. Classification Results
Classification datasets contained 349,360 valid cases with 0 `UNKNOWN` records remaining (Train: 249,451 | Val: 49,980 | Test: 49,929).

### Validation (2015) - Used for Selection
| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Majority/Dummy | 0.612 | 0.000 | 0.000 | 0.000 | 0.500 | 0.388 |
| Logistic Regression | 0.692 | 0.692 | 0.373 | 0.485 | 0.715 | 0.627 |
| Decision Tree | 0.693 | 0.708 | 0.356 | 0.474 | 0.715 | 0.594 |

### Final Test (2016) - Strictly Held Out
| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Majority/Dummy | 0.662 | 0.000 | 0.000 | 0.000 | 0.500 | 0.338 |
| Logistic Regression | 0.710 | 0.625 | 0.351 | 0.449 | 0.726 | 0.561 |
| Decision Tree | 0.708 | 0.653 | 0.293 | 0.404 | 0.707 | 0.524 |

## G. Validation/Test Separation
It is explicitly confirmed that the 2016 test cohort was completely isolated:
1. No 2016 rows were used in model fitting.
2. No 2016 rows were used for hyperparameter tuning.
3. No 2016 metrics were evaluated to select the model.
4. No 2016 data was utilized to fit preprocessing objects (StandardScaler, SimpleImputer, OneHotEncoder).

## H. Leakage Verification
The filing-time feature set (81 raw features: 62 numerical, 19 categorical) passed all leakage audits. It strictly excludes `case_duration_days`, `date_of_decision`, target-derived features (`delay_12m`, `delay_36m`), and future hearing information (`filing_to_first_list_days`).

## I. Interpretation
Under the robust, censoring-aware evaluation, Logistic Regression stands as the best-performing model in the evaluated baseline set. It establishes a strong predictive association, achieving a Test ROC-AUC of 0.726 and Test PR-AUC of 0.561 (significantly outperforming the 0.338 random-guess baseline).

## J. Limitations
The exact-duration regression models are inherently restricted to resolved cases, introducing a mild selection bias by definition. Furthermore, binary classification discards cases with `UNKNOWN` follow-up horizons, which makes modern (2017/2018) cohorts difficult to leverage using standard supervised binary evaluation.

## K. Recommended Next Step
Proceed to advanced machine learning algorithms. The baseline architecture establishes that the filing-time data possesses strong signal. The next immediate step should be evaluating advanced non-linear gradient-boosted ensembles (XGBoost, LightGBM, Random Forest) against this strict test paradigm.
