import pytest
from backend.app.services.risk_service import RiskService

def test_risk_score_bounds():
    assert RiskService.calculate_risk_score(0.0) == 0
    assert RiskService.calculate_risk_score(0.5) == 50
    assert RiskService.calculate_risk_score(1.0) == 100
    assert RiskService.calculate_risk_score(1.05) == 100  # Overflow handle
    assert RiskService.calculate_risk_score(-0.05) == 0  # Underflow handle
    assert RiskService.calculate_risk_score(0.8129) == 81

def test_risk_band_mapping():
    assert RiskService.assign_risk_band(0) == "Low"
    assert RiskService.assign_risk_band(20) == "Low"
    assert RiskService.assign_risk_band(21) == "Moderate"
    assert RiskService.assign_risk_band(50) == "Moderate"
    assert RiskService.assign_risk_band(51) == "High"
    assert RiskService.assign_risk_band(80) == "High"
    assert RiskService.assign_risk_band(81) == "Very High"
    assert RiskService.assign_risk_band(100) == "Very High"

def test_monotonicity():
    probs = [0.05, 0.25, 0.55, 0.85]
    scores = [RiskService.calculate_risk_score(p) for p in probs]
    assert scores == sorted(scores)
    assert len(set(scores)) == len(scores)
