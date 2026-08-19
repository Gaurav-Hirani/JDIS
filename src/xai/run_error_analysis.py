import os
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, mean_absolute_error, mean_squared_error

def duration_bucket(days):
    if days <= 365:
        return 'Short (<1 yr)'
    elif days <= 1095:
        return 'Medium (1-3 yrs)'
    else:
        return 'Long (>3 yrs)'

def main():
    os.makedirs("research/results", exist_ok=True)
    os.makedirs("research/figures/error_analysis", exist_ok=True)

    print("Loading models and 2016 Test data...")
    clf_pipe = joblib.load("models/final_calibrated_clf.joblib")
    reg_pipe = joblib.load("models/best_ablation_reg.joblib")
    
    # Read Classification Data
    df_clf = pd.read_parquet("data/features/filing_classification_24m_final.parquet")
    test_mask_clf = df_clf['filing_year'] == 2016
    df_test_clf = df_clf[test_mask_clf].copy()
    
    # Preprocessing info
    # The calibrator pipeline wraps the original pipeline (or FrozenEstimator).
    # Since we used FrozenEstimator, clf_pipe is a CalibratedClassifierCV.
    # To get features, we must look at the original pipeline.
    orig_clf = joblib.load("models/best_ablation_clf.joblib")
    preprocessor_clf = orig_clf.named_steps['preprocessor']
    num_cols_clf = preprocessor_clf.transformers_[0][2]
    cat_cols_clf = preprocessor_clf.transformers_[1][2]
    features_clf = num_cols_clf + cat_cols_clf
    
    X_test_clf = df_test_clf[features_clf].copy()
    X_test_clf[cat_cols_clf] = X_test_clf[cat_cols_clf].astype(str)
    y_test_clf = df_test_clf['delay_24m'].values
    
    # Predict Classification
    y_prob_clf = clf_pipe.predict_proba(X_test_clf)[:, 1]
    y_pred_clf = (y_prob_clf > 0.5).astype(int)
    
    df_test_clf['pred_prob'] = y_prob_clf
    df_test_clf['pred_class'] = y_pred_clf
    df_test_clf['risk_score'] = np.floor(np.clip(y_prob_clf, 0.0, 1.0) * 100).astype(int)
    
    # Define Error Types
    df_test_clf['Error_Type'] = 'Correct'
    df_test_clf.loc[(df_test_clf['delay_24m'] == 1) & (df_test_clf['pred_class'] == 1), 'Error_Type'] = 'TP'
    df_test_clf.loc[(df_test_clf['delay_24m'] == 0) & (df_test_clf['pred_class'] == 0), 'Error_Type'] = 'TN'
    df_test_clf.loc[(df_test_clf['delay_24m'] == 0) & (df_test_clf['pred_class'] == 1), 'Error_Type'] = 'FP'
    df_test_clf.loc[(df_test_clf['delay_24m'] == 1) & (df_test_clf['pred_class'] == 0), 'Error_Type'] = 'FN'
    
    # Subgroup Analysis - Classification
    subgroups = ['is_criminal_code', 'state_str']
    clf_errors = []
    
    for grp in subgroups:
        for val in df_test_clf[grp].dropna().unique()[:5]: # Top 5 to avoid explosion
            subset = df_test_clf[df_test_clf[grp] == val]
            if len(subset) > 100:
                tn, fp, fn, tp = confusion_matrix(subset['delay_24m'], subset['pred_class'], labels=[0,1]).ravel()
                clf_errors.append({
                    'Subgroup_Variable': grp,
                    'Subgroup_Value': val,
                    'Sample_Size': len(subset),
                    'TP': tp,
                    'TN': tn,
                    'FP': fp,
                    'FN': fn,
                    'FDR (FP / (FP+TP))': fp / (fp+tp) if (fp+tp)>0 else 0,
                    'FNR (FN / (FN+TP))': fn / (fn+tp) if (fn+tp)>0 else 0
                })
                
    pd.DataFrame(clf_errors).to_csv("research/results/error_analysis_classification.csv", index=False)
    
    # Plot FP/FN by Risk Score
    plt.figure(figsize=(10,6))
    df_test_clf[df_test_clf['Error_Type'] == 'FP']['risk_score'].hist(alpha=0.5, label='False Positives', bins=20)
    df_test_clf[df_test_clf['Error_Type'] == 'FN']['risk_score'].hist(alpha=0.5, label='False Negatives', bins=20)
    plt.title("Error Distribution by Risk Score")
    plt.xlabel("Risk Score")
    plt.legend()
    plt.savefig("research/figures/error_analysis/clf_errors_by_risk.png", bbox_inches='tight')
    plt.close()
    
    # Read Regression Data
    df_reg = pd.read_parquet("data/features/filing_regression_final.parquet")
    test_mask_reg = df_reg['filing_year'] == 2016
    df_test_reg = df_reg[test_mask_reg].copy()
    
    preprocessor_reg = reg_pipe.named_steps['preprocessor']
    num_cols_reg = preprocessor_reg.transformers_[0][2]
    cat_cols_reg = preprocessor_reg.transformers_[1][2]
    features_reg = num_cols_reg + cat_cols_reg
    
    X_test_reg = df_test_reg[features_reg].copy()
    X_test_reg[cat_cols_reg] = X_test_reg[cat_cols_reg].astype(str)
    y_test_reg = df_test_reg['case_duration_days'].values
    
    # Predict Regression
    y_pred_reg = reg_pipe.predict(X_test_reg)
    df_test_reg['pred_duration'] = y_pred_reg
    df_test_reg['error'] = y_pred_reg - y_test_reg
    df_test_reg['duration_bucket'] = df_test_reg['case_duration_days'].apply(duration_bucket)
    
    # Error by Bucket
    reg_errors = []
    for b in ['Short (<1 yr)', 'Medium (1-3 yrs)', 'Long (>3 yrs)']:
        subset = df_test_reg[df_test_reg['duration_bucket'] == b]
        if len(subset) > 0:
            mae = mean_absolute_error(subset['case_duration_days'], subset['pred_duration'])
            rmse = np.sqrt(mean_squared_error(subset['case_duration_days'], subset['pred_duration']))
            mean_error = subset['error'].mean() # positive = overprediction, negative = underprediction
            reg_errors.append({
                'Subgroup_Variable': 'Duration Bucket',
                'Subgroup_Value': b,
                'Sample_Size': len(subset),
                'MAE': mae,
                'RMSE': rmse,
                'Mean_Directional_Error': mean_error
            })
            
    for grp in subgroups:
        for val in df_test_reg[grp].dropna().unique()[:5]:
            subset = df_test_reg[df_test_reg[grp] == val]
            if len(subset) > 100:
                mae = mean_absolute_error(subset['case_duration_days'], subset['pred_duration'])
                rmse = np.sqrt(mean_squared_error(subset['case_duration_days'], subset['pred_duration']))
                reg_errors.append({
                    'Subgroup_Variable': grp,
                    'Subgroup_Value': val,
                    'Sample_Size': len(subset),
                    'MAE': mae,
                    'RMSE': rmse,
                    'Mean_Directional_Error': subset['error'].mean()
                })
                
    pd.DataFrame(reg_errors).to_csv("research/results/error_analysis_regression.csv", index=False)
    
    # Plot Regression Errors
    plt.figure(figsize=(10,6))
    plt.scatter(df_test_reg['case_duration_days'], df_test_reg['error'], alpha=0.1, s=2)
    plt.axhline(0, color='r', linestyle='--')
    plt.title("Regression Residuals by Actual Duration (2016 Test)")
    plt.xlabel("Actual Duration (Days)")
    plt.ylabel("Prediction Error (Predicted - Actual)")
    plt.savefig("research/figures/error_analysis/reg_residuals.png", bbox_inches='tight')
    plt.close()

    print("Error Analysis Complete.")

if __name__ == "__main__":
    main()
