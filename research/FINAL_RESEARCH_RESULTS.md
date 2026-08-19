# Final JDIS Research Results (Authoritative)

This document consolidates the final, validated results for the JDIS predictive modeling phase. It relies exclusively on the corrected temporal methodology that handles historical right-censoring.

---

## 1. Primary Filing-Time Delay Classification

- **Experiment Name**: Final Filing-Time 24-Month Delay Classification (Phase 5)
- **Dataset**: `filing_classification_24m_final.parquet`
- **Prediction Point**: Case Filing ($T_{\text{filing}}$)
- **Target**: `delay_24m` ($\mathbb{I}(\text{duration} > 730.5\text{ days})$). Unresolved/censored cases not demonstrably crossing the threshold are excluded.
- **Train Period**: 2010–2014
- **Validation Period**: 2015
- **Test Period**: 2016
- **Selected Model**: XGBoost Classifier (Config D: 29 Features) + Isotonic Calibration
- **Exact Metric Values (2016 Test)**:
  - Accuracy: 0.7346
  - Precision: 0.6724
  - Recall: 0.4183
  - F1-Score: 0.5157
  - ROC-AUC: 0.7938
  - PR-AUC: 0.6423
  - Brier Score: 0.1734
  - ECE: 0.0453
- **Interpretation**: The model successfully identifies high-risk cases at filing, providing strong discriminative power (ROC-AUC ~0.79) without relying on look-ahead bias. The probabilities are highly calibrated via Isotonic Regression, enabling strict risk banding.
- **Limitations**: Predictions are associational, capturing historical patterns of court/judge throughput and case types. They do not account for external shocks, procedural micro-details, or individual case merits.

---

## 2. Primary Filing-Time Duration Regression

- **Experiment Name**: Final Filing-Time Duration Regression (Phase 4)
- **Dataset**: `filing_regression_final.parquet`
- **Prediction Point**: Case Filing ($T_{\text{filing}}$)
- **Target**: `case_duration_days`
- **Train Period**: 2010–2014
- **Validation Period**: 2015
- **Test Period**: 2016
- **Selected Model**: XGBoost Regressor (Config D: 29 Features)
- **Exact Metric Values (2016 Test)**:
  - MAE: 262.88 days
  - RMSE: 324.07 days
  - R²: -0.0887
- **Interpretation**: The exact day-level duration of a case is difficult to predict precisely due to severe long-tail variance. While MAE improves upon simple baselines, the negative R² indicates that extreme outliers heavily skew the variance penalty.
- **Limitations**: The model systematically underpredicts extreme outliers (>5 years) due to standard MSE optimization compressing the extreme tail.

---

## 3. Hearing Continuation & Next-Listing Delay

- **Experiment Name**: Next-Listing Delay Prediction (Dataset C / Phase 6)
- **Dataset**: `hearing_features.parquet`
- **Prediction Point**: Most recent active hearing ($T_{\text{last\_list}}$)
- **Target**: `next_listing_gap_days` (`date_next_list - date_last_list`)
- **Train Period**: `last_list_year` $\le$ 2017
- **Validation Period**: `last_list_year` == 2018
- **Test Period**: `last_list_year` == 2019
- **Selected Model**: Random Forest Regressor
- **Exact Metric Values (2019 Test)**:
  - MAE: 31.27
  - RMSE: 39.20
  - R²: -1.7032
- **Interpretation**: The tested case-level and historical metadata features were insufficient to produce useful out-of-time prediction of exact next-listing delay. The model systematically failed to outperform historical mean predictors.
- **Limitations**: This is an evaluated research module yielding a negative experimental result. Unobserved micro-operational constraints (e.g., lawyer diary clashes) dominate this target. It is not approved for production prediction.
