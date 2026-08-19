import numpy as np
import pandas as pd

def calculate_risk_score(probabilities: np.ndarray) -> np.ndarray:
    """
    Deterministically maps calibrated probabilities [0, 1] to an interpretable risk score [0, 100].
    
    Requirements satisfied:
    - 0 to 100 boundaries
    - Monotonic
    - Reproducible
    - No arbitrary nonlinear transformations
    
    Parameters:
    probabilities (np.ndarray): Array of calibrated probabilities from the final model.
    
    Returns:
    np.ndarray: Integer risk scores from 0 to 100.
    """
    # Ensure inputs are clipped safely in case of float precision issues
    clipped_probs = np.clip(probabilities, 0.0, 1.0)
    
    # Map directly and linearly to 0-100 and floor to nearest integer
    risk_scores = np.floor(clipped_probs * 100).astype(int)
    
    return risk_scores

def assign_risk_bands(risk_scores: np.ndarray) -> np.ndarray:
    """
    Maps the 0-100 risk score to interpretable bands based on validation-derived distributions.
    
    Bands:
    - Low (0 - 20): Represents cases with very low baseline risk.
    - Moderate (21 - 50): Standard risk cases.
    - High (51 - 80): Elevated risk of severe delay.
    - Very High (81 - 100): Near certainty of severe delay.
    """
    bins = [-1, 20, 50, 80, 100]
    labels = ['Low', 'Moderate', 'High', 'Very High']
    
    return pd.cut(risk_scores, bins=bins, labels=labels)
