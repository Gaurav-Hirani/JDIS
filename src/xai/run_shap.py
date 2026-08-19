import os
import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt

def main():
    os.makedirs("research/results", exist_ok=True)
    os.makedirs("research/figures", exist_ok=True)
    os.makedirs("research/figures/shap_local", exist_ok=True)

    print("Loading test data and model...")
    df_clf = pd.read_parquet("data/features/filing_classification_24m_final.parquet")
    test_mask_clf = df_clf['filing_year'] == 2016
    df_test = df_clf[test_mask_clf].copy()
    
    pipe = joblib.load("models/best_ablation_clf.joblib")
    preprocessor = pipe.named_steps['preprocessor']
    model = pipe.named_steps['model']
    
    # Extract features used by Config D
    num_cols = preprocessor.transformers_[0][2]
    cat_cols = preprocessor.transformers_[1][2]
    features = num_cols + cat_cols
    
    # ---------------------------------------------------------
    # PHASE 5A: ARTIFACT VERIFICATION LOGGING
    # ---------------------------------------------------------
    print("=== Phase 5A: Model Artifact Verification ===")
    print(f"Model Path: models/best_ablation_clf.joblib")
    print(f"Algorithm: {type(model).__name__}")
    print(f"Feature Count: {len(features)}")
    print(f"Hyperparameters: n_estimators={model.n_estimators}, max_depth={model.max_depth}, learning_rate={model.learning_rate}")
    
    # Sample 5000 for SHAP explanation
    sample_size = min(5000, len(df_test))
    df_sample = df_test.sample(n=sample_size, random_state=42)
    
    X_sample = df_sample[features].copy()
    X_sample[cat_cols] = X_sample[cat_cols].astype(str)
    y_sample = df_sample['delay_24m'].values
    
    # Transform
    X_sample_trans = preprocessor.transform(X_sample)
    
    # Get feature names after OHE
    feature_names = preprocessor.get_feature_names_out()
    # Clean feature names
    feature_names = [f.replace('num__', '').replace('cat__', '') for f in feature_names]
    
    # Convert sparse to dense if needed for SHAP visualization
    X_sample_dense = X_sample_trans.toarray() if hasattr(X_sample_trans, 'toarray') else X_sample_trans
    
    X_sample_df = pd.DataFrame(X_sample_dense, columns=feature_names)
    
    print("Calculating SHAP values...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sample_df)
    
    # ---------------------------------------------------------
    # PHASE 5B: GLOBAL SHAP
    # ---------------------------------------------------------
    print("Generating Global SHAP Figures...")
    plt.figure()
    shap.summary_plot(shap_values, X_sample_df, show=False)
    plt.savefig("research/figures/shap_classification_beeswarm.png", bbox_inches='tight')
    plt.close()
    
    plt.figure()
    shap.summary_plot(shap_values, X_sample_df, plot_type='bar', show=False)
    plt.savefig("research/figures/shap_classification_bar.png", bbox_inches='tight')
    plt.close()
    
    # Global CSV
    mean_abs_shap = np.abs(shap_values).mean(axis=0)
    shap_global_df = pd.DataFrame({
        'Feature': feature_names,
        'Mean_Absolute_SHAP': mean_abs_shap
    }).sort_values('Mean_Absolute_SHAP', ascending=False)
    shap_global_df.to_csv("research/results/shap_classification_global.csv", index=False)
    
    with open("research/results/shap_classification_global.md", "w") as f:
        f.write("# Global SHAP Importance\n")
        f.write(shap_global_df.head(20).to_markdown(index=False))
        
    # ---------------------------------------------------------
    # PHASE 5C: LOCAL SHAP EXPLANATIONS
    # ---------------------------------------------------------
    print("Generating Local SHAP Explanations...")
    # Predict probabilities to identify cases
    preds_proba = pipe.predict_proba(X_sample)[:, 1]
    preds = (preds_proba > 0.5).astype(int)
    
    df_sample['pred_prob'] = preds_proba
    df_sample['pred'] = preds
    df_sample['risk_score'] = (preds_proba * 100).astype(int)
    
    cases = {}
    
    # 1. High risk (e.g. > 90%)
    high_risk = df_sample[df_sample['pred_prob'] > 0.9]
    if len(high_risk) > 0: cases['High Risk'] = high_risk.index[0]
    
    # 2. Medium risk (~50%)
    med_risk = df_sample[(df_sample['pred_prob'] > 0.45) & (df_sample['pred_prob'] < 0.55)]
    if len(med_risk) > 0: cases['Medium Risk'] = med_risk.index[0]
    
    # 3. Low risk (< 10%)
    low_risk = df_sample[df_sample['pred_prob'] < 0.1]
    if len(low_risk) > 0: cases['Low Risk'] = low_risk.index[0]
    
    # 4. True Positive
    tp = df_sample[(df_sample['delay_24m'] == 1) & (df_sample['pred'] == 1)]
    if len(tp) > 0: cases['True Positive'] = tp.index[0]
    
    # 5. False Positive
    fp = df_sample[(df_sample['delay_24m'] == 0) & (df_sample['pred'] == 1)]
    if len(fp) > 0: cases['False Positive'] = fp.index[0]
    
    # 6. False Negative
    fn = df_sample[(df_sample['delay_24m'] == 1) & (df_sample['pred'] == 0)]
    if len(fn) > 0: cases['False Negative'] = fn.index[0]
    
    local_results = []
    
    # To avoid duplicate indices if the same case satisfied multiple rules
    seen_idx = set()
    
    for case_type, idx in cases.items():
        if idx in seen_idx: continue
        seen_idx.add(idx)
        
        pos = df_sample.index.get_loc(idx)
        case_shap = shap_values[pos]
        case_feat = X_sample_df.iloc[pos]
        
        # Top positive contributors
        top_pos_idx = np.argsort(case_shap)[-3:][::-1]
        top_pos = [(feature_names[i], float(case_shap[i]), float(case_feat.iloc[i])) for i in top_pos_idx if case_shap[i] > 0]
        
        # Top negative contributors
        top_neg_idx = np.argsort(case_shap)[:3]
        top_neg = [(feature_names[i], float(case_shap[i]), float(case_feat.iloc[i])) for i in top_neg_idx if case_shap[i] < 0]
        
        local_results.append({
            'Case_ID': str(idx),
            'Category': case_type,
            'Actual_Label': int(df_sample.loc[idx, 'delay_24m']),
            'Predicted_Probability': df_sample.loc[idx, 'pred_prob'],
            'Risk_Score': df_sample.loc[idx, 'risk_score'],
            'Top_Pos_Contributors': str(top_pos),
            'Top_Neg_Contributors': str(top_neg)
        })
        
        # Local Plot
        plt.figure()
        shap.waterfall_plot(shap.Explanation(values=case_shap, 
                                             base_values=explainer.expected_value, 
                                             data=case_feat, 
                                             feature_names=feature_names), 
                            show=False)
        plt.savefig(f"research/figures/shap_local/waterfall_{case_type.replace(' ', '_')}.png", bbox_inches='tight')
        plt.close()
        
    pd.DataFrame(local_results).to_csv("research/results/shap_local_cases.csv", index=False)
    print("SHAP analysis complete.")

if __name__ == "__main__":
    main()
