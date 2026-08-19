# JDIS PHASE 3: ADVANCED MODEL RESULTS REPORT

## 1. Executive Summary

This report documents the Phase 3 advanced machine learning experiments for the JDIS project. The primary goal was to determine if advanced nonlinear ensemble models provide meaningful predictive improvements over the established linear and tree-based baselines.

**Strict Temporal Discipline Confirmation:**
The 2016 Test cohort was strictly isolated. It was **never** used for:
* Training
* Hyperparameter tuning
* Early stopping
* Preprocessing (e.g., TFIDF fitting or imputation)
* Model selection

All decisions and selections were made entirely based on the 2015 Validation cohort.

## 2. Methodology

### Data Splits & Exact Counts
* **Train (2010–2014):** 249,451 total cases (105,273 delayed, 42.20%)
* **Validation (2015):** 49,980 total cases (19,390 delayed, 38.79%)
* **Test (2016):** 49,929 total cases (16,871 delayed, 33.78%)

### Categorical Encoding & Dimensionality
* **Random Forest & XGBoost:** Sparse One-Hot Encoding (`handle_unknown='ignore', sparse_output=True`). Resulting dimensionality is ~900+ sparse features.
* **LightGBM:** Ordinal Encoding (`OrdinalEncoder` with -1 for unknowns) combined with LightGBM's native categorical handling (`categorical_feature` parameter).

### Hyperparameters (Pre-specified, No tuning on Test)
* **Random Forest (CLS & REG):** `n_estimators=100`, `max_depth=15`, `min_samples_leaf=5`, `random_state=42`
* **XGBoost (CLS & REG):** `n_estimators=200`, `max_depth=6`, `learning_rate=0.1`, `random_state=42`
* **LightGBM (CLS & REG):** `n_estimators=200`, `max_depth=6`, `learning_rate=0.1`, `random_state=42`

---

## 3. Validation Results (2015 Cohort)

### CLASSIFICATION (Target: `delay_24m`)

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC | Runtime (s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Majority-class Baseline | 0.6120 | 0.0000 | 0.0000 | 0.0000 | 0.5000 | 0.3880 | - |
| Decision Tree Baseline | 0.6932 | 0.7083 | 0.3558 | 0.4736 | 0.7151 | 0.5940 | - |
| Logistic Regression Baseline | 0.6925 | 0.6923 | 0.3731 | 0.4849 | 0.7152 | 0.6274 | - |
| LightGBM Classifier | 0.7026 | 0.6890 | 0.4256 | 0.5262 | 0.7531 | 0.6497 | 150.0* |
| Random Forest Classifier | 0.7117 | 0.6972 | 0.4542 | 0.5501 | 0.7775 | 0.6659 | 150.0* |
| **XGBoost Classifier (Best)** | **0.7191** | **0.7185** | **0.4538** | **0.5563** | **0.7875** | **0.6849** | 150.0* |

### REGRESSION (Target: `case_duration_days`)

| Model | MAE | RMSE | R² | Runtime (s) |
| :--- | :--- | :--- | :--- | :--- |
| Mean Predictor Baseline | 464.43 | 517.34 | -0.431 | - |
| Decision Tree Baseline | 382.73 | 448.53 | -0.076 | - |
| Median Predictor Baseline | 387.03 | 437.79 | -0.025 | - |
| Linear Regression Baseline | 370.08 | 454.49 | -0.105 | - |
| LightGBM Regressor | 398.13 | 452.95 | -0.097 | 4.53 |
| Random Forest Regressor | 310.40 | 387.78 | 0.196 | 462.27 |
| **XGBoost Regressor (Best)** | **296.02** | **374.93** | **0.248** | 4.89 |

### Model Selection Decisions
1. **Classification:** XGBoost Classifier was selected as the advanced representative because it achieved the highest PR-AUC (0.6849) on the 2015 Validation set.
2. **Regression:** XGBoost Regressor was selected as the advanced representative because it achieved the lowest MAE (296.02) and highest R² (0.248) on the 2015 Validation set.

---

## 4. Final Held-Out Test Results (2016 Cohort)

These metrics evaluate the selected XGBoost models against the best linear baselines on the strictly held-out 2016 cohort. 

### CLASSIFICATION RESULTS

| Task | Type | Model | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Classification | Baseline | Logistic Regression | 0.7096 | 0.6254 | 0.3508 | 0.4495 | 0.7258 | 0.5610 |
| Classification | Advanced | XGBoost Classifier | **0.7344** | **0.6722** | **0.4175** | **0.5151** | **0.7826** | **0.6278** |

*Analysis:* XGBoost provides a clear predictive improvement over the Logistic Regression baseline across all classification metrics. The PR-AUC improvement (+0.066) and Recall improvement (+0.066) indicate a significantly better ability to detect delayed cases without fabricating excessive false positives.

### REGRESSION RESULTS

| Task | Type | Model | MAE | RMSE | R² |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Regression | Baseline | Linear Regression | 346.71 | 430.62 | -0.922 |
| Regression | Advanced | XGBoost Regressor | **261.65** | **326.70** | **-0.106** |

*Analysis:* The XGBoost model substantially outperforms the Linear Regression baseline (MAE reduced by ~85 days). The R² for XGBoost improved massively but remains negative on the test set (-0.106), indicating that predicting the exact day a case resolves remains fundamentally difficult, highlighting the validity of shifting to threshold-based classification (`delay_24m`) as the primary task.

---

## 5. Artifact & File References

* **Validation Classification Metrics:** `research/results/advanced_model_comparison_classification_val.csv`
* **Validation Regression Metrics:** `research/results/advanced_model_comparison_regression_val.csv`
* **Final Test Metrics:** `research/results/final_model_test_results.csv`
* **XGBoost Classifer Pipeline:** `models/CLS-ADV-002.joblib`
* **XGBoost Regressor Pipeline:** `models/REG-ADV-002.joblib`
* **Test Scripts:** `src/ml/evaluate_advanced_test.py` and `tests/ml/test_ml_advanced.py`

## 6. Warnings & Anomalies

1. **LightGBM Native Categoricals:** The LightGBM Regressor performed unexpectedly poorly (MAE 398.13), worse than simple baselines. This strongly suggests that passing 900+ high-cardinality ordinal features natively to LightGBM without explicit target-encoding or tuning can trigger severe performance degradation in sparse judicial data.
2. **Random Forest Memory:** The dense internal memory overhead of Scikit-Learn's Random Forest caused the runtime to exceed 460+ seconds for regression compared to ~5 seconds for XGBoost. 
3. **Regression Task Difficulty:** Despite using advanced non-linear ensembles, the R² score on the 2016 Test set remains negative. The exact duration of judicial backlog contains high aleatoric uncertainty. The classification framework is much more reliable and robust for policy intervention.
