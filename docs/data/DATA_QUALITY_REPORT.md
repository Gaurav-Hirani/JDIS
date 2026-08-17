# JDIS Data Quality & Empirical Profiling Report

**Project**: Judicial Delay Intelligence System (JDIS)  
**Role**: Tanmay — Data Engineer & Data Architect  
**Version**: 2.0.0 (Post-Cleaning & Feature Pipeline Verification)  
**Date**: August 2026  
**Evaluated Corpus**: 450,000 Multi-Year Stratified Sample (2010–2018) + Key Lookups  

---

## 1. Executive Quality Summary

The JDIS data cleaning and feature engineering pipeline has processed and validated the multi-year corpus. All 10 automated schema, leakage, and classification tests passed.

| Quality Dimension | Measured Value | Standard Threshold | Quality Status | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Filing Date Completeness** | 100.0% (450,000 / 450,000) | 100.0% | **EXCELLENT** | Zero missing filing dates |
| **First Hearing Listing Completeness** | 99.64% (448,398 / 450,000) | > 95.0% | **EXCELLENT** | Hearing milestones highly populated |
| **Last Hearing Listing Completeness** | 99.52% (447,847 / 450,000) | > 95.0% | **EXCELLENT** | High integrity for listing span |
| **Inverted Dates Filtered (`decision < filing`)** | 543 cases (0.12%) | < 1.0% | **CLEANED** | Dropped in cleaning pipeline |
| **Total Cleaned Records** | 449,267 cases (99.84%) | > 99.0% | **EXCELLENT** | 100% structurally validated |
| **Resolved Cases for Duration Modeling** | 369,498 cases (82.25%) | > 70.0% | **ROBUST** | Non-negative duration verified |
| **Pending / Censored Cases** | 79,769 cases (17.75%) | — | **NORMAL** | Retained for ongoing backlog metrics |

---

## 2. Civil vs. Criminal 4-Category Empirical Breakdown

The deterministic rule-based classifier combining Statutory Acts (`acts_sections.csv`) and Case Type strings (`type_name_key.csv`) produced the following class distribution:

```text
4-Category Civil vs. Criminal Classification:
├── 1. High-Confidence Criminal:   318,721 cases (70.94%)
├── 2. High-Confidence Civil:       61,779 cases (13.75%)
├── 3. Other/Unknown/Unclassified:  68,699 cases (15.29%)
└── 4. Ambiguous / Mixed:               68 cases ( 0.02%)
```

> [!IMPORTANT]
> **No Synthetic Forcing**: Rather than forcing the remaining 15.29% of cases into arbitrary binary buckets, they are transparently labeled as `Other/Unknown/Unclassified`. In numerical model matrices, `is_criminal_code` is encoded as `1` (Criminal), `0` (Civil), and `-1` (Unknown/Ambiguous).

---

## 3. Target Distributions & Class Balances

### 3.1 Case Duration Distribution (`case_duration_days`)
Calculated on $N = 369,498$ valid resolved cases:
- **Mean Duration**: **538.32 days** (~1.47 years / 17.7 months)
- **Standard Deviation**: **629.17 days**
- **Median ($p_{50}$)**: **311.00 days** (~10.2 months)
- **25th Percentile ($p_{25}$)**: **41.00 days** (~1.3 months)
- **75th Percentile ($p_{75}$)**: **809.00 days** (~26.6 months)
- **90th Percentile ($p_{90}$)**: **1,451.00 days** (~47.7 months)
- **95th Percentile ($p_{95}$)**: **1,907.00 days** (~62.6 months)
- **Minimum**: **0.00 days**, **Maximum**: **3,811.00 days**

### 3.2 Delay Classification Targets

| Target Variable | Threshold Condition | Delayed Count | Delayed % | On-Time % | Role in JDIS |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Target (`delay_24m`)** | `duration > 730.50 days` | 103,061 | **27.89%** | 72.11% | **Primary Delay Target** |
| **Sensitivity Target (`delay_12m`)** | `duration > 365.25 days` | 172,788 | **46.76%** | 53.24% | Sensitivity Benchmark |
| **Sensitivity Target (`delay_36m`)** | `duration > 1095.75 days` | 61,288 | **16.59%** | 83.41% | Extreme Delay Benchmark |

### 3.3 Next-Listing Targets (Dataset C)
- **Next-Listing Gap (`next_listing_gap_days`)**: Median: 28.0 days, Mean: 54.2 days.
- **Hearing Continuation Risk (`hearing_continuation_risk`)**: 48.9% active hearing span $> 1$ year.

---

## 4. Pipeline Artifact Inventory

| Output Dataset | File Path | File Size | Shape | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Master Clean Data** | `data/processed/cases_clean.parquet` | 13.98 MB | (449,267, 40) | Normalized relational baseline |
| **Dataset A** | `data/features/filing_features.parquet` | ~45.2 MB | (449,267, 87) | Filing-Time Model Matrix (Tier A) |
| **Dataset B** | `data/features/ongoing_features.parquet` | ~45.8 MB | (449,267, 88) | Ongoing-Case Matrix (Tier A + First List) |
| **Dataset C** | `data/features/hearing_features.parquet` | ~12.1 MB | (449,267, 19) | Next-Listing Delay Matrix (Tier A + Last List) |
| **TF-IDF Vectorizer** | `data/features/tfidf_vectorizer.joblib` | ~1.2 MB | 5,000 Vocab | Fitted strictly on Train (2010–2016) |
| **SVD Dimensionality** | `data/features/tfidf_svd_model.joblib` | ~2.1 MB | 50 Components | Fitted strictly on Train (2010–2016) |

---

## 5. Automated Validation Results

```text
Ran 10 automated data integrity tests in tests/data/:
├── test_processed_cases_clean_exists ...... PASSED
├── test_dataset_a_filing_features_schema ... PASSED
├── test_dataset_c_hearing_features_schema . PASSED
├── test_no_negative_durations_in_resolved . PASSED
├── test_zero_tier_c_columns_in_dataset_a ... PASSED
├── test_zero_next_listing_date_in_dataset_c  PASSED
├── test_temporal_split_integrity .......... PASSED
├── test_criminal_classification_rules ..... PASSED
├── test_civil_classification_rules ........ PASSED
└── test_ambiguous_and_unknown_rules ....... PASSED
----------------------------------------------------------------------
Result: 10/10 Tests Passed (100% Success) in 3.17s
```
