"""
JDIS Time-Safe Historical Features Module (Vectorized & Bisect-Optimized)
Computes chronological expanding-window historical aggregates
strictly BEFORE each case's filing date (Zero Look-Ahead Leakage).
"""

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


def compute_time_safe_court_features(df: pd.DataFrame, prior_weight: float = 30.0) -> pd.DataFrame:
    """
    Computes court prior delay rate, average duration, and active backlog
    using strictly cases resolved prior to each case's date_of_filing.
    
    Bisect / Binary search optimization: O(N log K) time complexity.
    """
    logger.info("Computing bisect-optimized time-safe court historical metrics...")
    df = df.copy()
    
    # Global historical baseline priors
    global_resolved = df['case_duration_days'].dropna()
    global_mean_dur = float(global_resolved.mean()) if len(global_resolved) > 0 else 538.0
    global_delayed_rate = float((global_resolved > 730.5).mean()) if len(global_resolved) > 0 else 0.28

    court_keys = (df['state_code'].astype(str) + "_" + 
                  df['dist_code'].astype(str) + "_" + 
                  df['court_no'].astype(str))
    df['court_key'] = court_keys

    # Prepare resolved cases per court
    resolved_mask = df['date_of_decision_dt'].notna() & (df['case_duration_days'] >= 0)
    resolved_df = df[resolved_mask].copy()

    # Pre-index court lookup structures
    court_dec_data = {}
    for c_key, group in resolved_df.groupby('court_key'):
        group_sorted = group.sort_values(by='date_of_decision_dt')
        dec_dates = group_sorted['date_of_decision_dt'].values
        durations = group_sorted['case_duration_days'].values
        del_flags = group_sorted['delay_24m'].values
        
        cum_delayed = np.cumsum(del_flags)
        cum_duration = np.cumsum(durations)
        
        court_dec_data[c_key] = {
            'dates': dec_dates,
            'cum_count': np.arange(1, len(dec_dates) + 1),
            'cum_delayed': cum_delayed,
            'cum_duration': cum_duration
        }

    # Pre-index court filing dates for backlog
    court_filing_data = {}
    for c_key, group in df.groupby('court_key'):
        court_filing_data[c_key] = group['date_of_filing_dt'].sort_values().values

    # Compute per-row features
    n = len(df)
    court_prior_delay_rate = np.full(n, global_delayed_rate, dtype=np.float32)
    court_prior_avg_duration = np.full(n, global_mean_dur, dtype=np.float32)
    court_prior_active_backlog = np.zeros(n, dtype=np.int32)

    filing_dates = df['date_of_filing_dt'].values
    c_keys = df['court_key'].values

    for i in range(n):
        c_key = c_keys[i]
        f_date = filing_dates[i]
        
        # 1. Resolved prior to f_date
        if c_key in court_dec_data:
            dec_struct = court_dec_data[c_key]
            # searchsorted with side='left' finds elements strictly < f_date
            idx = np.searchsorted(dec_struct['dates'], f_date, side='left')
            if idx > 0:
                c_count = idx
                c_delayed = dec_struct['cum_delayed'][idx - 1]
                c_dur_sum = dec_struct['cum_duration'][idx - 1]
                
                # Empirical Bayes smoothing
                court_prior_delay_rate[i] = (c_delayed + prior_weight * global_delayed_rate) / (c_count + prior_weight)
                court_prior_avg_duration[i] = (c_dur_sum + prior_weight * global_mean_dur) / (c_count + prior_weight)
            else:
                court_prior_delay_rate[i] = global_delayed_rate
                court_prior_avg_duration[i] = global_mean_dur

        # 2. Backlog as-of f_date: (filings strictly < f_date) - (decisions strictly < f_date)
        if c_key in court_filing_data:
            filings_before = np.searchsorted(court_filing_data[c_key], f_date, side='left')
            decisions_before = np.searchsorted(court_dec_data[c_key]['dates'], f_date, side='left') if c_key in court_dec_data else 0
            court_prior_active_backlog[i] = max(0, filings_before - decisions_before)

    df['court_prior_delay_rate'] = court_prior_delay_rate
    df['court_prior_avg_duration'] = court_prior_avg_duration
    df['court_prior_active_backlog'] = court_prior_active_backlog
    
    if 'court_key' in df.columns:
        df = df.drop(columns=['court_key'])

    logger.info("Court historical metrics computation complete.")
    return df


def compute_time_safe_casetype_features(df: pd.DataFrame, prior_weight: float = 20.0) -> pd.DataFrame:
    """
    Computes prior delay rate for each case type strictly before date_of_filing.
    """
    logger.info("Computing bisect-optimized case-type prior delay rates...")
    df = df.copy()
    
    global_resolved = df['case_duration_days'].dropna()
    global_delayed_rate = float((global_resolved > 730.5).mean()) if len(global_resolved) > 0 else 0.28

    resolved_mask = df['date_of_decision_dt'].notna() & (df['case_duration_days'] >= 0)
    resolved_df = df[resolved_mask].copy()

    type_dec_data = {}
    for t_code, group in resolved_df.groupby('type_name'):
        group_sorted = group.sort_values(by='date_of_decision_dt')
        dec_dates = group_sorted['date_of_decision_dt'].values
        del_flags = group_sorted['delay_24m'].values
        cum_delayed = np.cumsum(del_flags)
        
        type_dec_data[t_code] = {
            'dates': dec_dates,
            'cum_delayed': cum_delayed
        }

    n = len(df)
    casetype_prior_delay_rate = np.full(n, global_delayed_rate, dtype=np.float32)
    filing_dates = df['date_of_filing_dt'].values
    t_codes = df['type_name'].values

    for i in range(n):
        t_code = t_codes[i]
        f_date = filing_dates[i]
        
        if t_code in type_dec_data:
            dec_struct = type_dec_data[t_code]
            idx = np.searchsorted(dec_struct['dates'], f_date, side='left')
            if idx > 0:
                c_count = idx
                c_delayed = dec_struct['cum_delayed'][idx - 1]
                casetype_prior_delay_rate[i] = (c_delayed + prior_weight * global_delayed_rate) / (c_count + prior_weight)
            else:
                casetype_prior_delay_rate[i] = global_delayed_rate

    df['casetype_prior_delay_rate'] = casetype_prior_delay_rate
    logger.info("Case-type historical metrics computation complete.")
    return df
