import pandas as pd
import numpy as np
from backend.app.schemas.prediction import CaseFilingFeatures
from backend.app.services.prediction_service import PredictionService
from backend.app.services.risk_service import RiskService
from backend.app.ml.manager import model_manager

def test_ml_pipeline_end_to_end_without_parquet(sample_case_features):
    """
    Verifies that filing-time prediction works end-to-end on raw 29 features
    without requiring raw Parquet datasets.
    """
    features = CaseFilingFeatures(**sample_case_features)
    df = PredictionService.features_to_dataframe(features)

    # 1. Pipeline transform
    assert df.shape == (1, 29)
    
    # 2. Classifier & Calibration
    calibrated_prob = float(model_manager.classifier.predict_proba(df)[:, 1][0])
    assert 0.0 <= calibrated_prob <= 1.0

    # 3. Risk formula check: floor(p * 100)
    expected_score = int(np.floor(calibrated_prob * 100))
    actual_score = RiskService.calculate_risk_score(calibrated_prob)
    assert actual_score == expected_score

    # 4. Risk band check
    actual_band = RiskService.assign_risk_band(actual_score)
    assert actual_band in ["Low", "Moderate", "High", "Very High"]

    # 5. Regressor check
    duration = float(model_manager.regressor.predict(df)[0])
    assert duration > 0.0
