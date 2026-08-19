# Temporal Target Distribution Audit

## 1. Executive Summary

A severe temporal target distribution shift was observed during the baseline classification experiments, with the primary target `delay_24m` collapsing from ~27.8% in the training years (2010–2016) to just 1.39% in the 2017 validation cohort.

This audit investigates the root cause of this anomaly by tracking yearly data compositions, durations, resolutions, and missingness.

**Conclusion:** The shift is a classic example of **Right-Censoring / Filtering Bias (Option D)**. Dropping "unresolved" cases from recent years systematically eliminates cases with long durations, artificially deflating the delay rate in the validation and test sets.

---

## 2. Year-by-Year Target & Resolution Analysis

| Year | Total Records | Resolved | Unresolved | Resolution % | Mean Duration | Median Duration | Delay 24m Count | Delay 24m % |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **2010** | 49,867 | 48,501 | 1,366 | 97.26% | 869.8 | 661.0 | 22,703 | 46.81% |
| **2011** | 49,892 | 47,764 | 2,128 | 95.73% | 817.0 | 623.0 | 21,542 | 45.10% |
| **2012** | 49,911 | 47,181 | 2,730 | 94.53% | 721.3 | 500.0 | 17,915 | 37.97% |
| **2013** | 49,949 | 45,167 | 4,782 | 90.43% | 579.7 | 397.0 | 14,064 | 31.14% |
| **2014** | 49,836 | 43,250 | 6,586 | 86.78% | 470.6 | 284.0 | 11,461 | 26.50% |
| **2015** | 49,982 | 41,178 | 8,804 | 82.39% | 413.8 | 250.0 | 10,588 | 25.71% |
| **2016** | 49,930 | 37,319 | 12,611 | 74.74% | 296.9 | 185.0 | 4,261 | 11.42% |
| **2017** | 49,913 | 33,227 | 16,686 | 66.57% | 200.9 | 127.0 | 463 | 1.39% |
| **2018** | 49,986 | 25,911 | 24,075 | 51.84% | 87.4 | 44.0 | 21 | 0.08% |

**Key Observation:** As the filing year approaches the present (snapshot likely taken late 2018/2019), the "Resolution %" drops significantly. Correspondingly, the maximum mathematically possible duration for a 2017/2018 case physically captured in this snapshot drops below 730 days.

---

## 3. Case Category & Case Type Stability

**Case Category Distribution:**
The Civil/Criminal composition shifted slightly but not dramatically enough to explain a 26-point drop in delay rates:
*   **2010–2016:** ~73% Criminal, ~11-14% Civil
*   **2017:** 68.9% Criminal, 19.8% Civil
*   **2018:** 67.4% Criminal, 20.7% Civil

**Dominant Case Types (2010-2016 vs 2017):**
*   **Train Top 3:** S.C.C (36.3%), CRI.M.A. (14.5%), R.C.C. (10.9%)
*   **Val Top 3:** S.C.C (39.6%), CRI.M.A. (16.4%), R.C.C. (7.2%)
The fundamental composition of case types is practically identical across the split.

---

## 4. Missingness & Target Construction

*   **Missing Filing/Decision Dates:** No anomalous missing dates other than the expected increase in missing `date_of_decision` for recent, unresolved cases (33.4% in 2017, 48.1% in 2018).
*   **Missing Judge/Court IDs:** Remained highly consistent (~85-90% missing `ddl_filing_judge_id` due to raw dataset constraints across all years).
*   **Target Computation Match:** Verified `date_of_decision - date_of_filing == case_duration_days` yields a 100% mathematical match. There is no code bug in target generation.

---

## 5. Final Analysis & Conclusion

Based on the evidence gathered, the observed temporal shift falls cleanly under:

### **D. Filtering / Preprocessing Issue**

**Mechanism:** 
The pipeline strictly filters out cases where `case_duration_days` is missing (i.e., cases that have not yet been decided by the snapshot date). Because the 2018 cases only had ~1 year to resolve before the dataset cutoff, and 2017 cases only had ~2 years, **any case filed in 2017 that actually takes more than 24 months to resolve is still open at the time of data collection**. 

Therefore, by filtering to only *resolved* cases in recent years, we systematically delete the delayed cases, leaving behind only the fast, early-resolved cases. This artificially plunges the delay rate toward 0% in the validation and test cohorts, completely invalidating them as a testbed for >24m delay classification under the current filtering logic.

---
**Recommendation:**
This filtering bias must be corrected before progressing to advanced models. Unresolved cases older than 24 months must be treated as **positive class** targets (they are factually delayed >24m, even if we don't know their final duration), rather than being indiscriminately dropped.
