import pandas as pd
import numpy as np
import os
import glob
import json

def generate_full_metrics():
    # Load cases
    case_files = sorted(glob.glob('data/extracted/cases_sample/*.csv'))
    dfs = [pd.read_csv(f, low_memory=False) for f in case_files]
    cases_df = pd.concat(dfs, ignore_index=True)
    
    # Dates
    cases_df['filing_dt'] = pd.to_datetime(cases_df['date_of_filing'], errors='coerce')
    cases_df['decision_dt'] = pd.to_datetime(cases_df['date_of_decision'], errors='coerce')
    cases_df['first_list_dt'] = pd.to_datetime(cases_df['date_first_list'], errors='coerce')
    cases_df['last_list_dt'] = pd.to_datetime(cases_df['date_last_list'], errors='coerce')
    cases_df['next_list_dt'] = pd.to_datetime(cases_df['date_next_list'], errors='coerce')
    
    cases_df['duration_days'] = (cases_df['decision_dt'] - cases_df['filing_dt']).dt.days
    
    valid_resolved = cases_df[cases_df['decision_dt'].notna() & (cases_df['duration_days'] >= 0)]
    
    # State key
    state_key = pd.read_csv('data/extracted/keys/cases_state_key.csv')
    court_key = pd.read_csv('data/extracted/keys/cases_court_key.csv')
    judges = pd.read_csv('data/extracted/judges_clean/judges_clean.csv')
    
    metrics = {
        'total_cases_sampled': len(cases_df),
        'years_covered': sorted(cases_df['year'].unique().tolist()),
        'disposed_count': int(cases_df['decision_dt'].notna().sum()),
        'disposed_pct': float(round(cases_df['decision_dt'].notna().mean() * 100, 2)),
        'pending_count': int(cases_df['decision_dt'].isna().sum()),
        'pending_pct': float(round(cases_df['decision_dt'].isna().mean() * 100, 2)),
        'invalid_duration_count': int((cases_df['duration_days'] < 0).sum()),
        'valid_resolved_count': len(valid_resolved),
        'duration_stats': {
            'mean_days': float(round(valid_resolved['duration_days'].mean(), 2)),
            'std_days': float(round(valid_resolved['duration_days'].std(), 2)),
            'median_days': float(round(valid_resolved['duration_days'].median(), 2)),
            'q25_days': float(round(valid_resolved['duration_days'].quantile(0.25), 2)),
            'q75_days': float(round(valid_resolved['duration_days'].quantile(0.75), 2)),
            'q90_days': float(round(valid_resolved['duration_days'].quantile(0.90), 2)),
            'q95_days': float(round(valid_resolved['duration_days'].quantile(0.95), 2)),
            'min_days': float(valid_resolved['duration_days'].min()),
            'max_days': float(valid_resolved['duration_days'].max())
        },
        'delay_rates': {
            '12_months_pct': float(round((valid_resolved['duration_days'] > 365.25).mean() * 100, 2)),
            '24_months_pct': float(round((valid_resolved['duration_days'] > 730.5).mean() * 100, 2)),
            '36_months_pct': float(round((valid_resolved['duration_days'] > 1095.75).mean() * 100, 2))
        },
        'hearing_dates_validity': {
            'first_list_valid_pct': float(round(cases_df['first_list_dt'].notna().mean() * 100, 2)),
            'last_list_valid_pct': float(round(cases_df['last_list_dt'].notna().mean() * 100, 2)),
            'next_list_valid_pct': float(round(cases_df['next_list_dt'].notna().mean() * 100, 2)),
            'filing_to_first_median_days': float(round((cases_df['first_list_dt'] - cases_df['filing_dt']).dt.days.median(), 2)),
            'first_to_last_median_days': float(round((cases_df['last_list_dt'] - cases_df['first_list_dt']).dt.days.median(), 2))
        },
        'metadata_counts': {
            'distinct_states': int(state_key['state_name'].nunique()),
            'distinct_districts': int(court_key[['state_code', 'dist_code']].drop_duplicates().shape[0]),
            'distinct_courts': int(court_key[['state_code', 'dist_code', 'court_no']].drop_duplicates().shape[0]),
            'distinct_judges': int(judges['ddl_judge_id'].nunique())
        }
    }
    
    with open('docs/data/full_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    print("Full metrics generated and written to docs/data/full_metrics.json")
    print(json.dumps(metrics, indent=2))

if __name__ == '__main__':
    generate_full_metrics()
