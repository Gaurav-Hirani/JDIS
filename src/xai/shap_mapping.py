import pandas as pd

def get_parent_and_group(model_feature):
    # Mapping exact prefixes to parent features and groups
    parent_mapping = {
        'filing_month': ('filing_month', 'Basic Case', 'Month of case filing'),
        'filing_day_of_week': ('filing_day_of_week', 'Basic Case', 'Day of the week of case filing'),
        'filing_quarter': ('filing_quarter', 'Basic Case', 'Quarter of case filing'),
        'type_name_': ('type_name', 'Basic Case', 'Granular case type name identifier'),
        'case_type_str_': ('case_type_str', 'Basic Case', 'Standardized case type string'),
        'case_category': ('case_category', 'Basic Case', 'Case category ID'),
        'is_criminal_code': ('is_criminal_code', 'Basic Case', 'Civil vs Criminal code (1=Criminal, 0=Civil)'),
        'statutory_act_count': ('statutory_act_count', 'Basic Case', 'Number of statutory acts involved'),
        'ipc_section_count': ('ipc_section_count', 'Basic Case', 'Number of IPC sections cited'),
        'bailable_ipc_flag': ('bailable_ipc_flag', 'Basic Case', 'Indicator if IPC sections are bailable'),
        'primary_act_id_': ('primary_act_id', 'Basic Case', 'Primary statutory act ID'),
        'female_defendant_clean': ('female_defendant_clean', 'Basic Case', 'Indicator for female defendant presence'),
        'female_petitioner_clean': ('female_petitioner_clean', 'Basic Case', 'Indicator for female petitioner presence'),
        'female_adv_def_clean': ('female_adv_def_clean', 'Basic Case', 'Indicator for female defense advocate'),
        'female_adv_pet_clean': ('female_adv_pet_clean', 'Basic Case', 'Indicator for female petitioner advocate'),
        'state_code_': ('state_code', 'Court', 'State code identifier'),
        'dist_code_': ('dist_code', 'Court', 'District code identifier'),
        'court_no_': ('court_no', 'Court', 'Numeric court identifier'),
        'state_str_': ('state_str', 'Court', 'State name string'),
        'district_str_': ('district_str', 'Court', 'District name string'),
        'court_str_': ('court_str', 'Court', 'Court establishment name string'),
        'ddl_filing_judge_id_': ('ddl_filing_judge_id', 'Judge', 'Filing judge identifier'),
        'judge_position_clean_': ('judge_position_clean', 'Judge', 'Standardized judge position'),
        'judge_gender_': ('judge_gender', 'Judge', 'Judge gender'),
        'judge_tenure_days': ('judge_tenure_days', 'Judge', 'Judge tenure duration at filing'),
        'court_prior_delay_rate': ('court_prior_delay_rate', 'Historical', 'Historical delay rate of the court at filing'),
        'court_prior_avg_duration': ('court_prior_avg_duration', 'Historical', 'Historical average duration of the court at filing'),
        'court_prior_active_backlog': ('court_prior_active_backlog', 'Historical', 'Active backlog count of the court at filing'),
        'casetype_prior_delay_rate': ('casetype_prior_delay_rate', 'Historical', 'Historical delay rate for the specific case type')
    }
    
    for prefix, (parent, group, desc) in parent_mapping.items():
        if model_feature.startswith(prefix) or model_feature == parent:
            return parent, group, desc
            
    return 'unknown', 'unknown', 'unknown'

def main():
    shap_df = pd.read_csv('research/results/shap_classification_global.csv')
    
    records = []
    for idx, row in shap_df.iterrows():
        feature = row['Feature']
        mean_shap = row['Mean_Absolute_SHAP']
        
        parent, group, desc = get_parent_and_group(feature)
        
        records.append({
            'model_feature': feature,
            'parent_feature': parent,
            'feature_group': group,
            'human_readable_description': desc,
            'mean_absolute_shap': mean_shap
        })
        
    mapped_df = pd.DataFrame(records)
    
    # Save the detailed mapping
    mapped_df[['model_feature', 'parent_feature', 'feature_group', 'human_readable_description']].to_csv('research/results/shap_feature_mapping.csv', index=False)
    
    # Grouped Summary
    grouped_df = mapped_df.groupby(['feature_group', 'parent_feature', 'human_readable_description'])['mean_absolute_shap'].sum().reset_index()
    grouped_df = grouped_df.sort_values(by='mean_absolute_shap', ascending=False)
    
    grouped_df.to_csv('research/results/shap_grouped_summary.csv', index=False)
    print("SHAP mapping complete.")

if __name__ == '__main__':
    main()
