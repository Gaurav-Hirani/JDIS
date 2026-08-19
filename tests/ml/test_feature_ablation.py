import pytest
import os
import pandas as pd
import joblib

def test_ablation_features_no_leakage():
    if not os.path.exists("models/best_ablation_clf.joblib"):
        pytest.skip("Ablation models not generated yet.")
        
    clf_pipe = joblib.load("models/best_ablation_clf.joblib")
    features = clf_pipe.named_steps['preprocessor'].get_feature_names_out()
    
    leakage_features = ['case_duration_days', 'delay_24m', 'delay_12m', 'delay_36m', 'date_of_decision']
    
    for f in features:
        for leak in leakage_features:
            assert leak not in f, f"Leakage feature {leak} found in ablation model pipeline features!"

def test_ablation_results_exist():
    assert os.path.exists("research/results/feature_ablation_classification.csv"), "Classification ablation results missing."
    assert os.path.exists("research/results/feature_ablation_regression.csv"), "Regression ablation results missing."
    
def test_ablation_model_params():
    if not os.path.exists("models/best_ablation_clf.joblib"):
        pytest.skip("Ablation models not generated yet.")
        
    clf_pipe = joblib.load("models/best_ablation_clf.joblib")
    model = clf_pipe.named_steps['model']
    
    # Must use the exact Phase 3 XGBoost Config
    assert getattr(model, 'n_estimators') == 200
    assert getattr(model, 'max_depth') == 6
    assert getattr(model, 'learning_rate') == 0.1
