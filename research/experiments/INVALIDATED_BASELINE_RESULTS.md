# Exploratory / Invalidated Baseline Results

## Previous Experimental Design
During the initial phase of the research, the baseline models were evaluated using the following temporal split:
*   **Train:** 2010–2016
*   **Validation:** 2017

## Reason for Invalidation
A subsequent temporal target-distribution audit revealed a severe right-censoring bias in the validation cohort. Specifically, the data pipeline indiscriminately filtered out all "unresolved" cases prior to model training.

Because the dataset snapshot ends in late 2018 / early 2022 (with varying operational tracking), cases filed in 2017 that took more than 24 months to resolve were systematically still pending (unresolved) at the time of data collection. By dropping unresolved cases, the pipeline silently deleted almost all of the delayed cases from the 2017 validation set, artificially suppressing the `delay_24m` positive rate to **1.39%** (down from an expected ~30%).

Consequently, evaluating 24-month delay prediction on the 2017 cohort under that data-filtering logic produced heavily distorted precision and recall metrics.

## Replacement Methodology
To enforce methodological integrity, the experimental design has been updated:
1.  **Strict Observability Rule:** A case is only classified if its individual follow-up history decisively proves whether it exceeded 24 months. Unresolved cases are now labeled as delayed (`delay_24m = 1`) if they were observed for > 730.5 days. Cases with insufficient observation (UNKNOWN) are explicitly dropped.
2.  **New Chronological Split:** Because the 2017 and 2018 cohorts suffer from massive censoring (where follow-up ended before 24 months), the primary filing-time classification evaluation has been shifted backwards to guarantee 100% observability:
    *   **Train:** 2010–2014
    *   **Validation:** 2015
    *   **Test:** 2016

The previous baseline metrics and model artifacts generated under the old split remain available in the repository for exploratory provenance but are formally declared **INVALID FOR FINAL RESEARCH EVALUATION** and must not be reported in the IEEE paper as the final baseline.
