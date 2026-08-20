from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Optional

from backend.app.db.session import get_db
from backend.app.schemas.prediction import (
    CaseFilingFeatures,
    RiskPredictionResponse,
    DurationPredictionResponse
)
from backend.app.schemas.explanation import (
    PredictionExplanationResponse,
    ExplanationDetail
)
from backend.app.services.prediction_service import PredictionService
from backend.app.services.explanation_service import ExplanationService
from backend.app.models.prediction import Prediction
from backend.app.core.errors import PredictionNotFoundException

router = APIRouter()

@router.post(
    "/delay",
    response_model=RiskPredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict Filing-Time Case Delay & Risk Score",
    description="Primary filing-time classification endpoint. Computes calibrated delay probability, JDIS risk score, risk band, and top SHAP feature contributions."
)
def predict_delay_risk(
    features: CaseFilingFeatures,
    save: bool = True,
    case_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Evaluates delay probability (>24 months) using the 29 Config D filing-time features.
    Strictly follows ML_INFERENCE_CONTRACT.md.
    """
    db_session = db if save else None
    return PredictionService.predict_delay(features=features, case_id=case_id, db=db_session)

@router.post(
    "/duration",
    response_model=DurationPredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict Expected Case Duration (Days)",
    description="Filing-time duration regression endpoint. Returns predicted duration days with documented model limitations."
)
def predict_case_duration(
    features: CaseFilingFeatures,
    save: bool = True,
    case_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Predicts expected case duration in days. Includes statutory warning flag regarding extreme outliers.
    """
    db_session = db if save else None
    return PredictionService.predict_duration(features=features, case_id=case_id, db=db_session)

@router.get(
    "/{prediction_id}/explanation",
    response_model=PredictionExplanationResponse,
    status_code=status.HTTP_200_OK,
    summary="Get SHAP Explanation for Prediction",
    description="Retrieves detailed SHAP feature attributions and human-readable narrative explanation for a specific prediction ID."
)
def get_prediction_explanation(
    prediction_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieves stored local SHAP explanation breakdown.
    """
    pred_obj = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not pred_obj:
        raise PredictionNotFoundException(prediction_id)

    details = []
    for exp in pred_obj.explanations:
        details.append(
            ExplanationDetail(
                feature_name=exp.feature_name,
                parent_feature=exp.parent_feature,
                feature_group=exp.feature_group,
                human_readable_description=exp.human_readable_description,
                contribution=exp.contribution,
                direction=exp.direction,
                feature_value=exp.feature_value,
                rank=exp.rank
            )
        )

    pos_drivers = [d.parent_feature for d in details if d.direction == "positive"][:2]
    neg_drivers = [d.parent_feature for d in details if d.direction == "negative"][:2]

    summary_parts = []
    if pos_drivers:
        summary_parts.append(f"Primary factors driving delay risk higher include: {', '.join(pos_drivers)}.")
    if neg_drivers:
        summary_parts.append(f"Mitigating factors pulling delay risk lower include: {', '.join(neg_drivers)}.")
    
    summary = " ".join(summary_parts) if summary_parts else "Delay risk reflects baseline court and case type throughput characteristics."

    return PredictionExplanationResponse(
        prediction_id=pred_obj.id,
        model_version=pred_obj.model_version,
        calibrated_probability=pred_obj.calibrated_probability,
        risk_score=pred_obj.risk_score,
        risk_band=pred_obj.risk_band,
        top_contributors=details,
        summary=summary,
        timestamp=pred_obj.created_at
    )
