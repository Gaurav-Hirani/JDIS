# Final Temporal Design Methodology

This document serves as the authoritative methodology guide for the experimental temporal design of the JDIS ML modeling pipeline, developed to resolve historical right-censoring bias found in standard dataset subsets.

## The Right-Censoring Problem
During preliminary analysis, unresolved cases (those without a recorded decision date) were indiscriminately dropped prior to modeling. Because a static dataset inherently censors cases closer to the collection date, dropping unresolved cases from recent years artificially suppresses the apparent positive rate of long-term delays.

For example, cases filed in 2017 that eventually take 3 years to resolve were still "unresolved" when the dataset was extracted. Dropping them artificially plunged the 24-month delay rate of the 2017 validation set from an expected ~34% down to just 1.39%.

## The Observability Rule
To restore validity, the evaluation requires a strict case-level observability rule:
**An unresolved case is only labeled as delayed if its individual tracking history proves it remained active beyond the target threshold.**

If an unresolved case lacks sufficient follow-up to prove it crossed the 24-month mark, its outcome is `UNKNOWN` and it is explicitly excluded from supervised classification.

### Data-Quality Correction: Impossible Future Dates
During evaluation, it was discovered that a small subset of cases contained impossible future dates in their tracking records (e.g., `date_last_list = '5000-01-01'`). These garbage dates artificially inflated the `follow_up_days` metric to over 1,000 years, falsely classifying unresolved cases as definitively delayed. 

To correct this, any observation date exceeding `2025-01-01` was masked to `NaT`. This correction affected 1,881 records in `date_last_list` and 2 records in `date_first_list`. Following this clamp, 4 records that were previously falsely marked as delayed reverted to an `UNKNOWN` status and were successfully excluded from the classification dataset. No valid historic dates were modified.

## The Authorized Temporal Split
To guarantee robust, fully observable outcomes without needing to drop any `UNKNOWN` observations from the test cohort, the final primary chronological evaluation shifts backwards to years possessing ~100% observability for 24-month delay outcomes.

*   **Train:** 2010–2014
*   **Validation:** 2015
*   **Test:** 2016

This split ensures zero selection bias in the primary evaluation metrics while rigorously preventing temporal leakage.

---

## 1. Model 1: Filing-Time Duration Regression
Predicts the exact continuous duration of a case from the moment of filing.

*   **Prediction Point:** Filing date.
*   **Target:** `case_duration_days`
*   **Eligible Population:** Strictly resolved cases with valid decision dates.
*   **Censoring Handling:** Unresolved cases are explicitly excluded to preserve true exact durations.
*   **Evaluation Split:** Train (2010–2014), Validation (2015), Test (2016).

---

## 2. Model 2: Filing-Time 24-Month Delay Classification
Predicts whether a newly filed case will exceed 24 months in duration.

*   **Prediction Point:** Filing date.
*   **Target:** `delay_24m`
*   **Eligible Population:** Fully observable outcomes only. 
    *   `0`: Resolved $\le$ 730.5 days.
    *   `1`: Resolved > 730.5 days OR Unresolved with `follow_up_days` > 730.5.
*   **Censoring Handling:** Unresolved cases with `follow_up_days` $\le$ 730.5 are UNKNOWN and dropped.
*   **Evaluation Split:** Train (2010–2014), Validation (2015), Test (2016).

---

## 3. Future Extension: Model 3 (Ongoing-Case Prediction)
*   **Prediction Point:** Specific snapshot date.
*   **Target:** Probability of exceeding further delay / survival times.
*   **Eligible Population:** All cases unresolved at the snapshot date.
*   **Evaluation Split:** 2017 and 2018 cohorts (ideal for utilizing heavily censored, recent data).

---

## 4. Future Extension: Model 4 (Next-Listing Delay)
*   **Prediction Point:** Post-hearing update.
*   **Target:** Days until `date_next_list`.
*   **Evaluation Split:** 2017 and 2018 cohorts.
