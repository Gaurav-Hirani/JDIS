from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ExplanationDetail(BaseModel):
    feature_name: str
    parent_feature: str
    feature_group: str
    human_readable_description: Optional[str] = None
    contribution: float
    direction: str
    feature_value: Optional[str] = None
    rank: int

class PredictionExplanationResponse(BaseModel):
    prediction_id: str
    model_version: str
    calibrated_probability: Optional[float] = None
    risk_score: Optional[int] = None
    risk_band: Optional[str] = None
    top_contributors: List[ExplanationDetail]
    summary: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
