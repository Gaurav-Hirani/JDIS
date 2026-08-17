# JDIS Feature Leakage Audit & Time-Safety Protocol

**Project**: Judicial Delay Intelligence System (JDIS)  
**Role**: Tanmay — Data Engineer & Data Architect  
**Date**: August 2026  
**Document Classification**: Scientific Data Integrity & Research Validity Standard  
**Integrity Rule**: Zero Tolerance for Temporal Contamination or Post-Disposal Feature Leakage

---

## 1. Executive Mandate

A predictive AI model for judicial delay is scientifically invalid if it incorporates information that was not available at the exact moment a prediction is made. 

In judicial data systems, data leakage frequently occurs via:
1. **Target-Derived Variables**: Using final case outcome or post-decision events as input features.
2. **Future Milestones**: Using subsequent hearing dates or decision timestamps to predict early-stage duration.
3. **Global Historical Aggregates**: Computing judge/court average delay across the *entire* 2010–2018 dataset and applying those averages to cases filed in 2010.

This audit establishes a strict 3-tier feature classification system and defines the mathematical time-windowing rules required for all engineered features.

---

## 2. Comprehensive Column-Level Leakage Audit

### Tier 1: Safe at Filing Stage (Filing-Time Model)
These features are known and recorded at the moment a case is filed and registered in the court registry. They may be used in all models.

| Field / Feature Name | Source Table | Justification | Permitted in Filing Model? |
| :--- | :--- | :--- | :--- |
| `state_code` / `state_name` | `cases_YYYY.csv` / `cases_state_key.csv` | Geographic jurisdiction fixed at filing | **YES** |
| `dist_code` / `district_name` | `cases_YYYY.csv` / `cases_district_key.csv` | District registry fixed at filing | **YES** |
| `court_no` / `court_name` | `cases_YYYY.csv` / `cases_court_key.csv` | Assigned courtroom/complex at filing | **YES** |
| `filing_year` / `filing_month` / `filing_day_of_week` | `date_of_filing` | Extracted strictly from `date_of_filing` | **YES** |
| `judge_position` | `cases_YYYY.csv` | Presiding bench position at filing | **YES** |
| `ddl_filing_judge_id` | `judge_case_merge_key.csv` | Judge assigned at case registration | **YES** |
| `case_type_code` / `case_type_string` | `type_name` / `type_name_key.csv` | Initial case category assigned at filing | **YES** |
| `is_criminal` | `acts_sections.csv` / `type_name_key.csv` | Primary case classification at registration | **YES** |
| `act_codes` / `act_titles` | `acts_sections.csv` / `act_key.csv` | Statutory Acts charged at filing | **YES** |
| `section_codes` / `section_tokens` | `acts_sections.csv` / `section_key.csv` | Statutory Sections listed in FIR / Plaint | **YES** |
| `statutory_act_count` | Aggregated from `acts_sections.csv` | Number of distinct legal Acts cited | **YES** |
| `ipc_section_count` | Aggregated from `acts_sections.csv` | Number of IPC sections charged | **YES** |
| `bailable_ipc` | `acts_sections.csv` | Legal bail classification at filing | **YES** |
| `female_defendant` | `cases_YYYY.csv` | Demographic party indicator at filing | **YES** |
| `female_petitioner` | `cases_YYYY.csv` | Demographic party indicator at filing | **YES** |
| `female_adv_def` | `cases_YYYY.csv` | Defense counsel gender flag at filing | **YES** |
| `female_adv_pet` | `cases_YYYY.csv` | Petitioner counsel gender flag at filing | **YES** |
| `judge_gender` | `judges_clean.csv` | Gender of filing judge | **YES** |
| `judge_prior_tenure_days` | Computed chronologically | Tenure prior to `date_of_filing` | **YES (Time-Safe)** |
| `court_prior_backlog_count` | Computed chronologically | Active cases in court as-of `date_of_filing` | **YES (Time-Safe)** |
| `court_prior_delay_rate` | Computed chronologically | Rate among cases resolved before `date_of_filing` | **YES (Time-Safe)** |
| `tfidf_legal_tokens` | Vectorized text from filing fields | Fit strictly on training split | **YES (Time-Safe)** |

---

### Tier 2: In-Progress / Hearing Stage Features (Hearing Model Only)
These features become available only after the case has undergone one or more preliminary hearings. **They MUST NOT be used in the initial Filing-Time Model.**

| Field / Feature Name | Source Table | Stage Available | Permitted in Filing Model? | Permitted in Hearing Model? |
| :--- | :--- | :--- | :--- | :--- |
| `date_first_list` | `cases_YYYY.csv` | First listing date | **NO (LEAKAGE)** | **YES** |
| `filing_to_first_list_days` | `date_first_list - date_of_filing` | First hearing gap | **NO (LEAKAGE)** | **YES** |
| `purpose_name` / `purpose_string` | `cases_YYYY.csv` | Current hearing stage | **NO (LEAKAGE)** | **YES** |
| `date_last_list` | `cases_YYYY.csv` | Last hearing date | **NO (LEAKAGE)** | **YES (As of snapshot)** |
| `date_next_list` | `cases_YYYY.csv` | Next scheduled hearing | **NO (LEAKAGE)** | **YES (As of snapshot)** |
| `hearing_span_days` | `date_last_list - date_first_list` | Hearing duration span | **NO (LEAKAGE)** | **YES** |
| `next_listing_gap_days` | `date_next_list - date_last_list` | Next listing interval | **NO (LEAKAGE)** | **YES** |

---

### Tier 3: Post-Disposal Fields & Ground Truth Targets (STRICTLY PROHIBITED AS FEATURES)
These fields represent the outcome or the mathematical definition of the ground truth target. **Using any of these fields as an input feature constitutes fatal scientific leakage.**

| Field / Target Name | Source Table | Risk Description | Usage Policy |
| :--- | :--- | :--- | :--- |
| `date_of_decision` | `cases_YYYY.csv` | Final decision timestamp | **PROHIBITED (Used ONLY to compute target `duration_days`)** |
| `disp_name` / `disp_name_s` | `cases_YYYY.csv` / `disp_name_key.csv` | Final judgment outcome (e.g. *acquitted, dismissed*) | **STRICTLY PROHIBITED (Post-hoc outcome)** |
| `ddl_decision_judge_id` | `judge_case_merge_key.csv` | Judge presiding at final disposition | **STRICTLY PROHIBITED (Disposal-time fact)** |
| `case_duration_days` | `date_of_decision - date_of_filing` | Primary Regression Target | **TARGET ONLY** |
| `delay_24m` | `case_duration_days > 730.5` | Primary Binary Classification Target | **TARGET ONLY** |
| `delay_12m` / `delay_36m` | `case_duration_days > 365.25 / 1095.75` | Sensitivity Analysis Targets | **TARGET ONLY** |

---

## 3. Strict Chronological Windowing for Historical Features

To prevent look-ahead bias in historical statistics (e.g., judge historical delay rate, court congestion), the following mathematical rules are enforced:

### Rule 1: Expanding Historical Window
For any case $i$ filed on date $T_i = \text{date\_of\_filing}_i$ in court $C_i$:
$$\text{court\_prior\_delay\_rate}(i) = \frac{\sum_{j \in S(i)} \mathbb{I}(\text{duration}_j > 730.5)}{|S(i)|}$$
Where the eligible historical case set $S(i)$ is defined strictly as:
$$S(i) = \{ j \mid \text{court}_j = C_i \;\land\; \text{date\_of\_decision}_j < T_i \}$$
*Cases decided on or after $T_i$ are mathematically excluded from the numerator and denominator.*

### Rule 2: Minimum Support Smoothing
To avoid extreme noisy estimates for judges or courts with few prior resolved cases, empirical Bayes smoothing is applied:
$$\hat{\mu}_{\text{judge}} = \frac{N_{\text{prior}} \cdot \bar{y}_{\text{prior}} + M \cdot \mu_{\text{global}}}{N_{\text{prior}} + M}$$
Where $M = 30$ cases (prior weight parameter) and $\mu_{\text{global}}$ is the global historical delay rate before $T_i$.

### Rule 3: Temporal Train/Validation/Test Split
Data must **never** be randomly split across time (e.g. random `train_test_split`).
- **Training Cohort**: Cases filed in **2010–2016**
- **Validation Cohort**: Cases filed in **2017**
- **Testing Cohort**: Cases filed in **2018**
*This guarantees that models are tested on strictly future unseen case filings.*
