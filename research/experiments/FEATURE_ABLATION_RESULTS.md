# JDIS Phase 4: Feature Ablation Results

This document presents the findings from the Phase 4 Feature-Group Ablation Study. The XGBoost configuration selected in Phase 3 was trained iteratively on cumulative feature groups (Train: 2010–2014) and evaluated (Validation: 2015).

## 1. Classification Results (Target: `delay_24m`)

| Config | Groups Included | Feature Count | PR-AUC | ΔPR-AUC | ROC-AUC | ΔROC-AUC | F1 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **A** | Basic | 15 | 0.6667 | - | 0.7811 | - | 0.5506 |
| **B** | Basic+Court | 21 | 0.6845 | +0.0177 | 0.7908 | +0.0096 | 0.5602 |
| **C** | Basic+Court+Judge | 25 | 0.6880 | +0.0034 | 0.7934 | +0.0026 | 0.5674 |
| **D (Best)** | Basic+Court+Judge+Historical | 29 | **0.6900** | **+0.0019** | **0.7964** | **+0.0030** | 0.5467 |
| **E** | Basic+...+Historical+NLP | 79 | 0.6842 | -0.0057 | 0.7869 | -0.0094 | 0.5574 |
| **F** | All + Graph | 81 | 0.6848 | +0.0005 | 0.7874 | +0.0005 | 0.5562 |

## 2. Regression Results (Target: `case_duration_days`)

| Config | Groups Included | Feature Count | MAE | ΔMAE | RMSE | ΔRMSE | R² |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **A** | Basic | 15 | 344.90 | - | 420.46 | - | 0.0546 |
| **B** | Basic+Court | 21 | 344.63 | -0.26 | 420.03 | -0.42 | 0.0565 |
| **C** | Basic+Court+Judge | 25 | 342.18 | -2.45 | 416.43 | -3.60 | 0.0726 |
| **D (Best)** | Basic+Court+Judge+Historical | 29 | **294.43** | **-47.74** | **370.76** | **-45.66** | **0.2648** |
| **E** | Basic+...+Historical+NLP | 79 | 295.04 | +0.61 | 374.21 | +3.44 | 0.2511 |
| **F** | All + Graph | 81 | 295.62 | +0.58 | 374.35 | +0.14 | 0.2506 |

## 3. Final Test Evaluation (2016 Cohort)
To avoid selection bias, only Config **D** (the best validation model for both tasks) was evaluated on the strictly isolated 2016 Test cohort.
- **Classification Test PR-AUC**: `0.6423`
- **Regression Test MAE**: `262.88`

---

## 4. Required Interpretation

### 1. Which feature group contributes the largest improvement?
* **Classification**: Group B (Court Features) contributed the largest incremental gain (+0.0177 PR-AUC). Jurisdiction shows a strong predictive association with baseline delay risk in classification.
* **Regression**: Group D (Historical Features) contributed the massive largest gain, reducing the absolute MAE by ~47.74 days.

### 2. Do judge features help?
Yes, modestly. Adding Group C (Judge Features) yielded an incremental predictive gain of +0.0034 PR-AUC and reduced Regression MAE by 2.45 days.

### 3. Do court features help?
Yes. Group B (Court Features) drove the largest classification jump (+0.0177 PR-AUC), confirming that the specific court establishment is highly predictive of severe (>24m) delays.

### 4. Do historical features help?
Yes, exceptionally so for exact duration prediction. Group D reduced the MAE by an incredible 47 days, suggesting that the expanding-window throughput and backlog characteristics of a court right before filing show a strong predictive association with how long the case will take.

### 5. Does legal metadata/NLP help?
No. Introducing the high-dimensional TF-IDF vectors (Group E) actually degraded both PR-AUC (-0.0057) and MAE (+0.61 days). Without heavy specialized tuning or denser representations (like BERT), the raw TF-IDF components inject sparsity and noise into the tree builder.

### 6. Do graph features add incremental value?
No. Introducing Group F (`judge_court_degree`, `court_judge_turnover_count`) yielded negligible to negative predictive gain (+0.0005 PR-AUC, +0.58 days MAE). It appears that judge and court throughput historicals already encapsulate this operational variance.

### 7. Is XGBoost still the strongest model when feature groups are restricted?
Yes. Even Config A (just 15 basic case features) achieved a Validation PR-AUC of 0.6667. This significantly outperforms the Logistic Regression baseline (0.6274 PR-AUC using all features) from Phase 3, demonstrating XGBoost's structural non-linear advantage even under severe feature restriction.

### 8. Are any feature groups redundant?
Yes. Groups E (NLP) and F (Graph) are effectively redundant or harmful. The dataset achieves maximum validation performance (Config D) using only Basic Case, Court, Judge, and Historical Throughput features.
