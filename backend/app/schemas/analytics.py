from typing import List, Dict, Any
from pydantic import BaseModel, Field

class RiskDistributionItem(BaseModel):
    risk_band: str = Field(..., description="Risk band: Low, Moderate, High, Very High")
    count: int = Field(..., description="Number of cases in this band")
    percentage: float = Field(..., description="Percentage of total cases in this band")

class AnalyticsSummaryResponse(BaseModel):
    total_cases: int
    total_predictions: int
    high_risk_cases_count: int
    high_risk_cases_percentage: float
    average_risk_score: float
    average_predicted_duration_days: float

class CourtRiskItem(BaseModel):
    court_identifier: str
    state_code: str
    dist_code: str
    court_no: str
    case_count: int
    average_risk_score: float
    high_risk_percentage: float
    average_duration_days: float

class CaseTypeRiskItem(BaseModel):
    type_name: str
    case_count: int
    average_risk_score: float
    high_risk_percentage: float
