import pandas as pd
import numpy as np
import os
import glob

def profile_keys():
    print("=== PROFILING STATES ===")
    df_state = pd.read_csv('data/extracted/keys/cases_state_key.csv')
    print(f"Total state mappings: {len(df_state)}")
    print(f"Distinct states: {df_state['state_name'].nunique()}")
    print(f"State list sample: {df_state[['state_code', 'state_name']].drop_duplicates().head(10).to_dict('records')}")

    print("\n=== PROFILING DISTRICTS ===")
    df_dist = pd.read_csv('data/extracted/keys/cases_district_key.csv')
    print(f"Total district records: {len(df_dist)}")
    print(f"Distinct districts: {df_dist['district_name'].nunique()}")
    print(f"Sample districts:\n{df_dist[['state_code', 'dist_code', 'district_name']].drop_duplicates().head(5)}")

    print("\n=== PROFILING COURTS ===")
    df_court = pd.read_csv('data/extracted/keys/cases_court_key.csv')
    print(f"Total court records: {len(df_court)}")
    print(f"Distinct court complexes/numbers: {df_court[['state_code', 'dist_code', 'court_no']].drop_duplicates().shape[0]}")
    print(f"Sample courts:\n{df_court[['state_code', 'dist_code', 'court_no', 'court_name']].drop_duplicates().head(5)}")

    print("\n=== PROFILING DISPOSITION CODES ===")
    df_disp = pd.read_csv('data/extracted/keys/disp_name_key.csv')
    print(f"Total disp records: {len(df_disp)}, Distinct disp codes: {df_disp['disp_name'].nunique()}")
    top_disp = df_disp.groupby('disp_name_s')['count'].sum().sort_values(ascending=False).head(15)
    print("Top Dispositions across years:")
    for name, cnt in top_disp.items():
        print(f"  - {name}: {cnt:,}")

    print("\n=== PROFILING CASE TYPES ===")
    df_type = pd.read_csv('data/extracted/keys/type_name_key.csv')
    print(f"Total type records: {len(df_type)}, Distinct type codes: {df_type['type_name'].nunique()}")
    top_types = df_type.groupby('type_name_s')['count'].sum().sort_values(ascending=False).head(15)
    print("Top Case Types across years:")
    for name, cnt in top_types.items():
        print(f"  - {name}: {cnt:,}")

    print("\n=== PROFILING PURPOSE OF HEARINGS ===")
    df_purp = pd.read_csv('data/extracted/keys/purpose_name_key.csv')
    print(f"Total purpose records: {len(df_purp)}, Distinct purpose codes: {df_purp['purpose_name'].nunique()}")
    top_purp = df_purp.groupby('purpose_name_s')['count'].sum().sort_values(ascending=False).head(15)
    print("Top Hearing Purposes across years:")
    for name, cnt in top_purp.items():
        print(f"  - {name}: {cnt:,}")

    print("\n=== PROFILING JUDGES ===")
    df_judges = pd.read_csv('data/extracted/judges_clean/judges_clean.csv')
    print(f"Total judge appointment records: {len(df_judges)}")
    print(f"Unique judge IDs: {df_judges['ddl_judge_id'].nunique()}")
    print(f"Judge gender distribution:\n{df_judges['female_judge'].value_counts(dropna=False)}")
    print(f"Top judge positions:\n{df_judges['judge_position'].value_counts().head(10)}")

    print("\n=== PROFILING JUDGE-CASE MERGE ===")
    df_jmerge = pd.read_csv('data/extracted/keys/judge_case_merge_key.csv', nrows=100000)
    print(f"Sample judge merge rows:\n{df_jmerge.head(5)}")
    print(f"Filing judge nulls in sample: {df_jmerge['ddl_filing_judge_id'].isna().mean():.2%}")
    print(f"Decision judge nulls in sample: {df_jmerge['ddl_decision_judge_id'].isna().mean():.2%}")
    print(f"Filing == Decision judge rate in sample: {(df_jmerge['ddl_filing_judge_id'] == df_jmerge['ddl_decision_judge_id']).mean():.2%}")

if __name__ == '__main__':
    profile_keys()
