import os
import pandas as pd
import numpy as np
import joblib

from experiment_utils import evaluate_classification, evaluate_regression

def main():
    os.makedirs("research/results", exist_ok=True)
    os.makedirs("research/figures", exist_ok=True)
    
    # ---------------------------------------------------------
    # 1. LOAD VALIDATION RESULTS & SELECT MODELS
    # ---------------------------------------------------------
    clf_val = pd.read_csv("research/results/advanced_model_comparison_classification_val.csv")
    reg_val = pd.read_csv("research/results/advanced_model_comparison_regression_val.csv")
    
    # Identify advanced models
    adv_clf_names = ['Random Forest Classifier', 'XGBoost Classifier', 'LightGBM Classifier']
    adv_reg_names = ['Random Forest Regressor', 'XGBoost Regressor', 'LightGBM Regressor']
    
    base_clf_names = [m for m in clf_val['Model'].unique() if m not in adv_clf_names]
    base_reg_names = [m for m in reg_val['Model'].unique() if m not in adv_reg_names]
    
    # Selection rule for Classification: PR-AUC
    best_adv_clf_row = clf_val[clf_val['Model'].isin(adv_clf_names)].sort_values(by='PR-AUC', ascending=False).iloc[0]
    best_base_clf_row = clf_val[clf_val['Model'].isin(base_clf_names)].sort_values(by='PR-AUC', ascending=False).iloc[0]
    
    # Selection rule for Regression: MAE (lowest is best)
    best_adv_reg_row = reg_val[reg_val['Model'].isin(adv_reg_names)].sort_values(by='MAE', ascending=True).iloc[0]
    best_base_reg_row = reg_val[reg_val['Model'].isin(base_reg_names)].sort_values(by='MAE', ascending=True).iloc[0]
    
    print("=== MODEL SELECTION (Based purely on 2015 Validation) ===")
    print(f"Selected Advanced Classifier: {best_adv_clf_row['Model']} (PR-AUC: {best_adv_clf_row['PR-AUC']:.4f})")
    print(f"Selected Baseline Classifier: {best_base_clf_row['Model']} (PR-AUC: {best_base_clf_row['PR-AUC']:.4f})")
    print(f"Selected Advanced Regressor: {best_adv_reg_row['Model']} (MAE: {best_adv_reg_row['MAE']:.2f})")
    print(f"Selected Baseline Regressor: {best_base_reg_row['Model']} (MAE: {best_base_reg_row['MAE']:.2f})")
    
    # Mapping Model names to IDs manually for loading
    model_to_id = {
        'Random Forest Classifier': 'CLS-ADV-001',
        'XGBoost Classifier': 'CLS-ADV-002',
        'LightGBM Classifier': 'CLS-ADV-003',
        'Random Forest Regressor': 'REG-ADV-001',
        'XGBoost Regressor': 'REG-ADV-002',
        'LightGBM Regressor': 'REG-ADV-003',
        'Logistic Regression': 'CLS-FIN-002',
        'Linear Regression': 'REG-FIN-003'
    }
    
    # Fallback to defaults if mapping is incomplete for baselines
    best_adv_clf_id = model_to_id.get(best_adv_clf_row['Model'], 'CLS-ADV-003')
    best_base_clf_id = model_to_id.get(best_base_clf_row['Model'], 'CLS-FIN-002')
    best_adv_reg_id = model_to_id.get(best_adv_reg_row['Model'], 'REG-ADV-003')
    best_base_reg_id = model_to_id.get(best_base_reg_row['Model'], 'REG-FIN-003')
    
    # ---------------------------------------------------------
    # 2. LOAD 2016 TEST DATA
    # ---------------------------------------------------------
    print("\nLoading 2016 Test cohorts...")
    df_clf = pd.read_parquet("data/features/filing_classification_24m_final.parquet")
    df_reg = pd.read_parquet("data/features/filing_regression_final.parquet")
    
    test_mask_clf = df_clf['filing_year'] == 2016
    test_mask_reg = df_reg['filing_year'] == 2016
    
    target_cols = ['case_duration_days', 'delay_24m', 'delay_12m', 'delay_36m']
    id_cols = ['ddl_case_id', 'filing_year']
    
    feature_cols_clf = [c for c in df_clf.columns if c not in target_cols + id_cols]
    feature_cols_reg = [c for c in df_reg.columns if c not in target_cols + id_cols]
    
    X_test_clf = df_clf.loc[test_mask_clf, feature_cols_clf].copy()
    y_test_clf = df_clf.loc[test_mask_clf, 'delay_24m']
    
    X_test_reg = df_reg.loc[test_mask_reg, feature_cols_reg].copy()
    y_test_reg = df_reg.loc[test_mask_reg, 'case_duration_days']
    
    # Ensure categorical columns are strings
    numerical_cols = [c for c in feature_cols_clf if c.startswith('tfidf_') or 
                      'count' in c or 'rate' in c or 'duration' in c or 
                      'backlog' in c or 'days' in c or 'degree' in c or 
                      'month' in c or 'quarter' in c or 'day_of_week' in c]
    categorical_cols = [c for c in feature_cols_clf if c not in numerical_cols]

    for df_split in [X_test_clf, X_test_reg]:
        df_split[categorical_cols] = df_split[categorical_cols].astype(str)
        
    # ---------------------------------------------------------
    # 3. EVALUATE ON TEST SET
    # ---------------------------------------------------------
    results_test = []
    
    print("\nEvaluating Classification on Test 2016...")
    # Base CLF
    base_clf_pipe = joblib.load(f"models/{best_base_clf_id}.joblib")
    metrics_base_clf = evaluate_classification(base_clf_pipe, X_test_clf, y_test_clf, 
                                              f"{best_base_clf_id}_test_final", 
                                              f"Baseline: {best_base_clf_row['Model']}")
    results_test.append({'Task': 'Classification', 'Type': 'Baseline', 'Model': best_base_clf_row['Model'], **metrics_base_clf})
    
    # Adv CLF
    adv_clf_pipe = joblib.load(f"models/{best_adv_clf_id}.joblib")
    metrics_adv_clf = evaluate_classification(adv_clf_pipe, X_test_clf, y_test_clf, 
                                             f"{best_adv_clf_id}_test_final", 
                                             f"Advanced: {best_adv_clf_row['Model']}")
    results_test.append({'Task': 'Classification', 'Type': 'Advanced', 'Model': best_adv_clf_row['Model'], **metrics_adv_clf})
    
    print("Evaluating Regression on Test 2016...")
    # Base REG
    base_reg_pipe = joblib.load(f"models/{best_base_reg_id}.joblib")
    metrics_base_reg = evaluate_regression(base_reg_pipe, X_test_reg, y_test_reg, 
                                          f"{best_base_reg_id}_test_final", 
                                          f"Baseline: {best_base_reg_row['Model']}")
    results_test.append({'Task': 'Regression', 'Type': 'Baseline', 'Model': best_base_reg_row['Model'], **metrics_base_reg})
    
    # Adv REG
    adv_reg_pipe = joblib.load(f"models/{best_adv_reg_id}.joblib")
    metrics_adv_reg = evaluate_regression(adv_reg_pipe, X_test_reg, y_test_reg, 
                                         f"{best_adv_reg_id}_test_final", 
                                         f"Advanced: {best_adv_reg_row['Model']}")
    results_test.append({'Task': 'Regression', 'Type': 'Advanced', 'Model': best_adv_reg_row['Model'], **metrics_adv_reg})
    
    # ---------------------------------------------------------
    # 4. SAVE FINAL TEST RESULTS
    # ---------------------------------------------------------
    final_test_df = pd.DataFrame(results_test)
    final_test_df.to_csv("research/results/final_model_test_results.csv", index=False)
    final_test_df.to_markdown("research/results/final_model_test_results.md", index=False)
    
    print("\n=== FINAL 2016 TEST EVALUATION COMPLETE ===")
    print("Results saved to research/results/final_model_test_results.csv")

if __name__ == '__main__':
    main()
