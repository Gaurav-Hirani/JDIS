# JDIS PHASE 3 PROVENANCE AUDIT

## 1. Classification Models (delay_24m)

### CLS-ADV-001
- **Artifact:** `models/CLS-ADV-001.joblib`
- **Model Type:** RandomForestClassifier
- **Actual Parameters:** `n_estimators`: 100, `max_depth`: 15, `min_samples_leaf`: 5, `random_state`: 42
- **Preprocessing:** Sparse One-Hot Encoder (`['imputer', 'onehot']`)
- **Reported Metric Source:** `research/results/advanced_model_comparison_classification_val.csv`
- **Validation Dataset:** 2015 Cohort
- **Consistency Status:** Consistent

### CLS-ADV-002 (Selected Best Model)
- **Artifact:** `models/CLS-ADV-002.joblib`
- **Model Type:** XGBClassifier
- **Actual Parameters:** `n_estimators`: 200, `max_depth`: 6, `learning_rate`: 0.1, `random_state`: 42
- **Preprocessing:** Sparse One-Hot Encoder (`['imputer', 'onehot']`)
- **Reported Metric Source:** `research/results/advanced_model_comparison_classification_val.csv` (Val) and `research/results/final_model_test_results.csv` (Test)
- **Validation/Test Dataset:** 2015 Cohort (Val), 2016 Cohort (Test)
- **Consistency Status:** Consistent

### CLS-ADV-003
- **Artifact:** `models/CLS-ADV-003.joblib`
- **Model Type:** LGBMClassifier
- **Actual Parameters:** `n_estimators`: 200, `max_depth`: 6, `learning_rate`: 0.1, `random_state`: 42
- **Preprocessing:** Ordinal Encoder (`['imputer', 'ordinal']`)
- **Reported Metric Source:** `research/results/advanced_model_comparison_classification_val.csv`
- **Validation Dataset:** 2015 Cohort
- **Consistency Status:** Consistent

## 2. Regression Models (case_duration_days)

### REG-ADV-001
- **Artifact:** `models/REG-ADV-001.joblib`
- **Model Type:** RandomForestRegressor
- **Actual Parameters:** `n_estimators`: 100, `max_depth`: 15, `min_samples_leaf`: 5, `random_state`: 42
- **Preprocessing:** Sparse One-Hot Encoder (`['imputer', 'onehot']`)
- **Reported Metric Source:** `research/results/advanced_model_comparison_regression_val.csv`
- **Validation Dataset:** 2015 Cohort
- **Consistency Status:** Consistent

### REG-ADV-002 (Selected Best Model)
- **Artifact:** `models/REG-ADV-002.joblib`
- **Model Type:** XGBRegressor
- **Actual Parameters:** `n_estimators`: 200, `max_depth`: 6, `learning_rate`: 0.1, `random_state`: 42
- **Preprocessing:** Sparse One-Hot Encoder (`['imputer', 'onehot']`)
- **Reported Metric Source:** `research/results/advanced_model_comparison_regression_val.csv` (Val) and `research/results/final_model_test_results.csv` (Test)
- **Validation/Test Dataset:** 2015 Cohort (Val), 2016 Cohort (Test)
- **Consistency Status:** Consistent

### REG-ADV-003
- **Artifact:** `models/REG-ADV-003.joblib`
- **Model Type:** LGBMRegressor
- **Actual Parameters:** `n_estimators`: 200, `max_depth`: 6, `learning_rate`: 0.1, `random_state`: 42
- **Preprocessing:** Ordinal Encoder (`['imputer', 'ordinal']`)
- **Reported Metric Source:** `research/results/advanced_model_comparison_regression_val.csv`
- **Validation Dataset:** 2015 Cohort
- **Consistency Status:** Consistent

## 3. Language & Documentation
The language in `ADVANCED_MODEL_RESULTS_REPORT.md` has been verified and updated. The phrase "statistically significant improvement", which implies formal statistical hypothesis testing that was not performed, was corrected to "predictive improvement" to meet rigorous academic standards. 

## PHASE 3 STATUS
- VERIFIED
