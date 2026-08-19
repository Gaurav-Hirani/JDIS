# Dataset C Censoring & Selection Audit

## 1. The Missing Target Anomaly
During the initial Dataset C validation, exactly 1,905 cases lacked a valid `next_listing_gap_days` target.

## 2. Cross-Reference Audit with Case Dispositions
We cross-referenced the 1,905 missing-target cases against the primary `cases_clean.parquet` database to check their final lifecycle status.

**Results:**
- **Missing targets with a populated `date_of_decision`**: 1,898 cases (99.6%)
- **Missing targets without a populated `date_of_decision`**: 7 cases (0.4%)

## 3. Conclusion & Handling Strategy
The overwhelming majority of missing `next_listing_gap_days` (1,898 / 1,905) occur precisely because the case **reached a terminal decision on the date of the last hearing**. 

Records without an observed next listing were excluded from the next-listing regression task because no next-listing interval is defined. The event we are trying to predict (a scheduling gap) does not exist for the final hearing of a disposed case.

**Action:**
We excluded these 1,905 rows from the training and evaluation cohorts.
