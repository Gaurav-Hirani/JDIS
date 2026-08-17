"""
JDIS Master Feature Pipeline Orchestrator
Builds and exports:
1. data/processed/cases_clean.parquet
2. data/features/filing_features.parquet (Dataset A - Filing-Time Model)
3. data/features/ongoing_features.parquet (Dataset B - Ongoing-Case Model)
4. data/features/hearing_features.parquet (Dataset C - Next-Listing Delay Model)
"""

import pandas as pd
import numpy as np
import os
import glob
import logging
from src.data.clean import clean_cases_data
from src.data.join import load_lookup_keys, enrich_cases_data
from src.features.historical import compute_time_safe_court_features, compute_time_safe_casetype_features
from src.features.text_features import generate_tfidf_features
from src.features.graph_features import compute_judge_court_graph_features

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def run_feature_pipeline(cases_glob: str = 'data/extracted/cases_sample/*.csv',
                         keys_dir: str = 'data/extracted/keys',
                         judges_file: str = 'data/extracted/judges_clean/judges_clean.csv',
                         acts_file: str = 'data/extracted/acts_sections_sample.csv',
                         output_processed_dir: str = 'data/processed',
                         output_features_dir: str = 'data/features'):
    """
    Executes the end-to-end cleaning, joining, feature engineering, and parquet generation pipeline.
    """
    logger.info("==================================================")
    logger.info("STARTING JDIS REPRODUCIBLE FEATURE PIPELINE")
    logger.info("==================================================")
    
    os.makedirs(output_processed_dir, exist_ok=True)
    os.makedirs(output_features_dir, exist_ok=True)

    # 1. Ingestion of Sample Cases
    case_files = sorted(glob.glob(cases_glob))
    logger.info(f"Loading {len(case_files)} case sample files from {cases_glob}...")
    dfs = [pd.read_csv(f, low_memory=False) for f in case_files]
    raw_cases_df = pd.concat(dfs, ignore_index=True)
    logger.info(f"Loaded {len(raw_cases_df):,} raw case records.")

    # 2. Cleaning & Timeline Validation
    cleaned_df = clean_cases_data(raw_cases_df)

    # 3. Load Auxiliary Key & Relational Tables
    keys = load_lookup_keys(keys_dir)
    
    judges_df = pd.read_csv(judges_file) if os.path.exists(judges_file) else None
    
    jmerge_path = os.path.join(keys_dir, 'judge_case_merge_key.csv')
    judge_merge_df = pd.read_csv(jmerge_path, nrows=500000) if os.path.exists(jmerge_path) else None
    
    acts_df = pd.read_csv(acts_file, low_memory=False) if os.path.exists(acts_file) else None

    # 4. Relational Joins & 4-Tier Civil/Criminal Classification
    enriched_df = enrich_cases_data(
        cases_df=cleaned_df,
        keys=keys,
        acts_df=acts_df,
        judges_df=judges_df,
        judge_merge_df=judge_merge_df
    )

    # Save Cleaned Master Table
    processed_master_path = os.path.join(output_processed_dir, 'cases_clean.parquet')
    enriched_df.to_parquet(processed_master_path, index=False)
    logger.info(f"Exported clean master dataset to {processed_master_path} ({os.path.getsize(processed_master_path)/(1024*1024):.2f} MB)")

    # 5. Compute Time-Safe Historical Features (Chronological Expanding Window)
    df_with_hist = compute_time_safe_court_features(enriched_df, prior_weight=30.0)
    df_with_hist = compute_time_safe_casetype_features(df_with_hist, prior_weight=20.0)

    # 6. Compute Judge-Court Bipartite Graph Features
    df_with_graph = compute_judge_court_graph_features(df_with_hist, judges_df)

    # 7. Generate NLP TF-IDF Features (fit strictly on Train: filing_year <= 2016)
    train_mask = (df_with_graph['filing_year'] <= 2016)
    tfidf_df = generate_tfidf_features(
        df=df_with_graph,
        train_mask=train_mask,
        n_components=50,
        artifacts_dir=output_features_dir
    )
    
    # Merge TF-IDF onto feature matrix
    df_full = pd.concat([df_with_graph.reset_index(drop=True), tfidf_df.reset_index(drop=True)], axis=1)

    # 8. Assemble & Export Dataset A (Filing-Time Prediction)
    logger.info("Assembling Dataset A: Filing-Time Prediction Matrix...")
    filing_cols = [
        # Identifiers & Split
        'ddl_case_id', 'filing_year',
        # Geographic / Court
        'state_code', 'dist_code', 'court_no', 'state_str', 'district_str', 'court_str',
        # Calendar (Tier A)
        'filing_month', 'filing_day_of_week', 'filing_quarter',
        # Bench / Judge
        'judge_position_clean', 'ddl_filing_judge_id', 'judge_gender',
        # Case Type & Law
        'type_name', 'case_type_str', 'case_category', 'is_criminal_code',
        'statutory_act_count', 'ipc_section_count', 'bailable_ipc_flag', 'primary_act_id',
        # Demographics
        'female_defendant_clean', 'female_petitioner_clean', 'female_adv_def_clean', 'female_adv_pet_clean',
        # Time-Safe Historical Features
        'court_prior_delay_rate', 'court_prior_avg_duration', 'court_prior_active_backlog', 'casetype_prior_delay_rate',
        # Graph Features
        'judge_court_degree', 'judge_tenure_days', 'court_judge_turnover_count',
        # Targets (for supervised modeling / evaluation)
        'case_duration_days', 'delay_24m', 'delay_12m', 'delay_36m'
    ] + [f"tfidf_{i}" for i in range(50)]

    dataset_a = df_full[[c for c in filing_cols if c in df_full.columns]].copy()
    dataset_a_path = os.path.join(output_features_dir, 'filing_features.parquet')
    dataset_a.to_parquet(dataset_a_path, index=False)
    logger.info(f"Dataset A exported to {dataset_a_path} (Shape: {dataset_a.shape})")

    # 9. Assemble & Export Dataset B (Ongoing-Case Prediction)
    logger.info("Assembling Dataset B: Ongoing-Case Prediction Matrix...")
    ongoing_df = df_full.copy()
    ongoing_df['filing_to_first_list_days'] = np.where(
        ongoing_df['date_first_list_dt'].notna(),
        (ongoing_df['date_first_list_dt'] - ongoing_df['date_of_filing_dt']).dt.days.clip(lower=0),
        np.nan
    )
    ongoing_cols = filing_cols.copy()
    ongoing_cols.insert(ongoing_cols.index('case_duration_days'), 'filing_to_first_list_days')
    dataset_b = ongoing_df[[c for c in ongoing_cols if c in ongoing_df.columns]].copy()
    dataset_b_path = os.path.join(output_features_dir, 'ongoing_features.parquet')
    dataset_b.to_parquet(dataset_b_path, index=False)
    logger.info(f"Dataset B exported to {dataset_b_path} (Shape: {dataset_b.shape})")

    # 10. Assemble & Export Dataset C (Hearing & Next-Listing Delay Prediction)
    logger.info("Assembling Dataset C: Hearing / Next-Listing Delay Matrix...")
    hearing_df = df_full.copy()
    hearing_df['days_since_filing_at_last_list'] = np.where(
        hearing_df['date_last_list_dt'].notna(),
        (hearing_df['date_last_list_dt'] - hearing_df['date_of_filing_dt']).dt.days.clip(lower=0),
        np.nan
    )
    hearing_cols = [
        'ddl_case_id', 'filing_year',
        'state_code', 'dist_code', 'court_no', 'state_str', 'district_str', 'court_str',
        'case_type_str', 'case_category', 'is_criminal_code',
        'purpose_str', 'judge_position_clean',
        'days_since_filing_at_last_list', 'hearing_span_days',
        'court_prior_delay_rate', 'court_prior_active_backlog',
        # Targets for Next-Listing Delay
        'next_listing_gap_days', 'hearing_continuation_risk'
    ]
    dataset_c = hearing_df[[c for c in hearing_cols if c in hearing_df.columns]].copy()
    dataset_c_path = os.path.join(output_features_dir, 'hearing_features.parquet')
    dataset_c.to_parquet(dataset_c_path, index=False)
    logger.info(f"Dataset C exported to {dataset_c_path} (Shape: {dataset_c.shape})")

    logger.info("==================================================")
    logger.info("ALL JDIS DATASETS GENERATED SUCCESSFULLY")
    logger.info("==================================================")
    return {
        'clean_master_shape': enriched_df.shape,
        'dataset_a_shape': dataset_a.shape,
        'dataset_b_shape': dataset_b.shape,
        'dataset_c_shape': dataset_c.shape
    }

if __name__ == '__main__':
    run_feature_pipeline()
