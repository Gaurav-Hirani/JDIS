import os
import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error
from train_hearing_baselines import load_and_split_hearing_data

def gap_bucket(days):
    if days == 0:
        return 'Zero Gap (Same Day)'
    elif days <= 14:
        return 'Short (1-14 days)'
    elif days <= 60:
        return 'Medium (15-60 days)'
    else:
        return 'Long (>60 days)'

def main():
    os.makedirs("research/results", exist_ok=True)
    os.makedirs("research/figures/hearing", exist_ok=True)
    
    print("Loading test data and model...")
    train_df, val_df, test_df, features, num_cols, cat_cols = load_and_split_hearing_data()
    
    pipe = joblib.load("models/final_hearing_model.joblib")
    
    X_test = test_df[features].copy()
    X_test[cat_cols] = X_test[cat_cols].astype(str)
    y_test = test_df['next_listing_gap_days'].values
    
    print("Predicting...")
    y_pred = pipe.predict(X_test)
    
    # Floor negative predictions to 0
    y_pred = np.maximum(y_pred, 0)
    
    test_df['predicted_gap'] = y_pred
    test_df['error'] = y_pred - y_test
    test_df['gap_bucket'] = test_df['next_listing_gap_days'].apply(gap_bucket)
    
    results = []
    
    # 1. By Gap Bucket
    for b in test_df['gap_bucket'].unique():
        subset = test_df[test_df['gap_bucket'] == b]
        if len(subset) > 0:
            mae = mean_absolute_error(subset['next_listing_gap_days'], subset['predicted_gap'])
            rmse = np.sqrt(mean_squared_error(subset['next_listing_gap_days'], subset['predicted_gap']))
            results.append({
                'Group_Variable': 'Gap Bucket',
                'Group_Value': b,
                'Sample_Size': len(subset),
                'MAE': mae,
                'RMSE': rmse,
                'Mean_Directional_Error': subset['error'].mean()
            })
            
    # 2. By State (Top 5)
    for state in test_df['state_str'].value_counts().nlargest(5).index:
        subset = test_df[test_df['state_str'] == state]
        if len(subset) > 0:
            mae = mean_absolute_error(subset['next_listing_gap_days'], subset['predicted_gap'])
            rmse = np.sqrt(mean_squared_error(subset['next_listing_gap_days'], subset['predicted_gap']))
            results.append({
                'Group_Variable': 'State',
                'Group_Value': state,
                'Sample_Size': len(subset),
                'MAE': mae,
                'RMSE': rmse,
                'Mean_Directional_Error': subset['error'].mean()
            })

    # 3. By Judge Position (Top 5)
    for jp in test_df['judge_position_clean'].value_counts().nlargest(5).index:
        subset = test_df[test_df['judge_position_clean'] == jp]
        if len(subset) > 0:
            mae = mean_absolute_error(subset['next_listing_gap_days'], subset['predicted_gap'])
            rmse = np.sqrt(mean_squared_error(subset['next_listing_gap_days'], subset['predicted_gap']))
            results.append({
                'Group_Variable': 'Judge Position',
                'Group_Value': jp,
                'Sample_Size': len(subset),
                'MAE': mae,
                'RMSE': rmse,
                'Mean_Directional_Error': subset['error'].mean()
            })

    df_res = pd.DataFrame(results)
    df_res.to_csv("research/results/hearing_error_analysis.csv", index=False)
    print("Error analysis saved to research/results/hearing_error_analysis.csv")
    
if __name__ == '__main__':
    main()
