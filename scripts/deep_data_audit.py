import pandas as pd
import numpy as np
import os
import glob
import json

def run_deep_audit():
    print("==================================================")
    print("RUNNING JDIS DEEP DATASET & FEASIBILITY AUDIT")
    print("==================================================")
    
    # 1. Load cases samples (450,000 cases across 2010-2018)
    case_files = sorted(glob.glob('data/extracted/cases_sample/*.csv'))
    dfs = []
    for f in case_files:
        df_year = pd.read_csv(f, low_memory=False)
        dfs.append(df_year)
    cases_df = pd.concat(dfs, ignore_index=True)
    print(f"Loaded {len(cases_df):,} sampled cases across {len(case_files)} years (2010-2018).")
    
    # Check shape and columns
    print(f"Cases columns ({len(cases_df.columns)}): {list(cases_df.columns)}")
    
    # Column missingness & dtypes
    print("\n--- Cases Column Quality & Missingness ---")
    missing_summary = []
    for col in cases_df.columns:
        null_count = cases_df[col].isna().sum()
        null_pct = (null_count / len(cases_df)) * 100
        nunique = cases_df[col].nunique(dropna=True)
        sample_val = str(cases_df[col].dropna().iloc[0]) if nunique > 0 else "N/A"
        missing_summary.append({
            'column': col,
            'dtype': str(cases_df[col].dtype),
            'missing_count': int(null_count),
            'missing_pct': round(null_pct, 2),
            'unique_values': int(nunique),
            'sample_val': sample_val
        })
        print(f"  {col:<20} | Dtype: {str(cases_df[col].dtype):<10} | Nulls: {null_count:>7,} ({null_pct:>5.1f}%) | Unique: {nunique:>7,} | Ex: {sample_val[:30]}")

    # 2. Date Analysis & Target Construction
    print("\n--- Date Analysis & Duration Target ---")
    date_cols = ['date_of_filing', 'date_of_decision', 'date_first_list', 'date_last_list', 'date_next_list']
    for dcol in date_cols:
        cases_df[dcol + '_dt'] = pd.to_datetime(cases_df[dcol], errors='coerce')
        valid_dt = cases_df[dcol + '_dt'].notna().sum()
        print(f"  {dcol:<20} | Valid dates: {valid_dt:>7,} ({(valid_dt/len(cases_df))*100:>5.1f}%) | Min: {cases_df[dcol + '_dt'].min()} | Max: {cases_df[dcol + '_dt'].max()}")
        
    # Disposed vs Pending Cases
    disposed_mask = cases_df['date_of_decision_dt'].notna()
    print(f"\nDisposed cases in sample: {disposed_mask.sum():,} ({disposed_mask.mean()*100:.1f}%)")
    print(f"Pending/Undecided cases in sample: {(~disposed_mask).sum():,} ({(~disposed_mask).mean()*100:.1f}%)")
    
    # Calculate duration for disposed cases
    filing_to_decision = (cases_df['date_of_decision_dt'] - cases_df['date_of_filing_dt']).dt.days
    cases_df['duration_days'] = filing_to_decision
    
    # Check invalid dates (decision before filing)
    invalid_dates = (cases_df['duration_days'] < 0)
    print(f"Invalid duration (decision < filing): {invalid_dates.sum():,} ({invalid_dates.mean()*100:.2f}%)")
    
    # Valid resolved cases
    valid_resolved = cases_df[disposed_mask & (cases_df['duration_days'] >= 0)]
    durations = valid_resolved['duration_days']
    print(f"\nValid Resolved Cases for Duration Target: {len(valid_resolved):,}")
    print(f"  Duration Mean: {durations.mean():.1f} days ({durations.mean()/365.25:.2f} years)")
    print(f"  Duration Median: {durations.median():.1f} days ({durations.median()/30.4375:.1f} months)")
    print(f"  Duration Std: {durations.std():.1f} days")
    print(f"  Duration Min: {durations.min():.0f} days, Max: {durations.max():.0f} days")
    print(f"  Quantiles: 25%={durations.quantile(0.25):.0f}d, 50%={durations.quantile(0.50):.0f}d, 75%={durations.quantile(0.75):.0f}d, 90%={durations.quantile(0.90):.0f}d, 95%={durations.quantile(0.95):.0f}d")
    
    # Delay Thresholds
    print("\n--- Delay Classification Target Feasibility ---")
    threshold_12m = 365.25
    threshold_24m = 730.5
    threshold_36m = 1095.75
    
    d12 = (durations > threshold_12m).mean() * 100
    d24 = (durations > threshold_24m).mean() * 100
    d36 = (durations > threshold_36m).mean() * 100
    
    print(f"  12-month delay rate (>365 days): {d12:.1f}% delayed vs {100-d12:.1f}% on-time")
    print(f"  24-month delay rate (>730 days) [PRIMARY TARGET]: {d24:.1f}% delayed vs {100-d24:.1f}% on-time")
    print(f"  36-month delay rate (>1095 days): {d36:.1f}% delayed vs {100-d36:.1f}% on-time")

    # 3. Hearing Dates Analysis (Adjournment Feasibility)
    print("\n--- Hearing Dates & Adjournment Feasibility Analysis ---")
    print("Checking hearing summary dates in cases_df:")
    has_first_list = cases_df['date_first_list_dt'].notna()
    has_last_list = cases_df['date_last_list_dt'].notna()
    has_next_list = cases_df['date_next_list_dt'].notna()
    print(f"  Cases with date_first_list: {has_first_list.sum():,} ({has_first_list.mean()*100:.1f}%)")
    print(f"  Cases with date_last_list:  {has_last_list.sum():,} ({has_last_list.mean()*100:.1f}%)")
    print(f"  Cases with date_next_list:  {has_next_list.sum():,} ({has_next_list.mean()*100:.1f}%)")
    
    # Gap between filing and first list
    filing_to_first = (cases_df['date_first_list_dt'] - cases_df['date_of_filing_dt']).dt.days
    print(f"  Filing to First Listing Gap (Median): {filing_to_first.median():.0f} days (Mean: {filing_to_first.mean():.1f} days)")
    
    # Gap between first and last list
    first_to_last = (cases_df['date_last_list_dt'] - cases_df['date_first_list_dt']).dt.days
    print(f"  First Listing to Last Listing Span (Median): {first_to_last.median():.0f} days (Mean: {first_to_last.mean():.1f} days)")

    # 4. Civil vs Criminal Analysis
    print("\n--- Civil vs Criminal Coverage & Feasibility ---")
    acts_df = pd.read_csv('data/extracted/acts_sections_sample.csv', low_memory=False)
    print(f"Loaded {len(acts_df):,} acts_sections sample rows.")
    print(f"Acts/Sections columns: {list(acts_df.columns)}")
    print(f"Acts criminal column value counts:\n{acts_df['criminal'].value_counts(dropna=False)}")
    
    # Merge acts_sections criminal indicator with cases sample
    case_criminal_map = acts_df.groupby('ddl_case_id')['criminal'].max()
    cases_df['criminal_flag_acts'] = cases_df['ddl_case_id'].map(case_criminal_map)
    print(f"\nCases mapped to acts_sections criminal flag:")
    print(f"  Mapped cases in sample: {cases_df['criminal_flag_acts'].notna().sum():,} ({(cases_df['criminal_flag_acts'].notna().mean())*100:.1f}%)")
    print(f"  Criminal == 1: {(cases_df['criminal_flag_acts'] == 1).sum():,} ({((cases_df['criminal_flag_acts'] == 1).mean())*100:.1f}%)")
    print(f"  Criminal == 0: {(cases_df['criminal_flag_acts'] == 0).sum():,} ({((cases_df['criminal_flag_acts'] == 0).mean())*100:.1f}%)")
    print(f"  Unmapped / No Act Section: {cases_df['criminal_flag_acts'].isna().sum():,} ({(cases_df['criminal_flag_acts'].isna().mean())*100:.1f}%)")

    # Case type string analysis
    type_key = pd.read_csv('data/extracted/keys/type_name_key.csv')
    print(f"\nType Name Key sample:\n{type_key.head(5)}")

    # 5. Judge and Court Join Feasibility
    print("\n--- Judge & Court Join Feasibility ---")
    jmerge_sample = pd.read_csv('data/extracted/keys/judge_case_merge_key.csv', nrows=200000)
    print(f"Judge Case Merge sample loaded ({len(jmerge_sample):,} rows).")
    
    # Check match rate with cases sample
    j_filing_map = dict(zip(jmerge_sample['ddl_case_id'], jmerge_sample['ddl_filing_judge_id']))
    j_dec_map = dict(zip(jmerge_sample['ddl_case_id'], jmerge_sample['ddl_decision_judge_id']))
    
    cases_df['filing_judge_id'] = cases_df['ddl_case_id'].map(j_filing_map)
    print(f"Cases with filing judge mapped (in merge sample): {cases_df['filing_judge_id'].notna().sum():,} ({(cases_df['filing_judge_id'].notna().mean())*100:.1f}%)")

    # 6. Party & Advocate Fields (Graph Feasibility)
    print("\n--- Party & Advocate Gender Fields (Graph Feasibility) ---")
    for gcol in ['female_defendant', 'female_petitioner', 'female_adv_def', 'female_adv_pet']:
        print(f"  Value counts for {gcol}:\n{cases_df[gcol].value_counts(dropna=False).head(5)}")

    # Save summary json
    audit_results = {
        'total_cases_sampled': len(cases_df),
        'disposed_cases_pct': float(round(disposed_mask.mean()*100, 2)),
        'valid_resolved_duration_mean_days': float(round(durations.mean(), 2)),
        'valid_resolved_duration_median_days': float(round(durations.median(), 2)),
        'delay_12m_pct': float(round(d12, 2)),
        'delay_24m_pct': float(round(d24, 2)),
        'delay_36m_pct': float(round(d36, 2)),
        'missing_summary': missing_summary
    }
    with open('docs/data/audit_summary.json', 'w') as f:
        json.dump(audit_results, f, indent=2)
    print("\nSaved audit summary to docs/data/audit_summary.json")

if __name__ == '__main__':
    run_deep_audit()
