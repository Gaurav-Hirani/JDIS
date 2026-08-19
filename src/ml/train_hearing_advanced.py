import os
import pandas as pd
import numpy as np
import joblib
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from train_hearing_baselines import load_and_split_hearing_data, build_preprocessor, evaluate_model

def main():
    os.makedirs("research/results", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    
    print("Loading data...")
    train_df, val_df, test_df, features, num_cols, cat_cols = load_and_split_hearing_data()
    
    X_train = train_df[features].copy()
    X_train[cat_cols] = X_train[cat_cols].astype(str)
    y_train = train_df['next_listing_gap_days'].values
    
    X_val = val_df[features].copy()
    X_val[cat_cols] = X_val[cat_cols].astype(str)
    y_val = val_df['next_listing_gap_days'].values
    
    X_test = test_df[features].copy()
    X_test[cat_cols] = X_test[cat_cols].astype(str)
    y_test = test_df['next_listing_gap_days'].values
    
    preprocessor = build_preprocessor(num_cols, cat_cols)
    
    advanced_models = {
        'Random Forest': RandomForestRegressor(n_estimators=50, max_depth=15, n_jobs=-1, random_state=42),
        'XGBoost': XGBRegressor(n_estimators=200, max_depth=8, learning_rate=0.1, n_jobs=-1, random_state=42)
    }
    
    results_val = []
    
    best_r2 = -float('inf')
    best_name = None
    best_pipe = None
    
    for name, reg in advanced_models.items():
        print(f"Training {name}...")
        pipe = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', reg)])
        pipe.fit(X_train, y_train)
        
        metrics = evaluate_model(name, pipe, X_val, y_val)
        results_val.append(metrics)
        print(f"Validation [{name}] -> MAE: {metrics['MAE']:.2f}, RMSE: {metrics['RMSE']:.2f}, R2: {metrics['R2']:.4f}")
        
        if metrics['R2'] > best_r2:
            best_r2 = metrics['R2']
            best_name = name
            best_pipe = pipe
            
    df_val = pd.DataFrame(results_val)
    df_val.to_csv("research/results/hearing_model_comparison_validation.csv", index=False)
    
    print(f"\nBest model selected on Validation: {best_name}")
    print("Evaluating on held-out 2019 Test Set...")
    
    test_metrics = evaluate_model(best_name, best_pipe, X_test, y_test)
    df_test = pd.DataFrame([test_metrics])
    df_test.to_csv("research/results/hearing_model_comparison_test.csv", index=False)
    
    print(f"Test [{best_name}] -> MAE: {test_metrics['MAE']:.2f}, RMSE: {test_metrics['RMSE']:.2f}, R2: {test_metrics['R2']:.4f}")
    
    # Save the final model
    joblib.dump(best_pipe, "models/final_hearing_model.joblib")
    print("Model saved to models/final_hearing_model.joblib")

if __name__ == "__main__":
    main()
