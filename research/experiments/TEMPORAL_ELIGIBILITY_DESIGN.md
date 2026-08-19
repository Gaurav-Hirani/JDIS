# Temporal Eligibility & Experimental Design

## 1. Target-Specific Eligibility Rules
To definitively resolve the right-censoring selection bias, case eligibility is strictly enforced at the target level based on individualized follow-up observability:

*   **A. Exact Duration Regression:** Eligible ONLY if `date_of_filing` and `date_of_decision` are valid, and exact `case_duration_days` can be calculated. Unresolved cases are excluded.
*   **B. 12-Month Classification:** Eligible if resolved OR (unresolved AND case-specific follow-up > 365.25 days). If unresolved and follow-up $\le$ 365.25 days, the outcome is UNKNOWN (excluded).
*   **C. 24-Month Classification:** Eligible if resolved OR (unresolved AND case-specific follow-up > 730.5 days). If unresolved and follow-up $\le$ 730.5 days, the outcome is UNKNOWN (excluded).
*   **D. 36-Month Classification:** Eligible if resolved OR (unresolved AND case-specific follow-up > 1095.75 days). If unresolved and follow-up $\le$ 1095.75 days, the outcome is UNKNOWN (excluded).

## 2. Year-Eligibility Matrix
Based on the exact observability rules, here is the eligibility count for each year (see `research/results/temporal_eligibility_matrix.csv` for exact outputs):

| Filing Year | Total Cases | Exact Duration Eligible (Resolved) | 12m Observable % | 24m Observable % | 36m Observable % |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **2010** | 49,867 | 48,501 (97%) | 100.0% | 100.0% | 100.0% |
| **2011** | 49,892 | 47,764 (95%) | 100.0% | 100.0% | 100.0% |
| **2012** | 49,911 | 47,181 (94%) | 100.0% | 100.0% | 100.0% |
| **2013** | 49,949 | 45,167 (90%) | 100.0% | 100.0% | 100.0% |
| **2014** | 49,836 | 43,250 (86%) | 100.0% | 100.0% | 100.0% |
| **2015** | 49,982 | 41,178 (82%) | 100.0% | 100.0% | 100.0% |
| **2016** | 49,930 | 37,319 (74%) | 100.0% | **100.0%** | 79.4% |
| **2017** | 49,913 | 33,227 (66%) | 100.0% | **73.8%** | 68.2% |
| **2018** | 49,986 | 25,911 (51%) | 63.0% | **55.1%** | 51.8% |

## 3. Selection of Valid Chronological Splits
The primary research evaluation must remain strictly chronological to test out-of-time generalization without leakage. Random splitting is strictly prohibited for the primary baseline.

**Identifying the Latest Filing Year for 24-Month Delay:**
The latest year with ~100% 24-month observability is **2016**. By 2017, 26% of cases are UNKNOWN. By 2018, 45% are UNKNOWN. 

**Proposed Split Strategy 1 (Strict Observability):**
*   **Train:** 2010–2014
*   **Validation:** 2015
*   **Test:** 2016
*   *Advantage:* Zero selection bias or dropping required for classification. 100% observability across all sets.

**Proposed Split Strategy 2 (Imputed/Dropped Recent):**
*   **Train:** 2010–2015
*   **Validation:** 2016
*   **Test:** 2017 (dropping the 26% UNKNOWN cases)
*   *Advantage:* Evaluates closer to the present day. *Disadvantage:* Re-introduces mild selection bias in the test set.

*(See `research/results/candidate_temporal_splits.csv`)*

## 4. 24-Month Classification Target Construction
*   **0 (On Time):** The case is resolved in $\le$ 730.5 days.
*   **1 (Delayed):** The case is resolved > 730.5 days OR unresolved with follow-up > 730.5 days.
*   **UNKNOWN:** Unresolved with follow-up $\le$ 730.5 days. These MUST be excluded from supervised evaluation unless Survival Analysis is used.

## 5. Duration Regression Target Construction
The target `case_duration_days` will ONLY be populated for fully resolved cases. Unresolved cases will NOT have their duration replaced by observation time or censoring time, to avoid corrupting exact duration metrics (MAE/RMSE).

## 6. Potential Survival Analysis
*   **Event:** Case Disposition (Resolved = 1, Unresolved = 0)
*   **Time:** `case_duration_days` if resolved, else `follow_up_days`.
*   **Feasibility:** Highly feasible. The dataset possesses precise tracking of time-to-event and censoring times. This would allow the inclusion of the 13k+ censored 2017 cases in a scientifically robust manner. 

## 7. Use of 2017 and 2018 Cohorts
While 2017/2018 cannot serve as the primary fully-observed 24m test cohorts without dropping substantial portions of data, they remain critical for:
*   **Model 3 (Ongoing-Case Prediction):** Predicting the remaining duration for cases still pending in 2017/2018.
*   **Model 4 (Next-listing delay):** Short-term operational predictions unaffected by 24-month horizons.
*   **Exploratory Temporal Robustness Analysis:** Measuring performance decay on heavily censored modern data.

## 8. IEEE Methodology Implication
The paper MUST explicitly state:
> "Because a snapshot of judicial records naturally censors pending cases, early iterations of this dataset naively filtered out all unresolved cases. As demonstrated in our censoring audit, this created severe right-censoring selection bias—artificially plunging the apparent delay rate in the 2017 cohort from an expected ~30% to just 1.3%. To maintain methodological validity, our final evaluation enforces a strict case-level observability rule: an unresolved case is only classified as delayed if its individual tracking history proves it remained active beyond the target threshold. This necessitates shifting the primary evaluation window to the 2010–2016 period, which possesses near-100% case observability."
