# Dataset C Validation: Hearing Continuation & Next-Listing

## 1. Target Definition
- **Target**: `next_listing_gap_days`
- **Definition**: `date_next_list - date_last_list`
- **Prediction Point**: `date_last_list` (The most recent active hearing)

## 2. Target Distribution & Anomaly Audit
An initial audit of the target variable reveals the following empirical distribution:

| Metric | Value |
| :--- | :--- |
| **Total Rows** | 449,266 |
| **Valid Numeric Targets** | 447,361 |
| **Missing Targets** | 1,905 |
| **Negative Targets** | 212 |
| **Zero-Day Gaps** | 188,179 |
| **Mean** | 18.40 days |
| **Median** | 4.00 days |
| **75th Percentile** | 29.00 days |
| **Maximum** | 1370.00 days |

## 3. Data Cleaning Protocol
To prepare the final ML-ready arrays, the following filtering is applied:
1. **Drop Missing Gaps (n=1,905)**: Determined to be terminal cases (see Censoring Audit).
2. **Drop Negative Gaps (n=212)**: Chronological invalidity (`date_next_list < date_last_list`).
3. **Keep Zero-Day Gaps**: Same-day continuations are procedurally common and valid predictions.
4. **Drop Temporal Anomalies**: Cases with an invalid future `last_list_year` (e.g., year 5000) are dropped.

## 4. Feature Leakage Verification
The prediction point is exactly `date_last_list`.
- `date_next_list` is verified to **not** be present in the feature matrix.
- Post-filing variables like `disp_name` and `date_of_decision` are absent.
- The temporal split will strictly partition chronologically on `date_last_list_dt.year` to prevent look-ahead bias from future cases entering the training window.
