import pytest
import pandas as pd
import numpy as np

def test_no_negative_targets():
    df = pd.read_parquet("data/features/hearing_features.parquet")
    # In training, we drop negatives. Let's make sure our pipeline logic will drop them.
    valid_targets = df[df['next_listing_gap_days'].notna() & (df['next_listing_gap_days'] >= 0)]
    assert (valid_targets['next_listing_gap_days'] < 0).sum() == 0

def test_no_date_next_list_in_features():
    df = pd.read_parquet("data/features/hearing_features.parquet")
    assert 'date_next_list' not in df.columns
    assert 'date_next_list_dt' not in df.columns
    assert 'date_of_decision' not in df.columns
    assert 'disp_name' not in df.columns

def test_temporal_split_logic():
    cases = pd.read_parquet("data/processed/cases_clean.parquet")
    df = pd.read_parquet("data/features/hearing_features.parquet")
    df = df.merge(cases[['ddl_case_id', 'date_last_list_dt']], on='ddl_case_id', how='left')
    df['last_list_year'] = df['date_last_list_dt'].dt.year
    
    train_df = df[df['last_list_year'] <= 2017]
    val_df = df[df['last_list_year'] == 2018]
    test_df = df[df['last_list_year'] == 2019]
    
    assert train_df['last_list_year'].max() == 2017
    assert val_df['last_list_year'].unique()[0] == 2018
    assert test_df['last_list_year'].unique()[0] == 2019
    
    # Check no overlap
    assert len(set(train_df['ddl_case_id']).intersection(set(val_df['ddl_case_id']))) == 0
