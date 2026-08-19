import os
import pandas as pd
import numpy as np
import joblib

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.dummy import DummyRegressor, DummyClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier

from experiment_utils import (register_experiment, evaluate_regression, 
                              evaluate_classification, check_data_validity)

def main():
    print("Loading Dataset A...")
    df = pd.read_parquet("data/features/filing_features.parquet")
    
    # 0. Filter resolved cases for supervised training
    df = df[df["case_duration_days"].notna() & (df["case_duration_days"] >= 0)].copy()
    
    # 1. Split logic
    train_mask = df['filing_year'] <= 2016
    val_mask = df['filing_year'] == 2017
    
    # 2. Features and Targets
    target_cols = ['case_duration_days', 'delay_24m', 'delay_12m', 'delay_36m']
    id_cols = ['ddl_case_id', 'filing_year']
    
    feature_cols = [c for c in df.columns if c not in target_cols + id_cols]
    
    # Check data validity
    check_data_validity(df, feature_cols, 'case_duration_days')
    check_data_validity(df, feature_cols, 'delay_24m')
    
    # Determine categorical vs numerical
    # Numericals usually include counts, rates, tfidf
    numerical_cols = [c for c in feature_cols if c.startswith('tfidf_') or 
                      'count' in c or 'rate' in c or 'duration' in c or 
                      'backlog' in c or 'days' in c or 'degree' in c or 
                      'month' in c or 'quarter' in c or 'day_of_week' in c]
    categorical_cols = [c for c in feature_cols if c not in numerical_cols]
    
    print(f"Numerical features: {len(numerical_cols)}")
    print(f"Categorical features: {len(categorical_cols)}")
    
    # Cast categorical columns to string to prevent OneHotEncoder TypeError
    df[categorical_cols] = df[categorical_cols].astype(str)
    
    # Define preprocessing
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ])

    X_train = df.loc[train_mask, feature_cols]
    y_train_reg = df.loc[train_mask, 'case_duration_days']
    y_train_clf = df.loc[train_mask, 'delay_24m']
    
    X_val = df.loc[val_mask, feature_cols]
    y_val_reg = df.loc[val_mask, 'case_duration_days']
    y_val_clf = df.loc[val_mask, 'delay_24m']
    
    # Setup Regression Models
    regression_models = {
        'REG-BASE-001': ('Mean Predictor', DummyRegressor(strategy='mean')),
        'REG-BASE-002': ('Median Predictor', DummyRegressor(strategy='median')),
        'REG-BASE-003': ('Linear Regression', LinearRegression()),
        'REG-BASE-004': ('Decision Tree Regressor', DecisionTreeRegressor(max_depth=5, random_state=42))
    }
    
    reg_results = []
    
    print("--- Running Regression Baselines ---")
    for exp_id, (name, model) in regression_models.items():
        print(f"Training {name} ({exp_id})...")
        pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])
        
        # In sklearn, OneHotEncoder outputting dense array can cause memory issues for large datasets
        # But we only have ~80 features, shouldn't explode too much. If it does, we can use sparse.
        # But Dummy and Trees handle sparse fine, Linear/Logistic handle sparse fine.
        pipeline.fit(X_train, y_train_reg)
        
        metrics = evaluate_regression(pipeline, X_val, y_val_reg, exp_id, name)
        reg_results.append({'Model': name, **metrics})
        
        register_experiment(exp_id, "Baseline Regression", "Dataset A", "case_duration_days", 
                            name, "Train: 2010-2016, Val: 2017", f"MAE: {metrics['MAE']:.2f}")
        
        joblib.dump(pipeline, f"models/{exp_id}.joblib")
        
    reg_df = pd.DataFrame(reg_results)
    reg_df.to_csv("research/results/regression_baselines.csv", index=False)
    reg_df.to_markdown("research/results/regression_baselines.md", index=False)
    
    # Setup Classification Models
    classification_models = {
        'CLS-BASE-001': ('Majority-class Predictor', DummyClassifier(strategy='prior')),
        'CLS-BASE-002': ('Logistic Regression', LogisticRegression(max_iter=1000, random_state=42)),
        'CLS-BASE-003': ('Decision Tree Classifier', DecisionTreeClassifier(max_depth=5, random_state=42))
    }
    
    clf_results = []
    
    print("--- Running Classification Baselines ---")
    for exp_id, (name, model) in classification_models.items():
        print(f"Training {name} ({exp_id})...")
        pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])
        
        pipeline.fit(X_train, y_train_clf)
        
        metrics = evaluate_classification(pipeline, X_val, y_val_clf, exp_id, name)
        clf_results.append({'Model': name, **metrics})
        
        register_experiment(exp_id, "Baseline Classification", "Dataset A", "delay_24m", 
                            name, "Train: 2010-2016, Val: 2017", f"F1: {metrics['F1']:.4f}")
        
        joblib.dump(pipeline, f"models/{exp_id}.joblib")
        
    clf_df = pd.DataFrame(clf_results)
    clf_df.to_csv("research/results/classification_baselines.csv", index=False)
    clf_df.to_markdown("research/results/classification_baselines.md", index=False)
    
    print("All baseline models trained and evaluated. Artifacts saved.")

if __name__ == '__main__':
    main()
