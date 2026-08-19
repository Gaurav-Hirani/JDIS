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
    print("--- 1. BUILDING REGRESSION BASELINES ---")
    df_reg = pd.read_parquet("data/features/filing_regression_final.parquet")
    
    # Final Primary Split
    train_mask_reg = (df_reg['filing_year'] >= 2010) & (df_reg['filing_year'] <= 2014)
    val_mask_reg = df_reg['filing_year'] == 2015
    test_mask_reg = df_reg['filing_year'] == 2016
    
    # Features and Targets
    target_cols = ['case_duration_days', 'delay_24m', 'delay_12m', 'delay_36m']
    id_cols = ['ddl_case_id', 'filing_year']
    feature_cols = [c for c in df_reg.columns if c not in target_cols + id_cols]
    
    numerical_cols = [c for c in feature_cols if c.startswith('tfidf_') or 
                      'count' in c or 'rate' in c or 'duration' in c or 
                      'backlog' in c or 'days' in c or 'degree' in c or 
                      'month' in c or 'quarter' in c or 'day_of_week' in c]
    categorical_cols = [c for c in feature_cols if c not in numerical_cols]
    
    df_reg[categorical_cols] = df_reg[categorical_cols].astype(str)
    
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=True))
    ])
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ])

    X_train_reg = df_reg.loc[train_mask_reg, feature_cols]
    y_train_reg = df_reg.loc[train_mask_reg, 'case_duration_days']
    X_val_reg = df_reg.loc[val_mask_reg, feature_cols]
    y_val_reg = df_reg.loc[val_mask_reg, 'case_duration_days']
    X_test_reg = df_reg.loc[test_mask_reg, feature_cols]
    y_test_reg = df_reg.loc[test_mask_reg, 'case_duration_days']
    
    regression_models = {
        'REG-FIN-001': ('Mean Predictor', DummyRegressor(strategy='mean')),
        'REG-FIN-002': ('Median Predictor', DummyRegressor(strategy='median')),
        'REG-FIN-003': ('Linear Regression', LinearRegression()),
        'REG-FIN-004': ('Decision Tree Regressor', DecisionTreeRegressor(max_depth=5, random_state=42))
    }
    
    reg_val_results = []
    reg_test_results = []
    
    for exp_id, (name, model) in regression_models.items():
        print(f"Training {name} ({exp_id})...")
        pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])
        
        # Train
        pipeline.fit(X_train_reg, y_train_reg)
        
        # Validation
        val_metrics = evaluate_regression(pipeline, X_val_reg, y_val_reg, f"{exp_id}_val", name)
        reg_val_results.append({'Model': name, **val_metrics})
        register_experiment(exp_id, "Final Baseline Regression", "Filing Regression Dataset", "case_duration_days", 
                            name, "Train: 2010-2014, Val: 2015", f"Val MAE: {val_metrics['MAE']:.2f}")
        
        # Final Test evaluation
        test_metrics = evaluate_regression(pipeline, X_test_reg, y_test_reg, f"{exp_id}_test", name)
        reg_test_results.append({'Model': name, **test_metrics})
        
        joblib.dump(pipeline, f"models/{exp_id}.joblib")
        
    pd.DataFrame(reg_val_results).to_csv("research/results/final_regression_baselines_val.csv", index=False)
    pd.DataFrame(reg_val_results).to_markdown("research/results/final_regression_baselines_val.md", index=False)
    pd.DataFrame(reg_test_results).to_csv("research/results/final_regression_baselines_test.csv", index=False)
    pd.DataFrame(reg_test_results).to_markdown("research/results/final_regression_baselines_test.md", index=False)


    print("\n--- 2. BUILDING 24M CLASSIFICATION BASELINES ---")
    df_clf = pd.read_parquet("data/features/filing_classification_24m_final.parquet")
    
    train_mask_clf = (df_clf['filing_year'] >= 2010) & (df_clf['filing_year'] <= 2014)
    val_mask_clf = df_clf['filing_year'] == 2015
    test_mask_clf = df_clf['filing_year'] == 2016
    
    df_clf[categorical_cols] = df_clf[categorical_cols].astype(str)
    
    X_train_clf = df_clf.loc[train_mask_clf, feature_cols]
    y_train_clf = df_clf.loc[train_mask_clf, 'delay_24m']
    X_val_clf = df_clf.loc[val_mask_clf, feature_cols]
    y_val_clf = df_clf.loc[val_mask_clf, 'delay_24m']
    X_test_clf = df_clf.loc[test_mask_clf, feature_cols]
    y_test_clf = df_clf.loc[test_mask_clf, 'delay_24m']
    
    # Generate Class Distribution Report
    dist_results = []
    for split_name, X_split, y_split in [("Train (2010-2014)", X_train_clf, y_train_clf),
                                         ("Validation (2015)", X_val_clf, y_val_clf),
                                         ("Test (2016)", X_test_clf, y_test_clf)]:
        tot = len(y_split)
        pos = y_split.sum()
        neg = tot - pos
        pct = (pos / tot * 100) if tot > 0 else 0
        dist_results.append({
            'Split': split_name,
            'Total Eligible': tot,
            'Negative Count': neg,
            'Positive Count': pos,
            'Positive %': pct
        })
    pd.DataFrame(dist_results).to_csv("research/results/final_24m_class_distribution.csv", index=False)
    print("\nClass Distribution Saved:")
    print(pd.DataFrame(dist_results).to_string())
    
    classification_models = {
        'CLS-FIN-001': ('Majority-class Predictor', DummyClassifier(strategy='prior')),
        'CLS-FIN-002': ('Logistic Regression', LogisticRegression(solver='saga', max_iter=1000, random_state=42)),
        'CLS-FIN-003': ('Decision Tree Classifier', DecisionTreeClassifier(max_depth=5, random_state=42))
    }
    
    clf_val_results = []
    clf_test_results = []
    
    for exp_id, (name, model) in classification_models.items():
        print(f"Training {name} ({exp_id})...")
        pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])
        
        # Train
        pipeline.fit(X_train_clf, y_train_clf)
        
        # Validation
        val_metrics = evaluate_classification(pipeline, X_val_clf, y_val_clf, f"{exp_id}_val", name)
        clf_val_results.append({'Model': name, **val_metrics})
        register_experiment(exp_id, "Final Baseline Classification", "Filing 24m Dataset", "delay_24m", 
                            name, "Train: 2010-2014, Val: 2015", f"Val F1: {val_metrics['F1']:.4f}")
                            
        # Final Test evaluation
        test_metrics = evaluate_classification(pipeline, X_test_clf, y_test_clf, f"{exp_id}_test", name)
        clf_test_results.append({'Model': name, **test_metrics})
        
        joblib.dump(pipeline, f"models/{exp_id}.joblib")
        
    pd.DataFrame(clf_val_results).to_csv("research/results/final_classification_baselines_val.csv", index=False)
    pd.DataFrame(clf_val_results).to_markdown("research/results/final_classification_baselines_val.md", index=False)
    pd.DataFrame(clf_test_results).to_csv("research/results/final_classification_baselines_test.csv", index=False)
    pd.DataFrame(clf_test_results).to_markdown("research/results/final_classification_baselines_test.md", index=False)

    print("\nAll final baseline models trained and evaluated on Val and Test cohorts. Artifacts saved.")

if __name__ == '__main__':
    main()
