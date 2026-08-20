from typing import List, Optional, Literal
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class CaseFilingFeatures(BaseModel):
    # Required identifiers per ML_INFERENCE_CONTRACT.md
    state_code: str = Field(..., description="State code identifier", examples=["01"])
    dist_code: str = Field(..., description="District code identifier", examples=["01"])
    court_no: str = Field(..., description="Numeric court identifier", examples=["01"])
    type_name: str = Field(..., description="Granular case type name identifier", examples=["criminal appeal"])

    # Basic Case Features
    filing_month: Optional[int] = Field(default=1, description="Month of filing (1-12)", ge=1, le=12, examples=[5])
    filing_day_of_week: Optional[int] = Field(default=1, description="Day of week (0-6)", ge=0, le=6, examples=[2])
    filing_quarter: Optional[int] = Field(default=1, description="Quarter of filing (1-4)", ge=1, le=4, examples=[2])
    case_type_str: Optional[str] = Field(default="unknown", description="Standardized case type string", examples=["criminal"])
    case_category: Optional[str] = Field(default="unknown", description="Broad case category ID", examples=["criminal"])
    is_criminal_code: Optional[int] = Field(default=0, description="Civil vs Criminal code (1=Criminal, 0=Civil)", ge=0, le=1, examples=[1])
    statutory_act_count: Optional[int] = Field(default=0, description="Number of statutory acts involved", ge=0, examples=[1])
    ipc_section_count: Optional[int] = Field(default=0, description="Number of IPC sections cited", ge=0, examples=[2])
    bailable_ipc_flag: Optional[str] = Field(default="unknown", description="Indicator if IPC sections are bailable", examples=["bailable"])
    primary_act_id: Optional[str] = Field(default="unknown", description="Primary statutory act ID", examples=["act_ipc"])

    # Demographics / Representation
    female_defendant_clean: Optional[str] = Field(default="0", description="Indicator for female defendant presence", examples=["0"])
    female_petitioner_clean: Optional[str] = Field(default="0", description="Indicator for female petitioner presence", examples=["0"])
    female_adv_def_clean: Optional[str] = Field(default="0", description="Indicator for female defense advocate", examples=["0"])
    female_adv_pet_clean: Optional[str] = Field(default="0", description="Indicator for female petitioner advocate", examples=["0"])

    # Court & Geography Strings
    state_str: Optional[str] = Field(default="unknown", description="State name string", examples=["Maharashtra"])
    district_str: Optional[str] = Field(default="unknown", description="District name string", examples=["Mumbai"])
    court_str: Optional[str] = Field(default="unknown", description="Court establishment name string", examples=["Chief Metropolitan Magistrate"])

    # Judge Features
    ddl_filing_judge_id: Optional[str] = Field(default="unknown", description="Filing judge identifier", examples=["judge_101"])
    judge_position_clean: Optional[str] = Field(default="unknown", description="Standardized judge position", examples=["magistrate"])
    judge_gender: Optional[str] = Field(default="unknown", description="Judge gender", examples=["male"])
    judge_tenure_days: Optional[float] = Field(default=0.0, description="Judge tenure duration in days at filing", ge=0.0, examples=[500.0])

    # Historical Throughput Features
    court_prior_delay_rate: Optional[float] = Field(default=0.0, description="Historical delay rate of the court at filing", ge=0.0, le=1.0, examples=[0.45])
    court_prior_avg_duration: Optional[float] = Field(default=0.0, description="Historical average duration in days", ge=0.0, examples=[650.0])
    court_prior_active_backlog: Optional[float] = Field(default=0.0, description="Active backlog count at filing", ge=0.0, examples=[1200.0])
    casetype_prior_delay_rate: Optional[float] = Field(default=0.0, description="Historical delay rate for case type", ge=0.0, le=1.0, examples=[0.38])

    model_config = ConfigDict(extra="ignore")

class SHAPExplanationItem(BaseModel):
    feature_name: str = Field(..., description="Model feature name or parent concept")
    contribution: float = Field(..., description="SHAP contribution value (log-odds impact)")
    direction: Optional[str] = Field(default="positive", description="'positive' (increases risk) or 'negative' (decreases risk)")
    feature_group: Optional[str] = Field(default="General", description="Parent feature category group")
    human_readable_description: Optional[str] = Field(default=None, description="Human readable context")

class RiskPredictionResponse(BaseModel):
    prediction_id: Optional[str] = Field(default=None, description="Unique prediction UUID")
    case_id: Optional[str] = Field(default=None, description="Linked case ID if saved")
    raw_probability: float = Field(..., description="Uncalibrated probability from XGBoost", ge=0.0, le=1.0)
    calibrated_probability: float = Field(..., description="Calibrated probability from Isotonic Wrapper", ge=0.0, le=1.0)
    risk_score: int = Field(..., description="JDIS Risk Score (0-100), computed as floor(calibrated_probability * 100)", ge=0, le=100)
    risk_band: Literal["Low", "Moderate", "High", "Very High"] = Field(..., description="Interpretable risk band")
    model_version: str = Field(..., description="Serving model version identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Prediction timestamp")
    shap_explanations: List[SHAPExplanationItem] = Field(default_factory=list, description="Top SHAP feature contributions")

class DurationPredictionResponse(BaseModel):
    prediction_id: Optional[str] = Field(default=None, description="Unique prediction UUID")
    predicted_duration_days: float = Field(..., description="Predicted case duration in days")
    model_version: str = Field(..., description="Serving model version")
    limitations_flag: str = Field(..., description="Documented model limitation caveat")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Prediction timestamp")
