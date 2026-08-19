# Recommended Model & Dataset Design

Based on the temporal eligibility rules and observability matrix, the following final experimental design is recommended for the JDIS project:

## Model 1: Filing-Time Duration Regression
Predicts the exact total duration of a case from the moment of filing.

*   **Prediction Point:** Filing date.
*   **Target Variable:** `case_duration_days` (continuous).
*   **Eligible Population:** Strictly resolved cases with valid decision dates.
*   **Censoring Treatment:** Unresolved cases are EXCLUDED due to unknown final durations.
*   **Train Period:** 2010–2014
*   **Validation Period:** 2015
*   **Test Period:** 2016 (or 2017, acknowledging increasing selection bias in recent years).

## Model 2: Filing-Time 24-Month Delay Classification
Predicts whether a newly filed case will exceed 24 months in duration.

*   **Prediction Point:** Filing date.
*   **Target Variable:** `delay_24m` (binary: 0 or 1).
*   **Eligible Population:** Cases with fully observable 24-month outcomes (Resolved $\le$ 24m, Resolved > 24m, or Unresolved with > 24m follow-up).
*   **Censoring Treatment:** Unresolved cases with $<$ 24 months of follow-up are classified as UNKNOWN and EXCLUDED. 
*   **Train Period:** 2010–2014
*   **Validation Period:** 2015
*   **Test Period:** 2016 (Guarantees 100% 24-month observability without needing to drop any UNKNOWN records).

## Model 3: Ongoing-Case Delay Prediction
Predicts the probability of further delay for cases that are currently pending.

*   **Prediction Point:** At a specific snapshot date (e.g., end of 2018).
*   **Target Variable:** Probability of exceeding an additional 12/24 months, OR remaining duration.
*   **Eligible Population:** All cases that are active/unresolved at the snapshot date.
*   **Censoring Treatment:** Evaluated using Survival Analysis methodologies or trained on historically analogous ongoing cases that eventually resolved.
*   **Evaluation Period:** 2017 and 2018 cohorts (ideal use case for recent, unresolved data).

## Model 4: Next-Listing Delay Prediction
Operational short-term model predicting the time until the next active hearing.

*   **Prediction Point:** Post-hearing update.
*   **Target Variable:** Days until `date_next_list`.
*   **Eligible Population:** All case updates possessing a valid next listing date.
*   **Censoring Treatment:** Not significantly affected by long-term right-censoring because hearings occur on a continuous operational loop.
*   **Evaluation Period:** 2017 and 2018 cohorts.
