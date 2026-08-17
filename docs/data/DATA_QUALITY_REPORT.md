# JDIS Data Quality & Empirical Profiling Report

**Project**: Judicial Delay Intelligence System (JDIS)  
**Role**: Tanmay — Data Engineer & Data Architect  
**Version**: 1.0.0  
**Date**: August 2026  
**Evaluation Sample**: 450,000 Multi-Year Stratified Cases (2010–2018) + Complete Key Metadata Repositories

---

## 1. Overview & Verification Summary

This report documents the empirical findings from profiling 450,000 case records sampled across all 9 filing years (2010–2018), 76.7 million Act records, 98,478 judges, and 6,958 court complexes.

| Quality Dimension | Measured Value | Standard Threshold | Quality Status | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Filing Date Completeness** | 100.0% (450,000 / 450,000) | 100.0% | **EXCELLENT** | Zero missing filing dates |
| **First Hearing Listing Completeness** | 99.64% (448,398 / 450,000) | > 95.0% | **EXCELLENT** | Hearing milestones highly populated |
| **Last Hearing Listing Completeness** | 99.52% (447,847 / 450,000) | > 95.0% | **EXCELLENT** | High integrity for listing span |
| **Primary Key Uniqueness (`ddl_case_id`)** | 100.0% unique | 100.0% | **EXCELLENT** | Zero duplicate IDs observed |
| **Date Ordering Inversions (`decision < filing`)** | 0.12% (543 cases) | < 1.0% | **CLEANABLE** | Minor clerical error, safely dropped |
| **Case Resolution Rate** | 82.27% disposed (370,217 cases) | > 70.0% | **SUFFICIENT** | Robust sample of resolved durations |
| **Pending / Censored Cases** | 17.73% pending (79,783 cases) | — | **NORMAL** | Retained for ongoing backlog metrics |

---

## 2. Target Variable Empirical Distributions

### 2.1 Case Duration Distribution (`case_duration_days`)
Calculated on $N = 369,674$ valid resolved cases with non-negative duration:

```text
Duration (Days) Distribution Metrics:
├── Mean:              538.32 days (~1.47 years / 17.7 months)
├── Standard Deviation: 629.17 days (~1.72 years)
├── Median (p50):      311.00 days (~10.2 months)
├── 25th Percentile:    41.00 days (~1.3 months)
├── 75th Percentile:   809.00 days (~26.6 months)
├── 90th Percentile:  1,451.00 days (~47.7 months / ~4.0 years)
├── 95th Percentile:  1,907.00 days (~62.6 months / ~5.2 years)
├── Minimum:             0.00 days (Disposed same-day)
└── Maximum:          3,811.00 days (Disposed after ~10.4 years)
```

### 2.2 Delay Classification Target Balance

| Delay Threshold | Condition | Delayed Count | Delayed % | On-Time % | Class Imbalance Ratio | Primary Usage |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **12 Months (1 Year)** | `duration > 365.25 days` | 172,875 | **46.76%** | 53.24% | 1 : 1.14 (Balanced) | Sensitivity Analysis |
| **24 Months (2 Years)** | `duration > 730.50 days` | 103,115 | **27.89%** | 72.11% | 1 : 2.58 (Clean) | **PRIMARY JDIS TARGET** |
| **36 Months (3 Years)** | `duration > 1095.75 days` | 61,316 | **16.59%** | 83.41% | 1 : 5.03 (Moderate) | Sensitivity Analysis |

---

## 3. Civil vs. Criminal Distribution

Based on standardized legal mapping across 80.9 million historical case type records in `type_name_key.csv` and `acts_sections.csv`:

```text
Case Category Distribution:
├── Criminal Cases:         37,663,296 records (46.54%)
├── Civil Cases:            12,484,757 records (15.43%)
├── Unclassified / Other:   30,787,225 records (38.03%)
└── Ambiguous / Mixed:             666 records ( 0.00%)
```

*Note: In the clean dataset, all cases will be strictly mapped into either Civil or Criminal using the combined Case Type + Acts/Sections rule.*

---

## 4. Hearing Milestones & Gap Distributions

| Milestone Interval | Metric | Value (Days) | Interpretation |
| :--- | :--- | :--- | :--- |
| **Filing to First Listing** | Median | 0.0 days | Cases are typically listed for initial registry processing on the date of filing or within 25 days (Mean: 25.1d) |
| **First Listing to Last Listing** | Median | 356.0 days | Total active trial/hearing duration averages ~1 year |
| **First Listing to Last Listing** | Mean | 583.0 days | Long-tail cases extend hearing span to ~1.6 years |

---

## 5. Column-by-Column Missingness Audit

| Column Name | Total Rows | Non-Null Rows | Missing Rows | Missing % | Action Required in Pipeline |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ddl_case_id` | 450,000 | 450,000 | 0 | 0.00% | None (Primary Key) |
| `year` | 450,000 | 450,000 | 0 | 0.00% | None |
| `state_code` | 450,000 | 450,000 | 0 | 0.00% | None |
| `dist_code` | 450,000 | 450,000 | 0 | 0.00% | None |
| `court_no` | 450,000 | 450,000 | 0 | 0.00% | None |
| `cino` | 450,000 | 450,000 | 0 | 0.00% | None |
| `judge_position` | 450,000 | 450,000 | 0 | 0.00% | None |
| `female_defendant` | 450,000 | 450,000 | 0 | 0.00% | Re-encode `-9998`, `-9999` |
| `female_petitioner` | 450,000 | 450,000 | 0 | 0.00% | Re-encode `-9998`, `-9999` |
| `female_adv_def` | 450,000 | 450,000 | 0 | 0.00% | Re-encode `-9998`, `-9999` |
| `female_adv_pet` | 450,000 | 450,000 | 0 | 0.00% | Re-encode `-9998`, `-9999` |
| `type_name` | 450,000 | 450,000 | 0 | 0.00% | None |
| `purpose_name` | 450,000 | 441,280 | 8,720 | 1.94% | Impute categorical `"UNKNOWN"` |
| `disp_name` | 450,000 | 450,000 | 0 | 0.00% | None (Post-Disposal target) |
| `date_of_filing` | 450,000 | 450,000 | 0 | 0.00% | Parse ISO datetime |
| `date_of_decision` | 450,000 | 370,217 | 79,783 | 17.73% | Supervised target filter |
| `date_first_list` | 450,000 | 448,398 | 1,602 | 0.36% | Impute `date_of_filing` if null |
| `date_last_list` | 450,000 | 447,847 | 2,153 | 0.48% | Impute `date_first_list` if null |
| `date_next_list` | 450,000 | 447,823 | 2,177 | 0.48% | Impute `date_last_list` if null |

---

## 6. Data Quality Verdict

The dataset exhibits **high structural integrity**, **complete temporal coverage**, and **scientifically valid target distributions**. The cleanable anomaly rate is exceptionally low (0.12%), making this dataset ideal for training high-precision judicial delay prediction models.
