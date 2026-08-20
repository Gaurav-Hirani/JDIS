from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from backend.app.schemas.prediction import CaseFilingFeatures, RiskPredictionResponse

class CaseCreate(CaseFilingFeatures):
    ddl_case_id: Optional[str] = Field(default=None, description="External case identifier", examples=["case_987654"])

class CaseUpdate(BaseModel):
    state_code: Optional[str] = None
    dist_code: Optional[str] = None
    court_no: Optional[str] = None
    type_name: Optional[str] = None
    state_str: Optional[str] = None
    district_str: Optional[str] = None
    court_str: Optional[str] = None
    ddl_filing_judge_id: Optional[str] = None
    judge_position_clean: Optional[str] = None
    judge_gender: Optional[str] = None
    judge_tenure_days: Optional[float] = None
    court_prior_delay_rate: Optional[float] = None
    court_prior_avg_duration: Optional[float] = None
    court_prior_active_backlog: Optional[float] = None
    casetype_prior_delay_rate: Optional[float] = None

class PredictionSummary(BaseModel):
    id: str
    model_version: str
    prediction_type: str
    raw_probability: Optional[float] = None
    calibrated_probability: Optional[float] = None
    risk_score: Optional[int] = None
    risk_band: Optional[str] = None
    predicted_duration_days: Optional[float] = None
    limitations_flag: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CaseResponse(CaseFilingFeatures):
    id: str
    ddl_case_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    latest_prediction: Optional[PredictionSummary] = None

    model_config = ConfigDict(from_attributes=True)

class CaseDetailResponse(CaseResponse):
    predictions: List[PredictionSummary] = []

class CaseListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[CaseResponse]
