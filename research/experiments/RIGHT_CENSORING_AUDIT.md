# Right-Censoring & Outcome Observability Audit

## 1. Dataset Observation Window
By examining the raw dates in the dataset, the exact observational timeline was measured:
*   **Earliest filing date:** 2010-01-01
*   **Latest filing date:** 2018-12-31
*   **Earliest decision date:** 2010-01-01
*   **Latest decision date:** 2020-09-15
*   **Latest hearing date (`date_next_list`):** 2022-01-08

**Apparent dataset endpoint:** 2022-01-08.
Because decisions and hearings are recorded up to early 2022, a case filed on the very last day of 2018 (2018-12-31) has exactly 1,104 days (just over 36 months) of follow-up observation time.

## 2. Case Observability & Censoring Analysis
*   **Rule for 12m Delay:** If unresolved, but censoring time > 365 days, outcome is **known delayed**.
*   **Rule for 24m Delay:** If unresolved, but censoring time > 730 days, outcome is **known delayed**.
*   **Rule for 36m Delay:** If unresolved, but censoring time > 1095 days, outcome is **known delayed**.

**Conclusion:** Because the dataset endpoint (2022-01-08) is more than 36 months after the latest filing date (2018-12-31), **there is zero right-censoring before 36 months**. Every single unresolved case in the 2010–2018 dataset is guaranteed to have been pending for >36 months. Therefore, **all unresolved records are valid, known positives for 12m, 24m, and 36m delay classifications.**

## 3. Rebuilt Yearly Distribution (Right-Censoring Taxonomy)
*(See `research/results/right_censoring_audit.csv` for full raw numbers)*

| Year | Total Cases | Resolved | Unresolved (Censored) | Valid 24m Label | Censored Before 24m | True Delayed 24m % |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **2010** | 49,867 | 48,501 | 1,366 | 49,867 | 0 | 48.27% |
| **2011** | 49,892 | 47,764 | 2,128 | 49,892 | 0 | 47.44% |
| **2012** | 49,911 | 47,181 | 2,730 | 49,911 | 0 | 41.36% |
| **2013** | 49,949 | 45,167 | 4,782 | 49,949 | 0 | 37.73% |
| **2014** | 49,836 | 43,250 | 6,586 | 49,836 | 0 | 36.21% |
| **2015** | 49,982 | 41,178 | 8,804 | 49,982 | 0 | 38.80% |
| **2016** | 49,930 | 37,319 | 12,611 | 49,930 | 0 | 33.79% |
| **2017** | 49,913 | 33,227 | 16,686 | 49,913 | 0 | 34.36% |
| **2018** | 49,986 | 25,911 | 24,075 | 49,986 | 0 | 48.21% |

## 4. Valid Temporal Evaluation Windows
| Target         | Earliest valid year | Latest valid year | Reason |
| -------------- | ------------------- | ----------------- | ------ |
| Duration       | 2010                | 2018              | Requires survival analysis / censoring models for unresolved cases. |
| 12-month delay | 2010                | 2018              | 100% observability. All cases have >12m follow-up. |
| 24-month delay | 2010                | 2018              | 100% observability. All cases have >24m follow-up. |
| 36-month delay | 2010                | 2018              | 100% observability. All cases have >36m follow-up. |

## 5. Comparison of Methodologies

**Approach A — Eligibility-window classification**
*   **Sample size:** 449,266 cases (100% of data).
*   **Advantages:** Because we have >36m observation time for all filing years, we can deterministically label all unresolved cases as `delay=1`. This completely fixes the selection bias, restores class balance, and allows us to use standard classification algorithms without losing a single record.
*   **Disadvantages:** Only solves classification; cannot predict the continuous duration of unresolved cases.

**Approach B — Survival analysis**
*   **Advantages:** Natively handles right-censoring for continuous time-to-event modeling.
*   **Disadvantages:** Requires specialized models (Cox PH, Random Survival Forests) which depart from standard classification workflows. 

**Approach C — Fully observed resolved-only cohort**
*   **Advantages:** Simplistic.
*   **Disadvantages:** Fatally flawed for recent years. Creates severe selection bias by artificially suppressing delay rates (plunging 2017 delay to 1.39%).

## 6. Recommended Research Strategy
*   **Primary 24-month classification methodology:** **Approach A**. We must impute `delay_24m = 1` for all unresolved cases since our observability window proves they all exceeded 24 months. 
*   **Primary duration methodology:** Survival Analysis (Approach B) should be explored if continuous regression remains a strict requirement, otherwise treat the system primarily as a binary delay classification system.
*   **Recommended Temporal Split:** Train (2010–2016), Validation (2017), Test (2018). This split remains scientifically robust once the labels are correctly imputed.

## 7. Existing Pipeline & Implications
**Code Path Identification:**
In `src/features/build_features.py`, the target is constructed as:
`delay_24m = 1 if case_duration_days > 730.5 else 0`. Because `case_duration_days` is NaN for unresolved cases, `delay_24m` evaluates to NaN for 79,768 records. 
Subsequently, the baseline ML training scripts (`src/ml/run_baselines.py` and `src/ml/run_classification_baselines.py`) explicitly ran:
`df = df[df["case_duration_days"].notna() & (df["case_duration_days"] >= 0)].copy()`
which dropped all these true positives prior to training.

**Crucial Statement:**
> The existing 2017 baseline classification results are invalid for final research evaluation because the validation cohort was affected by right-censoring.
