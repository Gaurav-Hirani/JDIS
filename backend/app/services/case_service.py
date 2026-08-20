import uuid
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from backend.app.models.case import Case
from backend.app.models.prediction import Prediction
from backend.app.schemas.case import (
    CaseCreate,
    CaseUpdate,
    CaseResponse,
    CaseDetailResponse,
    CaseListResponse,
    PredictionSummary
)
from backend.app.schemas.prediction import CaseFilingFeatures
from backend.app.services.prediction_service import PredictionService
from backend.app.core.errors import CaseNotFoundException
from backend.app.core.logging import logger

class CaseService:
    @staticmethod
    def create_case(case_in: CaseCreate, db: Session, auto_predict: bool = True) -> CaseResponse:
        """Creates a new case record and runs an initial baseline prediction."""
        case_dict = case_in.model_dump()
        case_id = str(uuid.uuid4())
        case_dict["id"] = case_id

        case_obj = Case(**case_dict)
        db.add(case_obj)
        db.commit()
        db.refresh(case_obj)

        latest_pred_summary = None

        if auto_predict:
            try:
                features = CaseFilingFeatures(**case_in.model_dump())
                pred_res = PredictionService.predict_delay(features=features, case_id=case_id, db=db)
                latest_pred_summary = PredictionSummary(
                    id=pred_res.prediction_id,
                    model_version=pred_res.model_version,
                    prediction_type="delay_classification",
                    raw_probability=pred_res.raw_probability,
                    calibrated_probability=pred_res.calibrated_probability,
                    risk_score=pred_res.risk_score,
                    risk_band=pred_res.risk_band,
                    created_at=pred_res.timestamp
                )
            except Exception as e:
                logger.warning(f"Automatic prediction on case creation failed: {e}")

        response = CaseResponse.model_validate(case_obj)
        response.latest_prediction = latest_pred_summary
        return response

    @staticmethod
    def get_case(case_id: str, db: Session) -> CaseDetailResponse:
        """Retrieves a single case with complete prediction history."""
        case_obj = db.query(Case).filter(Case.id == case_id).first()
        if not case_obj:
            raise CaseNotFoundException(case_id)

        predictions_summary = [
            PredictionSummary.model_validate(p) for p in case_obj.predictions
        ]

        response = CaseDetailResponse.model_validate(case_obj)
        response.predictions = predictions_summary
        if predictions_summary:
            response.latest_prediction = predictions_summary[0]
        return response

    @staticmethod
    def list_cases(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        state_code: Optional[str] = None,
        dist_code: Optional[str] = None,
        court_no: Optional[str] = None,
        type_name: Optional[str] = None,
        risk_band: Optional[str] = None
    ) -> CaseListResponse:
        """Retrieves a paginated and filtered list of cases."""
        query = db.query(Case)

        if state_code:
            query = query.filter(Case.state_code == state_code)
        if dist_code:
            query = query.filter(Case.dist_code == dist_code)
        if court_no:
            query = query.filter(Case.court_no == court_no)
        if type_name:
            query = query.filter(Case.type_name.ilike(f"%{type_name}%"))
        if risk_band:
            query = query.join(Case.predictions).filter(Prediction.risk_band == risk_band)

        total = query.count()
        cases = query.order_by(desc(Case.created_at)).offset(skip).limit(limit).all()

        items = []
        for c in cases:
            item = CaseResponse.model_validate(c)
            if c.predictions:
                item.latest_prediction = PredictionSummary.model_validate(c.predictions[0])
            items.append(item)

        page = (skip // limit) + 1 if limit > 0 else 1
        return CaseListResponse(total=total, page=page, page_size=limit, items=items)

    @staticmethod
    def update_case(case_id: str, case_in: CaseUpdate, db: Session) -> CaseResponse:
        """Updates case details and re-predicts if key attributes changed."""
        case_obj = db.query(Case).filter(Case.id == case_id).first()
        if not case_obj:
            raise CaseNotFoundException(case_id)

        update_data = case_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(case_obj, field, value)

        db.commit()
        db.refresh(case_obj)

        item = CaseResponse.model_validate(case_obj)
        if case_obj.predictions:
            item.latest_prediction = PredictionSummary.model_validate(case_obj.predictions[0])
        return item
