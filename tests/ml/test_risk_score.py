import numpy as np
from src.risk.risk_score import calculate_risk_score, assign_risk_bands

def test_risk_score_bounds():
    probs = np.array([0.0, 0.5, 1.0, 1.00001, -0.00001])
    scores = calculate_risk_score(probs)
    
    assert scores[0] == 0, "Probability 0 should map to score 0"
    assert scores[2] == 100, "Probability 1 should map to score 100"
    assert scores[3] == 100, "Should handle float overflow"
    assert scores[4] == 0, "Should handle float underflow"
    assert np.all((scores >= 0) & (scores <= 100)), "Scores must remain within 0-100 bounds"

def test_risk_score_monotonicity():
    probs = np.array([0.1, 0.2, 0.3, 0.9])
    scores = calculate_risk_score(probs)
    assert np.all(np.diff(scores) > 0), "Risk scores must be strictly monotonic for strictly increasing probabilities spanning integer bounds"

def test_risk_bands():
    scores = np.array([0, 10, 20, 21, 50, 51, 80, 81, 100])
    bands = assign_risk_bands(scores)
    
    assert bands[0] == 'Low'
    assert bands[2] == 'Low'
    assert bands[3] == 'Moderate'
    assert bands[4] == 'Moderate'
    assert bands[5] == 'High'
    assert bands[6] == 'High'
    assert bands[7] == 'Very High'
    assert bands[8] == 'Very High'
