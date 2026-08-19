# JDIS ML Experiment Register

This document tracks all machine learning experiments for the JDIS project.

> [!WARNING]
> Previous 2017 baseline classification experiments have been **INVALIDATED — RIGHT-CENSORING / SELECTION BIAS**. They are retained in history but must not be used for final evaluation.

| Experiment ID | Dataset | Prediction Point | Target | Feature Version | Temporal Split | Model | Validation Metric | Test Metric | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| REG-FIN-001 | Filing Regression | Filing | case_duration_days | TFIDF-SVD + Baseline | Train: 2010-2014, Val: 2015, Test: 2016 | Mean Predictor | Val MAE: 464.43 | Test MAE: 446.89 | Final |
| REG-FIN-002 | Filing Regression | Filing | case_duration_days | TFIDF-SVD + Baseline | Train: 2010-2014, Val: 2015, Test: 2016 | Median Predictor | Val MAE: 387.03 | Test MAE: 321.74 | Final |
| REG-FIN-003 | Filing Regression | Filing | case_duration_days | TFIDF-SVD + Baseline | Train: 2010-2014, Val: 2015, Test: 2016 | Linear Regression | Val MAE: 370.08 | Test MAE: 346.71 | Final |
| REG-FIN-004 | Filing Regression | Filing | case_duration_days | TFIDF-SVD + Baseline | Train: 2010-2014, Val: 2015, Test: 2016 | Decision Tree Regressor | Val MAE: 382.73 | Test MAE: 348.29 | Final |
| CLS-FIN-001 | Filing Classification 24m | Filing | delay_24m | TFIDF-SVD + Baseline | Train: 2010-2014, Val: 2015, Test: 2016 | Majority-class Predictor | Val F1: 0.0000 | Test F1: 0.0000 | Final |
| CLS-FIN-002 | Filing Classification 24m | Filing | delay_24m | TFIDF-SVD + Baseline (Sparse) | Train: 2010-2014, Val: 2015, Test: 2016 | Logistic Regression | Val F1: 0.4849 | Test F1: 0.4495 | Final |
| CLS-FIN-003 | Filing Classification 24m | Filing | delay_24m | TFIDF-SVD + Baseline (Sparse) | Train: 2010-2014, Val: 2015, Test: 2016 | Decision Tree Classifier | Val F1: 0.4736 | Test F1: 0.4042 | Final |
| CLS-ADV-001 | Filing Classification 24m | Filing | delay_24m | TFIDF-SVD + Baseline (Sparse) | Train: 2010-2014, Val: 2015, Test: 2016 | Random Forest Classifier | Pending | Pending | Proposed |
| CLS-ADV-002 | Filing Classification 24m | Filing | delay_24m | TFIDF-SVD + Baseline (Sparse) | Train: 2010-2014, Val: 2015, Test: 2016 | XGBoost Classifier | Pending | Pending | Proposed |
| CLS-ADV-003 | Filing Classification 24m | Filing | delay_24m | TFIDF-SVD + Baseline (Ordinal) | Train: 2010-2014, Val: 2015, Test: 2016 | LightGBM Classifier | Pending | Pending | Proposed |
| REG-ADV-001 | Filing Regression | Filing | case_duration_days | TFIDF-SVD + Baseline (Sparse) | Train: 2010-2014, Val: 2015, Test: 2016 | Random Forest Regressor | Pending | Pending | Proposed |
| REG-ADV-002 | Filing Regression | Filing | case_duration_days | TFIDF-SVD + Baseline (Sparse) | Train: 2010-2014, Val: 2015, Test: 2016 | XGBoost Regressor | Pending | Pending | Proposed |
| REG-ADV-003 | Filing Regression | Filing | case_duration_days | TFIDF-SVD + Baseline (Ordinal) | Train: 2010-2014, Val: 2015, Test: 2016 | LightGBM Regressor | Pending | Pending | Proposed |
| CLS-ADV-001 | 2026-08-18 | Final Advanced Classification | Filing 24m Dataset | delay_24m | Random Forest Classifier | Train: 2010-2014, Val: 2015 | Val F1: 0.5501 | Saved |
| CLS-ADV-002 | 2026-08-18 | Final Advanced Classification | Filing 24m Dataset | delay_24m | XGBoost Classifier | Train: 2010-2014, Val: 2015 | Val F1: 0.5563 | Saved |
| CLS-ADV-003 | 2026-08-18 | Final Advanced Classification | Filing 24m Dataset | delay_24m | LightGBM Classifier | Train: 2010-2014, Val: 2015 | Val F1: 0.5262 | Saved |
| REG-ADV-001 | 2026-08-18 | Final Advanced Regression | Filing Regression Dataset | case_duration_days | Random Forest Regressor | Train: 2010-2014, Val: 2015 | Val MAE: 310.40 | Saved |
| REG-ADV-002 | 2026-08-18 | Final Advanced Regression | Filing Regression Dataset | case_duration_days | XGBoost Regressor | Train: 2010-2014, Val: 2015 | Val MAE: 296.02 | Saved |
| REG-ADV-003 | 2026-08-18 | Final Advanced Regression | Filing Regression Dataset | case_duration_days | LightGBM Regressor | Train: 2010-2014, Val: 2015 | Val MAE: 398.13 | Saved |
| ABL-CLS-D | 2026-08-18 | Feature Ablation (Config D) | Filing 24m Dataset | delay_24m | XGBoost Classifier | Train: 2010-2014, Val: 2015, Test: 2016 | Val PR-AUC: 0.6900 | Test PR-AUC: 0.6423 | Final |
| ABL-REG-D | 2026-08-18 | Feature Ablation (Config D) | Filing Regression | case_duration_days | XGBoost Regressor | Train: 2010-2014, Val: 2015, Test: 2016 | Val MAE: 294.43 | Test MAE: 262.88 | Final |
