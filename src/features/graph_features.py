"""
JDIS Graph & Bipartite Network Features Module
Computes judge-court bipartite network degree, judge prior tenure days,
and court judicial turnover metrics.
"""

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


def compute_judge_court_graph_features(df: pd.DataFrame, judges_df: pd.DataFrame) -> pd.DataFrame:
    """
    Constructs judge-court bipartite mobility features and merges them onto cases.
    """
    logger.info("Computing Judge-Court bipartite graph features...")
    df = df.copy()
    
    if judges_df is None or len(judges_df) == 0:
        df['judge_court_degree'] = 1
        df['judge_tenure_days'] = 0
        df['court_judge_turnover_count'] = 1
        return df

    judges_df = judges_df.copy()
    judges_df['start_dt'] = pd.to_datetime(judges_df['start_date'], format='%d-%m-%Y', errors='coerce')
    judges_df['end_dt'] = pd.to_datetime(judges_df['end_date'], format='%d-%m-%Y', errors='coerce')
    judges_df['tenure_days'] = (judges_df['end_dt'] - judges_df['start_dt']).dt.days.clip(lower=0).fillna(0)

    # 1. Judge-level metrics
    judge_stats = judges_df.groupby('ddl_judge_id').agg(
        judge_court_degree=('court_no', 'nunique'),
        judge_tenure_days=('tenure_days', 'sum')
    ).reset_index()
    
    # 2. Court-level turnover metrics
    court_keys = (judges_df['state_code'].astype(str) + "_" + 
                  judges_df['dist_code'].astype(str) + "_" + 
                  judges_df['court_no'].astype(str))
    judges_df['court_key'] = court_keys
    court_turnover = judges_df.groupby('court_key')['ddl_judge_id'].nunique().to_dict()

    # Merge onto cases
    df = df.merge(judge_stats, left_on='ddl_filing_judge_id', right_on='ddl_judge_id', how='left')
    df['judge_court_degree'] = df['judge_court_degree'].fillna(1).astype(int)
    df['judge_tenure_days'] = df['judge_tenure_days'].fillna(0).astype(float)
    
    df_court_keys = (df['state_code'].astype(str) + "_" + 
                     df['dist_code'].astype(str) + "_" + 
                     df['court_no'].astype(str))
    df['court_judge_turnover_count'] = df_court_keys.map(court_turnover).fillna(1).astype(int)

    if 'ddl_judge_id' in df.columns:
        df = df.drop(columns=['ddl_judge_id'])

    logger.info("Judge-Court graph features merged.")
    return df
