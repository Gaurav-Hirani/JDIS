# JDIS Phase 4: Feature Group Definition

This document maps the raw features found in `filing_classification_24m_final.parquet` to logical feature groups as defined in `docs/data/DATA_DICTIONARY.md`. This mapping forms the basis of the Phase 4 Feature-Group Ablation Study.

## Group A — Basic Case Features
Represents the fundamental legal, demographic, and chronological constraints known strictly at the time of filing.
- `filing_month`
- `filing_day_of_week`
- `filing_quarter`
- `type_name`
- `case_type_str`
- `case_category`
- `is_criminal_code`
- `statutory_act_count`
- `ipc_section_count`
- `bailable_ipc_flag`
- `primary_act_id`
- `female_defendant_clean`
- `female_petitioner_clean`
- `female_adv_def_clean`
- `female_adv_pet_clean`

## Group B — Court Features
Represents geographic and administrative court jurisdictions.
- `state_code`
- `dist_code`
- `court_no`
- `state_str`
- `district_str`
- `court_str`

## Group C — Judge Features
Represents the individual presiding judge characteristics known at assignment.
- `ddl_filing_judge_id`
- `judge_position_clean`
- `judge_gender`
- `judge_tenure_days`

## Group D — Historical Features
Represents time-safe (expanding-window) aggregate statistics detailing court throughput and historical backlogs before the filing date.
- `court_prior_delay_rate`
- `court_prior_avg_duration`
- `court_prior_active_backlog`
- `casetype_prior_delay_rate`

## Group E — Legal Metadata / NLP Features
Represents high-dimensional unstructured text metadata (e.g. detailed Acts/Sections) reduced via TF-IDF and TruncatedSVD.
- `tfidf_0` through `tfidf_49`

## Group F — Graph Features
Represents localized network metrics drawn from the bipartite judge-court assignment history.
- `judge_court_degree`
- `court_judge_turnover_count`

## Excluded (Leakage / Target)
- `delay_24m`, `delay_12m`, `delay_36m`, `case_duration_days`, `ddl_case_id`, `filing_year`
