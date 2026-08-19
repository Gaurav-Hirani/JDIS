# Final JDIS Feature Specification (Config D)

This document lists the exact 29 features utilized in the production Filing-Time Classification and Regression models. All features are strictly "Tier A", meaning they are structurally available and recorded at the time of case filing.

| Feature Name | Group | Type | Meaning | Prediction-Time Availability | Leakage Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `filing_month` | Basic Case | Numeric | Month of case filing | At Filing | Safe |
| `filing_day_of_week` | Basic Case | Numeric | Day of the week of case filing | At Filing | Safe |
| `filing_quarter` | Basic Case | Numeric | Quarter of case filing | At Filing | Safe |
| `type_name` | Basic Case | Categorical | Granular case type name identifier | At Filing | Safe |
| `case_type_str` | Basic Case | Categorical | Standardized case type string | At Filing | Safe |
| `case_category` | Basic Case | Categorical | Broad case category ID | At Filing | Safe |
| `is_criminal_code` | Basic Case | Categorical | Civil vs Criminal code (1=Criminal, 0=Civil) | At Filing | Safe |
| `statutory_act_count` | Basic Case | Numeric | Number of statutory acts involved | At Filing | Safe |
| `ipc_section_count` | Basic Case | Numeric | Number of IPC sections cited | At Filing | Safe |
| `bailable_ipc_flag` | Basic Case | Categorical | Indicator if IPC sections are bailable | At Filing | Safe |
| `primary_act_id` | Basic Case | Categorical | Primary statutory act ID | At Filing | Safe |
| `female_defendant_clean` | Basic Case | Categorical | Indicator for female defendant presence | At Filing | Safe |
| `female_petitioner_clean` | Basic Case | Categorical | Indicator for female petitioner presence | At Filing | Safe |
| `female_adv_def_clean` | Basic Case | Categorical | Indicator for female defense advocate | At Filing | Safe |
| `female_adv_pet_clean` | Basic Case | Categorical | Indicator for female petitioner advocate | At Filing | Safe |
| `state_code` | Court | Categorical | State code identifier | At Filing | Safe |
| `dist_code` | Court | Categorical | District code identifier | At Filing | Safe |
| `court_no` | Court | Categorical | Numeric court identifier | At Filing | Safe |
| `state_str` | Court | Categorical | State name string | At Filing | Safe |
| `district_str` | Court | Categorical | District name string | At Filing | Safe |
| `court_str` | Court | Categorical | Court establishment name string | At Filing | Safe |
| `ddl_filing_judge_id` | Judge | Categorical | Filing judge identifier | At Filing | Safe |
| `judge_position_clean` | Judge | Categorical | Standardized judge position | At Filing | Safe |
| `judge_gender` | Judge | Categorical | Judge gender | At Filing | Safe |
| `judge_tenure_days` | Judge | Numeric | Judge tenure duration at filing | At Filing | Safe |
| `court_prior_delay_rate` | Historical | Numeric | Historical delay rate of the court at filing | At Filing | Safe |
| `court_prior_avg_duration` | Historical | Numeric | Historical average duration of the court at filing | At Filing | Safe |
| `court_prior_active_backlog` | Historical | Numeric | Active backlog count of the court at filing | At Filing | Safe |
| `casetype_prior_delay_rate` | Historical | Numeric | Historical delay rate for the specific case type | At Filing | Safe |
