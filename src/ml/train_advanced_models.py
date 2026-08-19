import os
import pandas as pd
import numpy as np
import joblib
import time

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

import xgboost as xgb
import lightgbm as lgb

from experiment_utils import (register_experiment, evaluate_regression, 
                              evaluate_classification)

def main():
    os.makedirs("research/results", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    
    # ---------------------------------------------------------
    # 1. LOAD DATA & SPLITS
    # ---------------------------------------------------------
    print("Loading datasets...")
    df_reg = pd.read_parquet("data/features/filing_regression_final.parquet")
    df_clf = pd.read_parquet("data/features/filing_classification_24m_final.parquet")
    
    # Train: 2010-2014, Val: 2015. (2016 is STRICTLY held out)
    train_mask_reg = (df_reg['filing_year'] >= 2010) & (df_reg['filing_year'] <= 2014)
    val_mask_reg = df_reg['filing_year'] == 2015
    
    train_mask_clf = (df_clf['filing_year'] >= 2010) & (df_clf['filing_year'] <= 2014)
    val_mask_clf = df_clf['filing_year'] == 2015

    target_cols = ['case_duration_days', 'delay_24m', 'delay_12m', 'delay_36m']
    id_cols = ['ddl_case_id', 'filing_year']
    
    # Regression
    feature_cols = [c for c in df_reg.columns if c not in target_cols + id_cols]
    X_train_reg = df_reg.loc[train_mask_reg, feature_cols]
    y_train_reg = df_reg.loc[train_mask_reg, 'case_duration_days']
    X_val_reg = df_reg.loc[val_mask_reg, feature_cols]
    y_val_reg = df_reg.loc[val_mask_reg, 'case_duration_days']
    
    # Classification
    X_train_clf = df_clf.loc[train_mask_clf, feature_cols]
    y_train_clf = df_clf.loc[train_mask_clf, 'delay_24m']
    X_val_clf = df_clf.loc[val_mask_clf, feature_cols]
    y_val_clf = df_clf.loc[val_mask_clf, 'delay_24m']

    numerical_cols = [c for c in feature_cols if c.startswith('tfidf_') or 
                      'count' in c or 'rate' in c or 'duration' in c or 
                      'backlog' in c or 'days' in c or 'degree' in c or 
                      'month' in c or 'quarter' in c or 'day_of_week' in c]
    categorical_cols = [c for c in feature_cols if c not in numerical_cols]

    # Convert to string for consistent encoding
    for df_split in [X_train_reg, X_val_reg, X_train_clf, X_val_clf]:
        df_split[categorical_cols] = df_split[categorical_cols].astype(str)

    # ---------------------------------------------------------
    # 2. PREPROCESSING PIPELINES
    # ---------------------------------------------------------
    # A. Sparse One-Hot (For RF, XGBoost)
    num_trans = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    cat_trans_ohe = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=True))
    ])
    preprocessor_ohe = ColumnTransformer(
        transformers=[
            ('num', num_trans, numerical_cols),
            ('cat', cat_trans_ohe, categorical_cols)
        ])
        
    # B. Ordinal (For LightGBM)
    cat_trans_ord = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('ordinal', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))
    ])
    preprocessor_ord = ColumnTransformer(
        transformers=[
            ('num', num_trans, numerical_cols),
            ('cat', cat_trans_ord, categorical_cols)
        ])

    # ---------------------------------------------------------
    # 3. DEFINE MODELS
    # ---------------------------------------------------------
    clf_models = [
        ('CLS-ADV-001', 'Random Forest Classifier', preprocessor_ohe, 
         RandomForestClassifier(n_estimators=100, max_depth=15, min_samples_leaf=5, n_jobs=-1, random_state=42)),
        ('CLS-ADV-002', 'XGBoost Classifier', preprocessor_ohe, 
         xgb.XGBClassifier(n_estimators=200, max_depth=6, learning_rate=0.1, n_jobs=-1, random_state=42)),
        ('CLS-ADV-003', 'LightGBM Classifier', preprocessor_ord, 
         lgb.LGBMClassifier(n_estimators=200, max_depth=6, learning_rate=0.1, n_jobs=-1, random_state=42, verbose=-1))
    ]
    
    reg_models = [
        ('REG-ADV-001', 'Random Forest Regressor', preprocessor_ohe, 
         RandomForestRegressor(n_estimators=100, max_depth=15, min_samples_leaf=5, n_jobs=-1, random_state=42)),
        ('REG-ADV-002', 'XGBoost Regressor', preprocessor_ohe, 
         xgb.XGBRegressor(n_estimators=200, max_depth=6, learning_rate=0.1, n_jobs=-1, random_state=42)),
        ('REG-ADV-003', 'LightGBM Regressor', preprocessor_ord, 
         lgb.LGBMRegressor(n_estimators=200, max_depth=6, learning_rate=0.1, n_jobs=-1, random_state=42, verbose=-1))
    ]

    clf_val_results = []
    reg_val_results = []

    # ---------------------------------------------------------
    # 4. TRAIN & EVALUATE CLASSIFICATION
    # ---------------------------------------------------------
    print("\n=== CLASSIFICATION ===")
    for exp_id, name, prep, model in clf_models:
        print(f"Training {name} ({exp_id})...")
        pipeline = Pipeline(steps=[('preprocessor', prep), ('model', model)])
        
        # Determine early stopping / fit params
        fit_params = {}
        if 'LightGBM' in name:
            # Need to inform LightGBM which features are categorical AFTER column transformer
            # OrdinalEncoder appends categorical columns at the end
            num_features = len(numerical_cols)
            cat_features = list(range(num_features, num_features + len(categorical_cols)))
            fit_params['model__categorical_feature'] = cat_features
            
        start_time = time.time()
        pipeline.fit(X_train_clf, y_train_clf, **fit_params)
        runtime = time.time() - start_time
        
        print(f"  Training took {runtime:.1f} seconds. Evaluating...")
        val_metrics = evaluate_classification(pipeline, X_val_clf, y_val_clf, f"{exp_id}_val", name)
        
        clf_val_results.append({'Model': name, 'Runtime (s)': runtime, **val_metrics})
        register_experiment(exp_id, "Final Advanced Classification", "Filing 24m Dataset", "delay_24m", 
                            name, "Train: 2010-2014, Val: 2015", f"Val F1: {val_metrics['F1']:.4f}")
        joblib.dump(pipeline, f"models/{exp_id}.joblib")

    # ---------------------------------------------------------
    # 5. TRAIN & EVALUATE REGRESSION
    # ---------------------------------------------------------
    print("\n=== REGRESSION ===")
    for exp_id, name, prep, model in reg_models:
        print(f"Training {name} ({exp_id})...")
        pipeline = Pipeline(steps=[('preprocessor', prep), ('model', model)])
        
        fit_params = {}
        if 'LightGBM' in name:
            num_features = len(numerical_cols)
            cat_features = list(range(num_features, num_features + len(categorical_cols)))
            fit_params['model__categorical_feature'] = cat_features
            
        start_time = time.time()
        pipeline.fit(X_train_reg, y_train_reg, **fit_params)
        runtime = time.time() - start_time
        
        print(f"  Training took {runtime:.1f} seconds. Evaluating...")
        val_metrics = evaluate_regression(pipeline, X_val_reg, y_val_reg, f"{exp_id}_val", name)
        
        reg_val_results.append({'Model': name, 'Runtime (s)': runtime, **val_metrics})
        register_experiment(exp_id, "Final Advanced Regression", "Filing Regression Dataset", "case_duration_days", 
                            name, "Train: 2010-2014, Val: 2015", f"Val MAE: {val_metrics['MAE']:.2f}")
        joblib.dump(pipeline, f"models/{exp_id}.joblib")
        
    # ---------------------------------------------------------
    # 6. COMBINE WITH BASELINES & SAVE
    # ---------------------------------------------------------
    # Load baselines
    try:
        base_clf = pd.read_csv("research/results/final_classification_baselines_val.csv")
        base_reg = pd.read_csv("research/results/final_regression_baselines_val.csv")
        
        full_clf = pd.concat([base_clf, pd.DataFrame(clf_val_results)], ignore_index=True)
        full_reg = pd.concat([base_reg, pd.DataFrame(reg_val_results)], ignore_index=True)
    except FileNotFoundError:
        # Fallback if baselines missing
        full_clf = pd.DataFrame(clf_val_results)
        full_reg = pd.DataFrame(reg_val_results)

    full_clf.to_csv("research/results/advanced_model_comparison_classification_val.csv", index=False)
    full_clf.to_markdown("research/results/advanced_model_comparison_classification_val.md", index=False)
    
    full_reg.to_csv("research/results/advanced_model_comparison_regression_val.csv", index=False)
    full_reg.to_markdown("research/results/advanced_model_comparison_regression_val.md", index=False)

    print("\nAdvanced models successfully trained and evaluated on 2015 Validation.")

if __name__ == '__main__':
    main()
