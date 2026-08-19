# Dataset C Feature Specification

## 1. Prediction Point Definition
The Next-Listing Delay Model operates exactly at the conclusion of a case hearing.
- **Prediction Point**: $T_{\text{last\_list}}$
- **Target**: `next_listing_gap_days` (`date_next_list - date_last_list`)

## 2. Approved Features
The following features from the `data/features/hearing_features.parquet` matrix have been audited and cleared for use, representing only information explicitly known at $T_{\text{last\_list}}$.

### Tier A (Available at Filing)
- **Geographic/Administrative**: `state_code`, `dist_code`, `court_no`
- **Categorical Meta**: `state_str`, `district_str`, `court_str`, `case_type_str`, `case_category`
- **Legal Profile**: `is_criminal_code`
- **Judge Context**: `judge_position_clean`
- **Historical Dynamics**: `court_prior_delay_rate`, `court_prior_active_backlog`

### Tier B (Available at Current Hearing)
- **Time Since Origin**: `days_since_filing_at_last_list` (Total case age today)
- **Active Proceeding Age**: `hearing_span_days` (Days between first listing and today)
- **Hearing Purpose**: `purpose_str` (The procedural goal of today's hearing, e.g., "Evidence", "Arguments")

## 3. Prohibited Exclusions
The following fields are strictly prohibited to prevent data leakage:
- `date_next_list`
- `date_of_decision`
- `disp_name` / `disp_str`
- `case_duration_days`
- `delay_24m`
