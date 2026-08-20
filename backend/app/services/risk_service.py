import math
from typing import Literal

RiskBandType = Literal["Low", "Moderate", "High", "Very High"]

class RiskService:
    @staticmethod
    def calculate_risk_score(calibrated_probability: float) -> int:
        """
        Deterministically calculates the JDIS integer risk score:
        score = floor(calibrated_probability * 100)
        
        Strict bounds: 0 to 100
        """
        clipped_prob = max(0.0, min(1.0, float(calibrated_probability)))
        score = int(math.floor(clipped_prob * 100.0))
        return max(0, min(100, score))

    @staticmethod
    def assign_risk_band(risk_score: int) -> RiskBandType:
        """
        Maps the 0-100 risk score to interpretable product bands:
        - Low (0 - 20): Baseline risk
        - Moderate (21 - 50): Standard operational risk
        - High (51 - 80): Elevated risk of severe delay (>24m)
        - Very High (81 - 100): High certainty of severe delay
        """
        if risk_score <= 20:
            return "Low"
        elif risk_score <= 50:
            return "Moderate"
        elif risk_score <= 80:
            return "High"
        else:
            return "Very High"
