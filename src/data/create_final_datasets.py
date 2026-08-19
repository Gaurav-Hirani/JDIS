import pandas as pd
import numpy as np
import os

def main():
    print("Loading cases_clean.parquet for observability rules...")
    raw = pd.read_parquet("data/processed/cases_clean.parquet")
    
    print("Loading filing_features.parquet...")
    feat = pd.read_parquet("data/features/filing_features.parquet")
    
    # We need to compute case-specific follow_up_days to correctly classify 24m targets
    raw['date_of_filing_dt'] = pd.to_datetime(raw['date_of_filing'], errors='coerce')
    raw['is_resolved'] = raw['date_of_decision'].notna()
    
    obs_cols = [c for c in ['date_first_list', 'date_last_list', 'date_next_list'] if c in raw.columns]
    for c in obs_cols:
        raw[c + '_dt'] = pd.to_datetime(raw[c], errors='coerce')
        # Mask out garbage future dates (e.g. 5000-01-01)
        raw.loc[raw[c + '_dt'] > pd.Timestamp('2025-01-01'), c + '_dt'] = pd.NaT
        
    obs_dt_cols = [c + '_dt' for c in obs_cols]
    if obs_dt_cols:
        raw['case_last_observed_date'] = raw[obs_dt_cols].max(axis=1)
    else:
        raw['case_last_observed_date'] = pd.NaT
        
    raw['follow_up_days'] = (raw['case_last_observed_date'] - raw['date_of_filing_dt']).dt.days
    
    # Create the mapping dataframe
    map_df = raw[['ddl_case_id', 'is_resolved', 'follow_up_days']].copy()
    
    # Merge with features
    df = feat.merge(map_df, on='ddl_case_id', how='left')
    
    # Restrict to 2010-2016 primary timeline
    df = df[(df['filing_year'] >= 2010) & (df['filing_year'] <= 2016)].copy()
    
    # --- 1. REGRESSION DATASET ---
    print("Building regression dataset...")
    df_reg = df[df['is_resolved']].copy()
    # Ensure no unresolved cases are passed
    df_reg = df_reg[df_reg['case_duration_days'].notna() & (df_reg['case_duration_days'] >= 0)]
    df_reg.drop(columns=['is_resolved', 'follow_up_days'], inplace=True)
    
    out_reg = "data/features/filing_regression_final.parquet"
    df_reg.to_parquet(out_reg, index=False)
    print(f"Saved {len(df_reg)} records to {out_reg}")
    
    # --- 2. 24-MONTH CLASSIFICATION DATASET ---
    print("Building 24-month classification dataset...")
    # Label 0: Resolved <= 730.5
    # Label 1: Resolved > 730.5 OR (Unresolved AND follow_up > 730.5)
    # UNKNOWN: Unresolved AND follow_up <= 730.5
    
    def get_24m_label(row):
        if row['is_resolved']:
            if pd.notna(row['case_duration_days']):
                return 1 if row['case_duration_days'] > 730.5 else 0
            else:
                return np.nan
        else:
            if pd.notna(row['follow_up_days']) and row['follow_up_days'] > 730.5:
                return 1
            else:
                return np.nan # UNKNOWN
                
    df['final_delay_24m'] = df.apply(get_24m_label, axis=1)
    
    # Drop UNKNOWN
    df_clf = df[df['final_delay_24m'].notna()].copy()
    df_clf['final_delay_24m'] = df_clf['final_delay_24m'].astype(int)
    
    # Drop intermediate columns
    df_clf.drop(columns=['is_resolved', 'follow_up_days', 'delay_24m', 'delay_12m', 'delay_36m', 'case_duration_days'], inplace=True, errors='ignore')
    # Rename target to standardized column name for pipeline
    df_clf.rename(columns={'final_delay_24m': 'delay_24m'}, inplace=True)
    
    out_clf = "data/features/filing_classification_24m_final.parquet"
    df_clf.to_parquet(out_clf, index=False)
    print(f"Saved {len(df_clf)} records to {out_clf}")
    
if __name__ == '__main__':
    main()
