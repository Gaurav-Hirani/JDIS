"""
JDIS Data Cleaning & Standardization Module
Applies deterministic date sanitization, demographic normalization,
invalid timeline removal, and target variable construction.
"""

import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

STANDARD_JUDGE_POSITIONS = {
    'district and sessions court': 'district_and_sessions',
    'chief judicial magistrate': 'chief_judicial_magistrate',
    'civil judge senior division': 'civil_judge_senior',
    'civil judge junior division': 'civil_judge_junior',
    'civil court': 'civil_court',
    'judicial magistrate court': 'judicial_magistrate',
    'additional chief judicial magistrate': 'addl_cjm',
    'city civil and sessions court': 'city_civil_sessions',
    'additional district and sessions court': 'addl_district_sessions',
    'family court': 'family_court',
}


def clean_cases_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw case records, standardizes columns, validates timelines,
    and constructs ground-truth target variables.
    """
    initial_rows = len(df)
    logger.info(f"Starting data cleaning on {initial_rows:,} records.")

    # 1. Standardize column names
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    # 2. Parse Date Columns
    date_cols = ['date_of_filing', 'date_of_decision', 'date_first_list', 'date_last_list', 'date_next_list']
    for col in date_cols:
        if col in df.columns:
            df[col + '_dt'] = pd.to_datetime(df[col], errors='coerce')

    # 3. Filter impossible date sequences
    # date_of_filing must be present and valid
    valid_filing_mask = df['date_of_filing_dt'].notna()
    df = df[valid_filing_mask]
    
    # If decision date is present, it must be >= filing date
    has_decision = df['date_of_decision_dt'].notna()
    invalid_decision_mask = has_decision & (df['date_of_decision_dt'] < df['date_of_filing_dt'])
    dropped_decision_inversions = invalid_decision_mask.sum()
    df = df[~invalid_decision_mask]

    # If first list date is present, it should not precede filing by more than 30 days (clerical typo threshold)
    has_first_list = df['date_first_list_dt'].notna()
    invalid_first_list = has_first_list & (df['date_first_list_dt'] < (df['date_of_filing_dt'] - pd.Timedelta(days=30)))
    df = df[~invalid_first_list]

    logger.info(f"Filtered {dropped_decision_inversions} inverted decision dates. Rows remaining: {len(df):,}")

    # 4. Standardize Demographics
    def clean_gender_string(val):
        if pd.isna(val):
            return 'UNKNOWN'
        s = str(val).lower().strip()
        if 'female' in s and 'non' not in s and '0' not in s:
            return 'FEMALE'
        elif 'male' in s or '0 nonfemale' in s:
            return 'MALE'
        elif 'unclear' in s or '-9998' in s:
            return 'UNCLEAR'
        elif 'missing' in s or '-9999' in s:
            return 'MISSING'
        return 'OTHER'

    def clean_adv_code(val):
        if pd.isna(val):
            return -1
        try:
            v = int(val)
            if v == 1:
                return 1
            elif v == 0:
                return 0
            elif v == -9998:
                return -2  # unclear
            elif v == -9999:
                return -1  # missing
            return -1
        except (ValueError, TypeError):
            return -1

    if 'female_defendant' in df.columns:
        df['female_defendant_clean'] = df['female_defendant'].apply(clean_gender_string)
    if 'female_petitioner' in df.columns:
        df['female_petitioner_clean'] = df['female_petitioner'].apply(clean_gender_string)
    if 'female_adv_def' in df.columns:
        df['female_adv_def_clean'] = df['female_adv_def'].apply(clean_adv_code)
    if 'female_adv_pet' in df.columns:
        df['female_adv_pet_clean'] = df['female_adv_pet'].apply(clean_adv_code)

    # 5. Standardize Judge Position
    if 'judge_position' in df.columns:
        def standardize_judge_pos(pos_str):
            if pd.isna(pos_str):
                return 'other'
            s = str(pos_str).lower().strip()
            return STANDARD_JUDGE_POSITIONS.get(s, 'other')
        df['judge_position_clean'] = df['judge_position'].apply(standardize_judge_pos)

    # 6. Construct Ground Truth Targets
    # Duration Target (only for resolved cases)
    df['case_duration_days'] = np.where(
        df['date_of_decision_dt'].notna(),
        (df['date_of_decision_dt'] - df['date_of_filing_dt']).dt.days,
        np.nan
    )
    
    # Binary Delay Targets (Primary 24M, Sensitivity 12M, 36M)
    df['delay_24m'] = np.where(
        df['case_duration_days'].notna(),
        (df['case_duration_days'] > 730.5).astype(int),
        np.nan
    )
    df['delay_12m'] = np.where(
        df['case_duration_days'].notna(),
        (df['case_duration_days'] > 365.25).astype(int),
        np.nan
    )
    df['delay_36m'] = np.where(
        df['case_duration_days'].notna(),
        (df['case_duration_days'] > 1095.75).astype(int),
        np.nan
    )

    # Next-Listing Delay Target (as of last listing)
    df['next_listing_gap_days'] = np.where(
        df['date_next_list_dt'].notna() & df['date_last_list_dt'].notna(),
        (df['date_next_list_dt'] - df['date_last_list_dt']).dt.days,
        np.nan
    )
    
    # Hearing Span & Continuation Risk
    df['hearing_span_days'] = np.where(
        df['date_last_list_dt'].notna() & df['date_first_list_dt'].notna(),
        (df['date_last_list_dt'] - df['date_first_list_dt']).dt.days,
        np.nan
    )
    df['hearing_continuation_risk'] = np.where(
        df['hearing_span_days'].notna(),
        (df['hearing_span_days'] > 365.25).astype(int),
        np.nan
    )

    # Calendar Features from Filing Date (Tier A - Safe at filing)
    df['filing_year'] = df['date_of_filing_dt'].dt.year
    df['filing_month'] = df['date_of_filing_dt'].dt.month
    df['filing_day_of_week'] = df['date_of_filing_dt'].dt.dayofweek
    df['filing_quarter'] = df['date_of_filing_dt'].dt.quarter

    logger.info(f"Cleaned dataset shape: {df.shape}. Resolved cases: {df['case_duration_days'].notna().sum():,}")
    return df
