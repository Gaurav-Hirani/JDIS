import os
import pandas as pd
import numpy as np
import joblib

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from experiment_utils import (register_experiment, evaluate_classification, check_data_validity)

def main():
    print("Loading Dataset A...")
    df = pd.read_parquet("data/features/filing_features.parquet")
    
    # 0. Filter resolved cases
    df = df[df["case_duration_days"].notna() & (df["case_duration_days"] >= 0)].copy()
    
    # 1. Split logic
    train_mask = df['filing_year'] <= 2016
    val_mask = df['filing_year'] == 2017
    
    # 2. Features and Targets
    target_cols = ['case_duration_days', 'delay_24m', 'delay_12m', 'delay_36m']
    id_cols = ['ddl_case_id', 'filing_year']
    
    feature_cols = [c for c in df.columns if c not in target_cols + id_cols]
    
    # Check data validity
    check_data_validity(df, feature_cols, 'delay_24m')
    
    numerical_cols = [c for c in feature_cols if c.startswith('tfidf_') or 
                      'count' in c or 'rate' in c or 'duration' in c or 
                      'backlog' in c or 'days' in c or 'degree' in c or 
                      'month' in c or 'quarter' in c or 'day_of_week' in c]
    categorical_cols = [c for c in feature_cols if c not in numerical_cols]
    
    print(f"Raw feature count: {len(feature_cols)}")
    print(f"Numerical features: {len(numerical_cols)}")
    print(f"Categorical features: {len(categorical_cols)}")
    
    # Cast categorical columns to string
    df[categorical_cols] = df[categorical_cols].astype(str)
    
    # Define preprocessing
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    # Using sparse_output=True to handle high cardinality memory efficiently
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=True))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ])

    X_train = df.loc[train_mask, feature_cols]
    y_train_clf = df.loc[train_mask, 'delay_24m']
    
    X_val = df.loc[val_mask, feature_cols]
    y_val_clf = df.loc[val_mask, 'delay_24m']

    print("Fitting preprocessor to calculate transformed dimensionality...")
    X_train_transformed = preprocessor.fit_transform(X_train)
    print(f"Transformed dimensionality after encoding: {X_train_transformed.shape[1]}")

    print(f"Train samples: {len(X_train)}")
    print(f"Train negative: {(y_train_clf == 0).sum()} ({ (y_train_clf == 0).mean():.2%})")
    print(f"Train positive: {(y_train_clf == 1).sum()} ({ (y_train_clf == 1).mean():.2%})")
    
    print(f"Validation samples: {len(X_val)}")
    print(f"Validation negative: {(y_val_clf == 0).sum()} ({ (y_val_clf == 0).mean():.2%})")
    print(f"Validation positive: {(y_val_clf == 1).sum()} ({ (y_val_clf == 1).mean():.2%})")

    classification_models = {
        'CLS-BASE-001': ('Majority-class Predictor', DummyClassifier(strategy='prior')),
        'CLS-BASE-002': ('Logistic Regression', LogisticRegression(solver='saga', max_iter=1000, random_state=42)),
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
