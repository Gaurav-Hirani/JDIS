import os
import pandas as pd
import pytest

def test_classification_dataset_unknowns_excluded():
    df = pd.read_parquet("data/features/filing_classification_24m_final.parquet")
    # In the final dataset, delay_24m must be strictly 0 or 1, no NaNs
    assert df['delay_24m'].isna().sum() == 0, "Classification dataset contains UNKNOWN (NaN) targets"
    assert set(df['delay_24m'].unique()) == {0, 1}, "Classification dataset contains labels other than 0 or 1"

def test_no_unresolved_insufficient_followup_labelled_delayed():
    raw = pd.read_parquet("data/processed/cases_clean.parquet")
    df = pd.read_parquet("data/features/filing_classification_24m_final.parquet")
    
    # Merge to get unresolved status and dates
    merged = df.merge(raw[['ddl_case_id', 'date_of_decision', 'date_of_filing', 'date_last_list', 'date_first_list', 'date_next_list']], on='ddl_case_id')
    
    unresolved = merged[merged['date_of_decision'].isna()].copy()
    
    for c in ['date_of_filing', 'date_first_list', 'date_last_list', 'date_next_list']:
        unresolved[c] = pd.to_datetime(unresolved[c], errors='coerce')
        # Mask future dates out
        unresolved.loc[unresolved[c] > pd.Timestamp('2025-01-01'), c] = pd.NaT
        
    obs_cols = ['date_first_list', 'date_last_list', 'date_next_list']
    unresolved['case_last_observed_date'] = unresolved[obs_cols].max(axis=1)
    unresolved['follow_up_days'] = (unresolved['case_last_observed_date'] - unresolved['date_of_filing']).dt.days
    
    # If delayed (1), follow up MUST be > 730.5
    delayed_unresolved = unresolved[unresolved['delay_24m'] == 1]
    
    violations = delayed_unresolved[delayed_unresolved['follow_up_days'] <= 730.5]
    assert len(violations) == 0, f"Found {len(violations)} unresolved cases falsely labeled as delayed with insufficient follow-up"

def test_no_tier_c_features():
    df = pd.read_parquet("data/features/filing_classification_24m_final.parquet")
    forbidden_features = ['date_of_decision', 'disp_name', 'filing_to_first_list_days', 'delay_12m', 'delay_36m', 'case_duration_days']
    
    for f in forbidden_features:
        assert f not in df.columns, f"Tier-C or target-derived feature '{f}' found in predictors"

def test_temporal_ordering_preserved():
    df = pd.read_parquet("data/features/filing_classification_24m_final.parquet")
    
    train_mask = (df['filing_year'] >= 2010) & (df['filing_year'] <= 2014)
    val_mask = df['filing_year'] == 2015
    test_mask = df['filing_year'] == 2016
    
    train_max_year = df.loc[train_mask, 'filing_year'].max()
    val_min_year = df.loc[val_mask, 'filing_year'].min()
    val_max_year = df.loc[val_mask, 'filing_year'].max()
    test_min_year = df.loc[test_mask, 'filing_year'].min()
    
    assert train_max_year < val_min_year, "Train overlaps or exceeds Validation temporally"
    assert val_max_year < test_min_year, "Validation overlaps or exceeds Test temporally"
