# Case-Level Observation Audit

## 1. Defining the Case-Specific Observation Date
A global dataset maximum date (e.g., Jan 2022) only proves that the database existed until then. It does not prove that an individual court case was actively tracked until that date.

To measure individual follow-up, the case-specific "last observed date" is defined as:
`case_last_observed_date = max(date_first_list, date_last_list, date_next_list)`

For unresolved cases, the observation duration (follow-up) is:
`follow_up_days = case_last_observed_date - date_of_filing`

---

## 2. Global Unresolved Follow-Up Totals
Out of **79,768** total unresolved cases (2010–2018):
*   **>12 months follow-up:** 61,261 (76.8%)
*   **>24 months follow-up:** 44,220 (55.4%)
*   **>36 months follow-up:** 29,513 (37.0%)

This reveals that a massive portion of unresolved cases were "lost" or stopped updating before crossing the 24 or 36-month thresholds.

---

## 3. Year-by-Year Follow-up Breakdown

### 24-Month Target Observability

| Filing Year | Total | Unresolved | Proven >24m | Censored <24m | Unknown |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **2010** | 49,867 | 1,366 | 1,365 | 1 | 0 |
| **2011** | 49,892 | 2,128 | 2,127 | 1 | 0 |
| **2012** | 49,911 | 2,730 | 2,730 | 0 | 0 |
| **2013** | 49,949 | 4,782 | 4,782 | 0 | 0 |
| **2014** | 49,836 | 6,586 | 6,586 | 0 | 0 |
| **2015** | 49,982 | 8,804 | 8,803 | 1 | 0 |
| **2016** | 49,930 | 12,611 | 12,611 | 0 | 0 |
| **2017** | 49,913 | 16,686 | 3,596 | 13,090 | 0 |
| **2018** | 49,986 | 24,075 | 1,620 | 22,455 | 0 |

### 36-Month Target Observability

| Filing Year | Total | Unresolved | Proven >36m | Censored <36m | Unknown |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **2010** | 49,867 | 1,366 | 1,365 | 1 | 0 |
| **2011** | 49,892 | 2,128 | 2,127 | 1 | 0 |
| **2012** | 49,911 | 2,730 | 2,730 | 0 | 0 |
| **2013** | 49,949 | 4,782 | 4,782 | 0 | 0 |
| **2014** | 49,836 | 6,586 | 6,586 | 0 | 0 |
| **2015** | 49,982 | 8,804 | 8,803 | 1 | 0 |
| **2016** | 49,930 | 12,611 | 2,320 | 10,291 | 0 |
| **2017** | 49,913 | 16,686 | 797 | 15,889 | 0 |
| **2018** | 49,986 | 24,075 | 3 | 24,072 | 0 |

---

## 4. Verification of the 2017 and 2018 Cohorts

For the **24-month** target in 2017:
*   Total Unresolved: 16,686
*   Proven delayed (>24m follow-up): 3,596
*   **Censored (last observed <24m): 13,090**

For the **24-month** target in 2018:
*   Total Unresolved: 24,075
*   Proven delayed (>24m follow-up): 1,620
*   **Censored (last observed <24m): 22,455**

Because the vast majority of unresolved cases in 2017 and 2018 dropped off the radar *before* they reached 24 months, their true 24-month outcome is permanently unknown.

---

## 5. Answers & Target Recommendations

**1. What is the best case-specific last-observation date?**
`max(date_first_list, date_last_list, date_next_list)`. These active hearing/listing fields accurately represent the last physical update made to the case lifecycle.

**2. How many unresolved cases have proven >12m follow-up?**
61,261 (76.8% of all unresolved cases).

**3. How many have proven >24m follow-up?**
44,220 (55.4% of all unresolved cases).

**4. How many have proven >36m follow-up?**
29,513 (37.0% of all unresolved cases).

**5. Which filing years have fully observable 24-month outcomes?**
**2010 through 2016 only.** In these years, observability is ~100%.

**6. Which filing years have fully observable 36-month outcomes?**
**2010 through 2015 only.** (2016 suffers massive censoring at the 36m mark).

**7. Can unresolved cases safely be labelled delayed for the 24-month target?**
**Only for years 2010–2016.** For 2017 and 2018, they absolutely *cannot* be assumed delayed, because 13,000+ and 22,000+ respectively were censored before 24 months.

**8. Can unresolved cases safely be labelled delayed for the 36-month target?**
**Only for years 2010–2015.**

---

## 6. Final Target Recommendations

**For 24-Month Classification Target (`delay_24m`)**
*   `0`: Resolved in $\le$ 730.5 days.
*   `1`: Resolved in > 730.5 days **OR** (Unresolved AND `follow_up_days` > 730.5).
*   `Unknown/NaN`: Unresolved AND `follow_up_days` $\le$ 730.5.

**Impact on Regression:**
Exact duration regression remains mathematically impossible for unresolved cases (even if we know they crossed 24 months, we don't know exactly when they finished). We must continue to either restrict exact regression to resolved cases (acknowledging the bias) or pursue survival analysis.
