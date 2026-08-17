# JDIS Master Data Dictionary & Feature Specification

**Project**: Judicial Delay Intelligence System (JDIS)  
**Role**: Tanmay — Data Engineer & Data Architect  
**Version**: 1.0.0 (Release Candidate)  
**Date**: August 2026  

---

## 1. Primary Target Variables

| Target Variable | Source Fields | Exact Formula / Definition | Type | Valid Range | Missing Strategy | Prediction Stage | Leakage Risk | Owner |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `case_duration_days` | `date_of_filing`, `date_of_decision` | `(date_of_decision - date_of_filing).days` | Float / Int | $[0, 5000]$ | Excluded if pending (`decision` is null) | Ground Truth Target | **High (Never use as feature)** | Gaurav / Tanmay |
| `delay_24m` | `case_duration_days` | $\mathbb{I}(\text{case\_duration\_days} > 730.5)$ | Binary Int (0/1) | $\{0, 1\}$ | Excluded if pending | Primary Classification Target | **High (Never use as feature)** | Gaurav / Tanmay |
| `delay_12m` | `case_duration_days` | $\mathbb{I}(\text{case\_duration\_days} > 365.25)$ | Binary Int (0/1) | $\{0, 1\}$ | Excluded if pending | Sensitivity Target | **High (Never use as feature)** | Gaurav / Tanmay |
| `delay_36m` | `case_duration_days` | $\mathbb{I}(\text{case\_duration\_days} > 1095.75)$ | Binary Int (0/1) | $\{0, 1\}$ | Excluded if pending | Sensitivity Target | **High (Never use as feature)** | Gaurav / Tanmay |
| `hearing_delay_risk` | `date_first_list`, `date_last_list` | $\mathbb{I}((\text{date\_last\_list} - \text{date\_first\_list}).\text{days} > 365.25)$ | Binary Int (0/1) | $\{0, 1\}$ | Excluded if no hearing dates | Hearing Stage Target | **Hearing Model Only** | Gaurav / Tanmay |

---

## 2. Filing-Stage Feature Set (Filing Model)

### 2.1 Geographic & Court Context Features

| Feature Name | Source Field(s) | Formula / Definition | Type | Valid Range | Missing Strategy | Stage | Leakage Risk |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `state_code` | `state_code` | Categorical state jurisdiction code | Categorical | 1 to 35 | Must not be null | Filing | None (Safe) |
| `dist_code` | `dist_code` | District jurisdiction code | Categorical | 1 to 75 | Must not be null | Filing | None (Safe) |
| `court_no` | `court_no` | Court establishment / courtroom number | Categorical | 1 to 99 | Must not be null | Filing | None (Safe) |
| `filing_year` | `date_of_filing` | `date_of_filing.year` | Integer | $2010 \le Y \le 2018$ | Must not be null | Filing | None (Safe) |
| `filing_month` | `date_of_filing` | `date_of_filing.month` | Integer | 1 to 12 | Must not be null | Filing | None (Safe) |
| `filing_day_of_week` | `date_of_filing` | `date_of_filing.dayofweek` | Integer | 0 (Mon) to 6 (Sun) | Must not be null | Filing | None (Safe) |
| `filing_quarter` | `date_of_filing` | `date_of_filing.quarter` | Integer | 1 to 4 | Must not be null | Filing | None (Safe) |

### 2.2 Case Characteristics & Legal Complexity Features

| Feature Name | Source Field(s) | Formula / Definition | Type | Valid Range | Missing Strategy | Stage | Leakage Risk |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `case_type_code` | `type_name` | Integer identifier for case type | Categorical | 1 to 10,000 | Impute `-1` | Filing | None (Safe) |
| `is_criminal` | `type_name_key`, `acts_sections` | 1 if criminal case type / IPC charge, else 0 | Binary (0/1) | $\{0, 1\}$ | Fallback to text classification | Filing | None (Safe) |
| `judge_position_clean` | `judge_position` | Standardized judge designation (CJM, District, Civil, etc.) | Categorical | 10 standard categories | Mode imputation | Filing | None (Safe) |
| `statutory_act_count` | `acts_sections.csv` | Count of distinct legal Acts cited in case | Integer | $0 \le N \le 50$ | Default 0 if unlisted | Filing | None (Safe) |
| `ipc_section_count` | `acts_sections.csv` | Count of distinct IPC sections cited | Integer | $0 \le N \le 100$ | Default 0 if unlisted | Filing | None (Safe) |
| `bailable_ipc_flag` | `acts_sections.csv` | 1 if any cited IPC section is bailable, 0 if non-bailable, -1 if non-IPC | Categorical | $\{-1, 0, 1\}$ | Impute `-1` | Filing | None (Safe) |
| `primary_act_code` | `acts_sections.csv` | Most frequently cited Act code for the case | Categorical | Valid Act IDs | Impute `-1` | Filing | None (Safe) |

### 2.3 Party & Advocate Demographic Features

| Feature Name | Source Field(s) | Formula / Definition | Type | Valid Range | Missing Strategy | Stage | Leakage Risk |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `female_petitioner_flag` | `female_petitioner` | 1 if female petitioner, 0 if male, -1 if unclear/missing | Categorical | $\{-1, 0, 1\}$ | Normalized encoding | Filing | None (Safe) |
| `female_defendant_flag` | `female_defendant` | 1 if female defendant, 0 if male, -1 if unclear/missing | Categorical | $\{-1, 0, 1\}$ | Normalized encoding | Filing | None (Safe) |
| `female_adv_pet_flag` | `female_adv_pet` | 1 if female petitioner advocate, 0 if male, -1 if unclear/missing | Categorical | $\{-1, 0, 1\}$ | Normalized encoding | Filing | None (Safe) |
| `female_adv_def_flag` | `female_adv_def` | 1 if female defense advocate, 0 if male, -1 if unclear/missing | Categorical | $\{-1, 0, 1\}$ | Normalized encoding | Filing | None (Safe) |

### 2.4 Time-Safe Historical Aggregate Features (Chronological Expanding Window)

| Feature Name | Source Field(s) | Formula / Definition | Type | Valid Range | Missing Strategy | Stage | Leakage Risk |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `court_prior_delay_rate` | Historical cases in same court | Smoothed delay rate among cases decided before `date_of_filing` | Float | $[0.0, 1.0]$ | Impute global historical mean | Filing | **Requires strict time window** |
| `court_prior_avg_duration` | Historical cases in same court | Mean duration (days) of cases decided before `date_of_filing` | Float | $[0, 3000]$ | Impute state historical mean | Filing | **Requires strict time window** |
| `court_prior_active_backlog` | Historical filings in same court | Count of cases filed before $T_i$ and not yet decided by $T_i$ | Integer | $\ge 0$ | Impute district median | Filing | **Requires strict time window** |
| `judge_prior_delay_rate` | Historical cases with same filing judge | Smoothed delay rate of judge among cases decided before $T_i$ | Float | $[0.0, 1.0]$ | Impute court/bench mean | Filing | **Requires strict time window** |
| `judge_prior_cases_decided` | Historical cases with same filing judge | Count of cases decided by judge prior to $T_i$ | Integer | $\ge 0$ | Impute 0 | Filing | **Requires strict time window** |
| `casetype_prior_delay_rate` | Historical cases of same case type | Smoothed delay rate for case type prior to $T_i$ | Float | $[0.0, 1.0]$ | Impute state mean | Filing | **Requires strict time window** |

### 2.5 NLP Text Representation Features

| Feature Name | Source Field(s) | Formula / Definition | Type | Valid Range | Missing Strategy | Stage | Leakage Risk |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `tfidf_dim_0` to `tfidf_dim_49` | Concatenated metadata strings | Top 50 TruncatedSVD components from TF-IDF vectorizer (fit on Train) | Float | $[-\infty, \infty]$ | Default 0.0 | Filing | **Fit on Train split only** |

---

## 3. In-Progress Hearing Features (Hearing Stage Model Only)

| Feature Name | Source Field(s) | Formula / Definition | Type | Valid Range | Missing Strategy | Stage | Leakage Risk |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `filing_to_first_list_days` | `date_first_list`, `date_of_filing` | `(date_first_list - date_of_filing).days` | Integer | $[0, 2000]$ | Median imputation | In-Progress | **Hearing Model Only** |
| `hearing_span_days` | `date_last_list`, `date_first_list` | `(date_last_list - date_first_list).days` | Integer | $[0, 3500]$ | Default 0 | In-Progress | **Hearing Model Only** |
| `next_listing_gap_days` | `date_next_list`, `date_last_list` | `(date_next_list - date_last_list).days` | Integer | $[0, 1000]$ | Median imputation | In-Progress | **Hearing Model Only** |
| `purpose_stage_clean` | `purpose_name`, `purpose_name_key` | Categorical procedural stage (Evidence, Arguments, Summons, etc.) | Categorical | Standard categories | Token `"UNKNOWN"` | In-Progress | **Hearing Model Only** |

---

## 4. Feature Ownership & Testing Protocol

- **Feature Engineering Module**: `src/features/build_features.py`
- **Unit & Data Integrity Tests**: `tests/data/test_features.py`
- **Validation Checks**:
  1. Range verification for all numerical features.
  2. Zero nulls in final model feature matrices.
  3. No negative durations or historical window leakage.
