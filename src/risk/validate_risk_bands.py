import os
import pandas as pd
import numpy as np
import joblib

def calculate_band_metrics(df, pipe, features, cat_cols, dataset_name):
    X = df[features].copy()
    X[cat_cols] = X[cat_cols].astype(str)
    
    probs = pipe.predict_proba(X)[:, 1]
    scores = np.floor(np.clip(probs, 0.0, 1.0) * 100).astype(int)
    
    bins = [-1, 20, 50, 80, 100]
    labels = ['Low', 'Moderate', 'High', 'Very High']
    bands = pd.cut(scores, bins=bins, labels=labels)
    
    df_metrics = pd.DataFrame({
        'delay_24m': df['delay_24m'].values,
        'pred_prob': probs,
        'band': bands
    })
    
    results = []
    total_cases = len(df)
    
    for label in labels:
        subset = df_metrics[df_metrics['band'] == label]
        n_cases = len(subset)
        if n_cases == 0:
            continue
        
        n_delayed = subset['delay_24m'].sum()
        results.append({
            'Risk_Band': label,
            'Total_Cases': n_cases,
            'Percentage': (n_cases / total_cases) * 100,
            'Number_Delayed': n_delayed,
            'Observed_Delay_Rate': n_delayed / n_cases,
            'Mean_Predicted_Prob': subset['pred_prob'].mean(),
            'Median_Predicted_Prob': subset['pred_prob'].median()
        })
        
    res_df = pd.DataFrame(results)
    res_df.to_csv(f"research/results/risk_band_{dataset_name}.csv", index=False)
    return res_df

def main():
    os.makedirs("research/results", exist_ok=True)
    
    df_clf = pd.read_parquet("data/features/filing_classification_24m_final.parquet")
    
    pipe = joblib.load("models/final_calibrated_clf.joblib")
    orig_clf = joblib.load("models/best_ablation_clf.joblib")
    preprocessor = orig_clf.named_steps['preprocessor']
    num_cols = preprocessor.transformers_[0][2]
    cat_cols = preprocessor.transformers_[1][2]
    features = num_cols + cat_cols
    
    df_val = df_clf[df_clf['filing_year'] == 2015].copy()
    print("Validating 2015...")
    calculate_band_metrics(df_val, pipe, features, cat_cols, "validation")
    
    df_test = df_clf[df_clf['filing_year'] == 2016].copy()
    print("Validating 2016...")
    test_res = calculate_band_metrics(df_test, pipe, features, cat_cols, "test")
    # For test, user requested number of cases, percentage, observed delay rate (which are in the CSV).
    
    print("Risk band validation complete.")

if __name__ == "__main__":
    main()
