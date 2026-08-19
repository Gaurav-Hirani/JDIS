import os
import pandas as pd
import numpy as np
import time
import joblib
import matplotlib.pyplot as plt

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import xgboost as xgb

from experiment_utils import (evaluate_regression, evaluate_classification, 
                              register_experiment)

def get_feature_groups():
    groups = {
        'A_Basic': [
            'filing_month', 'filing_day_of_week', 'filing_quarter',
            'type_name', 'case_type_str', 'case_category', 'is_criminal_code',
            'statutory_act_count', 'ipc_section_count', 'bailable_ipc_flag', 'primary_act_id',
            'female_defendant_clean', 'female_petitioner_clean', 'female_adv_def_clean', 'female_adv_pet_clean'
        ],
        'B_Court': [
            'state_code', 'dist_code', 'court_no', 
            'state_str', 'district_str', 'court_str'
        ],
        'C_Judge': [
            'ddl_filing_judge_id', 'judge_position_clean', 
            'judge_gender', 'judge_tenure_days'
        ],
        'D_Historical': [
            'court_prior_delay_rate', 'court_prior_avg_duration', 
            'court_prior_active_backlog', 'casetype_prior_delay_rate'
        ],
        'E_NLP': [f'tfidf_{i}' for i in range(50)],
        'F_Graph': [
            'judge_court_degree', 'court_judge_turnover_count'
        ]
    }
    return groups

def create_pipeline(feature_cols):
    numerical_cols = [c for c in feature_cols if c.startswith('tfidf_') or 
                      'count' in c or 'rate' in c or 'duration' in c or 
                      'backlog' in c or 'days' in c or 'degree' in c or 
                      'month' in c or 'quarter' in c or 'day_of_week' in c]
    categorical_cols = [c for c in feature_cols if c not in numerical_cols]

    num_trans = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    cat_trans = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=True))
    ])
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_trans, numerical_cols),
            ('cat', cat_trans, categorical_cols)
        ])
    return preprocessor, categorical_cols

def plot_ablation(df, metric, title, filename):
    plt.figure(figsize=(10, 6))
    plt.plot(df['Config'], df[metric], marker='o', linewidth=2, markersize=8)
    plt.title(title, fontsize=14)
    plt.xlabel('Feature Configuration', fontsize=12)
    plt.ylabel(metric, fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f"research/figures/{filename}")
    plt.close()

def main():
    os.makedirs("research/results", exist_ok=True)
    os.makedirs("research/figures", exist_ok=True)
    
    print("Loading datasets...")
    df_clf = pd.read_parquet("data/features/filing_classification_24m_final.parquet")
    df_reg = pd.read_parquet("data/features/filing_regression_final.parquet")
    
    train_mask_clf = (df_clf['filing_year'] >= 2010) & (df_clf['filing_year'] <= 2014)
    val_mask_clf = df_clf['filing_year'] == 2015
    test_mask_clf = df_clf['filing_year'] == 2016
    
    train_mask_reg = (df_reg['filing_year'] >= 2010) & (df_reg['filing_year'] <= 2014)
    val_mask_reg = df_reg['filing_year'] == 2015
    test_mask_reg = df_reg['filing_year'] == 2016
    
    groups = get_feature_groups()
    
    ablations = [
        ('A', ['A_Basic']),
        ('B', ['A_Basic', 'B_Court']),
        ('C', ['A_Basic', 'B_Court', 'C_Judge']),
        ('D', ['A_Basic', 'B_Court', 'C_Judge', 'D_Historical']),
        ('E', ['A_Basic', 'B_Court', 'C_Judge', 'D_Historical', 'E_NLP']),
        ('F', ['A_Basic', 'B_Court', 'C_Judge', 'D_Historical', 'E_NLP', 'F_Graph'])
    ]
    
    # ---------------------------------------------------------
    # CLASSIFICATION ABLATION
    # ---------------------------------------------------------
    print("\n=== CLASSIFICATION ABLATION ===")
    clf_val_results = []
    best_clf_metric = -1
    best_clf_config = None
    best_clf_features = None
    
    y_train_clf = df_clf.loc[train_mask_clf, 'delay_24m']
    y_val_clf = df_clf.loc[val_mask_clf, 'delay_24m']
    y_test_clf = df_clf.loc[test_mask_clf, 'delay_24m']
    
    for config_name, group_list in ablations:
        print(f"Training Config {config_name} ({'+'.join(group_list)})...")
        current_features = []
        for g in group_list:
            current_features.extend(groups[g])
            
        X_train = df_clf.loc[train_mask_clf, current_features].copy()
        X_val = df_clf.loc[val_mask_clf, current_features].copy()
        
        preprocessor, cat_cols = create_pipeline(current_features)
        X_train[cat_cols] = X_train[cat_cols].astype(str)
        X_val[cat_cols] = X_val[cat_cols].astype(str)
        
        model = xgb.XGBClassifier(n_estimators=200, max_depth=6, learning_rate=0.1, n_jobs=-1, random_state=42)
        pipe = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])
        
        start_time = time.time()
        pipe.fit(X_train, y_train_clf)
        runtime = time.time() - start_time
        
        metrics = evaluate_classification(pipe, X_val, y_val_clf, f"abl_{config_name}", config_name)
        clf_val_results.append({
            'Config': config_name, 
            'Groups': '+'.join([g.split('_')[1] for g in group_list]),
            'Feature Count': len(current_features),
            'Runtime (s)': runtime,
            **metrics
        })
        
        # Determine best on Validation (PR-AUC)
        if metrics['PR-AUC'] > best_clf_metric:
            best_clf_metric = metrics['PR-AUC']
            best_clf_config = config_name
            best_clf_features = current_features
            joblib.dump(pipe, "models/best_ablation_clf.joblib")
            
    clf_res_df = pd.DataFrame(clf_val_results)
    clf_res_df['ΔPR-AUC'] = clf_res_df['PR-AUC'].diff().fillna(0)
    clf_res_df['ΔROC-AUC'] = clf_res_df['ROC-AUC'].diff().fillna(0)
    clf_res_df.to_csv("research/results/feature_ablation_classification.csv", index=False)
    
    plot_ablation(clf_res_df, 'PR-AUC', 'Classification PR-AUC by Feature Configuration (Validation)', 'ablation_pr_auc.png')
    plot_ablation(clf_res_df, 'ROC-AUC', 'Classification ROC-AUC by Feature Configuration (Validation)', 'ablation_roc_auc.png')
    
    # ---------------------------------------------------------
    # REGRESSION ABLATION
    # ---------------------------------------------------------
    print("\n=== REGRESSION ABLATION ===")
    reg_val_results = []
    best_reg_metric = float('inf')
    best_reg_config = None
    best_reg_features = None
    
    y_train_reg = df_reg.loc[train_mask_reg, 'case_duration_days']
    y_val_reg = df_reg.loc[val_mask_reg, 'case_duration_days']
    y_test_reg = df_reg.loc[test_mask_reg, 'case_duration_days']
    
    for config_name, group_list in ablations:
        print(f"Training Config {config_name} ({'+'.join(group_list)})...")
        current_features = []
        for g in group_list:
            current_features.extend(groups[g])
            
        X_train = df_reg.loc[train_mask_reg, current_features].copy()
        X_val = df_reg.loc[val_mask_reg, current_features].copy()
        
        preprocessor, cat_cols = create_pipeline(current_features)
        X_train[cat_cols] = X_train[cat_cols].astype(str)
        X_val[cat_cols] = X_val[cat_cols].astype(str)
        
        model = xgb.XGBRegressor(n_estimators=200, max_depth=6, learning_rate=0.1, n_jobs=-1, random_state=42)
        pipe = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])
        
        start_time = time.time()
        pipe.fit(X_train, y_train_reg)
        runtime = time.time() - start_time
        
        metrics = evaluate_regression(pipe, X_val, y_val_reg, f"abl_{config_name}", config_name)
        reg_val_results.append({
            'Config': config_name, 
            'Groups': '+'.join([g.split('_')[1] for g in group_list]),
            'Feature Count': len(current_features),
            'Runtime (s)': runtime,
            **metrics
        })
        
        # Determine best on Validation (MAE)
        if metrics['MAE'] < best_reg_metric:
            best_reg_metric = metrics['MAE']
            best_reg_config = config_name
            best_reg_features = current_features
            joblib.dump(pipe, "models/best_ablation_reg.joblib")
            
    reg_res_df = pd.DataFrame(reg_val_results)
    reg_res_df['ΔMAE'] = reg_res_df['MAE'].diff().fillna(0)
    reg_res_df['ΔRMSE'] = reg_res_df['RMSE'].diff().fillna(0)
    reg_res_df.to_csv("research/results/feature_ablation_regression.csv", index=False)
    
    plot_ablation(reg_res_df, 'MAE', 'Regression MAE by Feature Configuration (Validation)', 'ablation_mae.png')
    plot_ablation(reg_res_df, 'RMSE', 'Regression RMSE by Feature Configuration (Validation)', 'ablation_rmse.png')
    
    # ---------------------------------------------------------
    # FINAL TEST EVALUATION (ONLY BEST MODEL)
    # ---------------------------------------------------------
    print(f"\n=== FINAL TEST EVALUATION ===")
    print(f"Best Classification Config: {best_clf_config} (Val PR-AUC: {best_clf_metric:.4f})")
    
    X_test_clf = df_clf.loc[test_mask_clf, best_clf_features].copy()
    _, cat_cols_clf = create_pipeline(best_clf_features)
    X_test_clf[cat_cols_clf] = X_test_clf[cat_cols_clf].astype(str)
    
    best_clf_pipe = joblib.load("models/best_ablation_clf.joblib")
    clf_test_metrics = evaluate_classification(best_clf_pipe, X_test_clf, y_test_clf, "test_clf_best", "Best_Ablation")
    print(f"Test PR-AUC: {clf_test_metrics['PR-AUC']:.4f}")
    
    print(f"\nBest Regression Config: {best_reg_config} (Val MAE: {best_reg_metric:.2f})")
    
    X_test_reg = df_reg.loc[test_mask_reg, best_reg_features].copy()
    _, cat_cols_reg = create_pipeline(best_reg_features)
    X_test_reg[cat_cols_reg] = X_test_reg[cat_cols_reg].astype(str)
    
    best_reg_pipe = joblib.load("models/best_ablation_reg.joblib")
    reg_test_metrics = evaluate_regression(best_reg_pipe, X_test_reg, y_test_reg, "test_reg_best", "Best_Ablation")
    print(f"Test MAE: {reg_test_metrics['MAE']:.2f}")

if __name__ == '__main__':
    main()
