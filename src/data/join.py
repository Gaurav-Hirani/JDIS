"""
JDIS Relational Join & Feature Enrichment Module
Joins lookup keys, judge appointments, and legal acts/sections.
"""

import pandas as pd
import numpy as np
import os
import logging
from src.data.classify_case_type import classify_case_type_string, classify_case_record

logger = logging.getLogger(__name__)


def load_lookup_keys(keys_dir: str = 'data/extracted/keys'):
    """
    Loads normalized lookup dictionaries from keys folder.
    """
    logger.info(f"Loading lookup tables from {keys_dir}...")
    
    # State key
    state_df = pd.read_csv(os.path.join(keys_dir, 'cases_state_key.csv'))
    state_map = dict(zip(state_df['state_code'].astype(str).str.zfill(2), state_df['state_name']))
    state_map_int = dict(zip(state_df['state_code'], state_df['state_name']))
    
    # District key
    dist_df = pd.read_csv(os.path.join(keys_dir, 'cases_district_key.csv'))
    dist_df['key'] = dist_df['state_code'].astype(str) + "_" + dist_df['dist_code'].astype(str)
    dist_map = dict(zip(dist_df['key'], dist_df['district_name']))
    
    # Court key
    court_df = pd.read_csv(os.path.join(keys_dir, 'cases_court_key.csv'))
    court_df['key'] = court_df['state_code'].astype(str) + "_" + court_df['dist_code'].astype(str) + "_" + court_df['court_no'].astype(str)
    court_map = dict(zip(court_df['key'], court_df['court_name']))
    
    # Type key
    type_df = pd.read_csv(os.path.join(keys_dir, 'type_name_key.csv'))
    # Deduplicate by type_name code (most recent / highest frequency)
    type_df_sorted = type_df.sort_values(by='count', ascending=False).drop_duplicates(subset=['type_name'])
    type_str_map = dict(zip(type_df_sorted['type_name'], type_df_sorted['type_name_s']))
    
    # Purpose key
    purp_df = pd.read_csv(os.path.join(keys_dir, 'purpose_name_key.csv'))
    purp_df_sorted = purp_df.sort_values(by='count', ascending=False).drop_duplicates(subset=['purpose_name'])
    purp_str_map = dict(zip(purp_df_sorted['purpose_name'], purp_df_sorted['purpose_name_s']))
    
    # Disp key
    disp_df = pd.read_csv(os.path.join(keys_dir, 'disp_name_key.csv'))
    disp_df_sorted = disp_df.sort_values(by='count', ascending=False).drop_duplicates(subset=['disp_name'])
    disp_str_map = dict(zip(disp_df_sorted['disp_name'], disp_df_sorted['disp_name_s']))
    
    # Act key
    act_df = pd.read_csv(os.path.join(keys_dir, 'act_key.csv'))
    act_str_map = dict(zip(act_df['act'], act_df['act_s']))

    return {
        'state_map': state_map,
        'state_map_int': state_map_int,
        'dist_map': dist_map,
        'court_map': court_map,
        'type_str_map': type_str_map,
        'purp_str_map': purp_str_map,
        'disp_str_map': disp_str_map,
        'act_str_map': act_str_map
    }


def enrich_cases_data(cases_df: pd.DataFrame, 
                      keys: dict,
                      acts_df: pd.DataFrame = None,
                      judges_df: pd.DataFrame = None,
                      judge_merge_df: pd.DataFrame = None) -> pd.DataFrame:
    """
    Enriches cleaned cases dataframe with text descriptions, acts/sections summary,
    judge assignments, and 4-category Civil/Criminal classification.
    """
    df = cases_df.copy()
    logger.info("Enriching cases data with lookup keys and relational tables...")

    # 1. Resolve State, District, Court Names
    df['state_str'] = df['state_code'].astype(str).map(keys['state_map']).fillna(df['state_code'].map(keys['state_map_int'])).fillna('Unknown State')
    
    dist_keys = df['state_code'].astype(str) + "_" + df['dist_code'].astype(str)
    df['district_str'] = dist_keys.map(keys['dist_map']).fillna('Unknown District')
    
    court_keys = df['state_code'].astype(str) + "_" + df['dist_code'].astype(str) + "_" + df['court_no'].astype(str)
    df['court_str'] = court_keys.map(keys['court_map']).fillna('Unknown Court')

    # 2. Resolve Case Type, Purpose, Disposition strings
    df['case_type_str'] = df['type_name'].map(keys['type_str_map']).fillna('Unknown Case Type')
    df['purpose_str'] = df['purpose_name'].map(keys['purp_str_map']).fillna('Unknown Purpose')
    df['disp_str'] = df['disp_name'].map(keys['disp_str_map']).fillna('Unknown Disposition')

    # 3. Join Judge Information if provided
    if judge_merge_df is not None:
        logger.info("Joining judge case merge keys...")
        j_merge_sub = judge_merge_df[judge_merge_df['ddl_case_id'].isin(df['ddl_case_id'])].drop_duplicates(subset=['ddl_case_id'])
        df = df.merge(j_merge_sub[['ddl_case_id', 'ddl_filing_judge_id']], on='ddl_case_id', how='left')
    elif 'ddl_filing_judge_id' not in df.columns:
        df['ddl_filing_judge_id'] = np.nan

    if judges_df is not None and 'ddl_filing_judge_id' in df.columns:
        j_sub = judges_df.drop_duplicates(subset=['ddl_judge_id'])
        j_gender_map = dict(zip(j_sub['ddl_judge_id'], j_sub['female_judge']))
        df['judge_gender'] = df['ddl_filing_judge_id'].map(j_gender_map).fillna('UNKNOWN')
    else:
        df['judge_gender'] = 'UNKNOWN'

    # 4. Aggregate Acts & Sections
    if acts_df is not None:
        logger.info("Aggregating statutory legal acts and sections per case...")
        acts_sub = acts_df[acts_df['ddl_case_id'].isin(df['ddl_case_id'])].copy()
        
        if len(acts_sub) > 0:
            acts_agg = acts_sub.groupby('ddl_case_id').agg(
                statutory_act_count=('act', 'nunique'),
                ipc_section_count=('number_sections_ipc', 'max'),
                bailable_ipc_flag=('bailable_ipc', 'max'),
                criminal_flag_acts=('criminal', 'max'),
                primary_act_id=('act', lambda x: x.mode().iloc[0] if len(x) > 0 else np.nan)
            ).reset_index()
            
            df = df.merge(acts_agg, on='ddl_case_id', how='left')
        else:
            df['statutory_act_count'] = 0
            df['ipc_section_count'] = 0
            df['bailable_ipc_flag'] = -1
            df['criminal_flag_acts'] = np.nan
            df['primary_act_id'] = np.nan
    else:
        df['statutory_act_count'] = 0
        df['ipc_section_count'] = 0
        df['bailable_ipc_flag'] = -1
        df['criminal_flag_acts'] = np.nan
        df['primary_act_id'] = np.nan

    # Fill defaults for missing legal aggregations
    df['statutory_act_count'] = df['statutory_act_count'].fillna(0).astype(int)
    df['ipc_section_count'] = df['ipc_section_count'].fillna(0).astype(int)
    df['bailable_ipc_flag'] = df['bailable_ipc_flag'].fillna(-1).astype(int)

    # 5. Apply 4-Category Civil vs Criminal Classifier
    logger.info("Applying 4-category Civil vs Criminal classification...")
    type_category = df['case_type_str'].apply(classify_case_type_string)
    
    df['case_category'] = [
        classify_case_record(tc, act_id, crim_act)
        for tc, act_id, crim_act in zip(type_category, df['primary_act_id'], df['criminal_flag_acts'])
    ]

    # Binary flag for models: 1 = Criminal, 0 = Civil, -1 = Other/Ambiguous
    category_to_code = {
        'High-Confidence Criminal': 1,
        'High-Confidence Civil': 0,
        'Ambiguous/Mixed': -1,
        'Other/Unknown/Unclassified': -1
    }
    df['is_criminal_code'] = df['case_category'].map(category_to_code).fillna(-1).astype(int)

    logger.info(f"Enrichment complete. Category distribution:\n{df['case_category'].value_counts()}")
    return df
