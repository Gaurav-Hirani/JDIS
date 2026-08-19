import pytest
import os
import pandas as pd
import joblib

def test_advanced_models_leakage_absence():
    # Only test if models have been generated
    if not os.path.exists("models/CLS-ADV-001.joblib"):
        pytest.skip("Advanced models not generated yet.")
        
    clf_pipe = joblib.load("models/CLS-ADV-001.joblib")
    features = clf_pipe.named_steps['preprocessor'].get_feature_names_out()
    
    leakage_features = ['case_duration_days', 'delay_24m', 'delay_12m', 'delay_36m', 'date_of_decision']
    
    for f in features:
        for leak in leakage_features:
            assert leak not in f, f"Leakage feature {leak} found in model pipeline features!"

def test_lightgbm_ordinal_usage():
    if not os.path.exists("models/CLS-ADV-003.joblib"):
        pytest.skip("LightGBM not generated yet.")
        
    lgb_pipe = joblib.load("models/CLS-ADV-003.joblib")
    prep = lgb_pipe.named_steps['preprocessor']
    
    # Check that it uses OrdinalEncoder, not OneHotEncoder
    for name, trans, cols in prep.transformers:
        if name == 'cat':
            steps = dict(trans.steps)
            assert 'ordinal' in steps, "LightGBM pipeline must use OrdinalEncoder for categoricals."
            assert 'onehot' not in steps, "LightGBM pipeline must NOT use OneHotEncoder."
