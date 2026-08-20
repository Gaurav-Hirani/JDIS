import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session

from backend.app.ml.manager import model_manager
from backend.app.core.logging import logger
from backend.app.core.errors import ModelNotFoundException, InferenceException
from backend.app.schemas.prediction import (
    CaseFilingFeatures,
    RiskPredictionResponse,
    DurationPredictionResponse,
    SHAPExplanationItem
)
from backend.app.services.risk_service import RiskService
from backend.app.services.explanation_service import ExplanationService
from backend.app.models.prediction import Prediction
from backend.app.models.explanation import Explanation

# Exact 29 feature column order for Config D
FEATURE_COLUMNS_CONFIG_D = [
    'filing_month',
    'filing_day_of_week',
    'filing_quarter',
    'type_name',
    'case_type_str',
    'case_category',
    'is_criminal_code',
    'statutory_act_count',
    'ipc_section_count',
    'bailable_ipc_flag',
    'primary_act_id',
    'female_defendant_clean',
    'female_petitioner_clean',
    'female_adv_def_clean',
    'female_adv_pet_clean',
    'state_code',
    'dist_code',
    'court_no',
    'state_str',
    'district_str',
    'court_str',
    'ddl_filing_judge_id',
    'judge_position_clean',
    'judge_gender',
    'judge_tenure_days',
    'court_prior_delay_rate',
    'court_prior_avg_duration',
    'court_prior_active_backlog',
    'casetype_prior_delay_rate'
]

class PredictionService:
    @staticmethod
    def features_to_dataframe(features: CaseFilingFeatures) -> pd.DataFrame:
        """Converts CaseFilingFeatures to a single-row DataFrame matching the 29 Config D columns."""
        data_dict = features.model_dump()
        row = {col: [data_dict.get(col)] for col in FEATURE_COLUMNS_CONFIG_D}
        return pd.DataFrame(row)

    @classmethod
    def predict_delay(
        cls,
        features: CaseFilingFeatures,
        case_id: Optional[str] = None,
        db: Optional[Session] = None
    ) -> RiskPredictionResponse:
        """Executes filing-time delay classification and calibration."""
        if not model_manager.is_loaded or model_manager.classifier is None:
            logger.error("Attempted prediction while models are not loaded.")
            raise ModelNotFoundException()

        try:
            df = cls.features_to_dataframe(features)

            # 1. Calibrated Probability
            calibrated_prob = float(model_manager.classifier.predict_proba(df)[:, 1][0])
            calibrated_prob = max(0.0, min(1.0, calibrated_prob))

            # 2. Raw Probability from base estimator
            raw_prob = calibrated_prob
            if model_manager.base_pipeline is not None:
                try:
                    raw_prob = float(model_manager.base_pipeline.predict_proba(df)[:, 1][0])
                    raw_prob = max(0.0, min(1.0, raw_prob))
                except Exception as e:
                    logger.debug(f"Could not compute separate raw probability; falling back to calibrated: {e}")
                    raw_prob = calibrated_prob

            # 3. Deterministic Risk Score & Band
            risk_score = RiskService.calculate_risk_score(calibrated_prob)
            risk_band = RiskService.assign_risk_band(risk_score)

            # 4. SHAP Local Attributions
            shap_explanations: List[SHAPExplanationItem] = ExplanationService.explain_instance(df, top_n=5)

            prediction_id = str(uuid.uuid4())
            now = datetime.now(timezone.utc)

            # 5. Persist to DB if session provided
            if db is not None:
                try:
                    pred_record = Prediction(
                        id=prediction_id,
                        case_id=case_id,
                        model_version=model_manager.model_version,
                        prediction_type="delay_classification",
                        raw_probability=raw_prob,
                        calibrated_probability=calibrated_prob,
                        risk_score=risk_score,
                        risk_band=risk_band,
                        created_at=now
                    )
                    db.add(pred_record)

                    for rank, exp in enumerate(shap_explanations, 1):
                        parent, group, desc = ExplanationService.map_feature_to_parent(exp.feature_name)
                        exp_record = Explanation(
                            id=str(uuid.uuid4()),
                            prediction_id=prediction_id,
                            feature_name=exp.feature_name,
                            parent_feature=parent,
                            feature_group=exp.feature_group or group,
                            human_readable_description=exp.human_readable_description or desc,
                            contribution=exp.contribution,
                            direction=exp.direction or ("positive" if exp.contribution >= 0 else "negative"),
                            rank=rank,
                            created_at=now
                        )
                        db.add(exp_record)

                    db.commit()
                except Exception as db_err:
                    db.rollback()
                    logger.warning(f"Failed to persist prediction record to database: {db_err}")

            return RiskPredictionResponse(
                prediction_id=prediction_id,
                case_id=case_id,
                raw_probability=round(raw_prob, 4),
                calibrated_probability=round(calibrated_prob, 4),
                risk_score=risk_score,
                risk_band=risk_band,
                model_version=model_manager.model_version,
                timestamp=now,
                shap_explanations=shap_explanations
            )

        except Exception as e:
            logger.exception(f"Prediction failed: {str(e)}")
            raise InferenceException(f"Failed to generate delay prediction: {str(e)}")

    @classmethod
    def predict_duration(
        cls,
        features: CaseFilingFeatures,
        case_id: Optional[str] = None,
        db: Optional[Session] = None
    ) -> DurationPredictionResponse:
        """Executes filing-time case duration regression."""
        if not model_manager.is_loaded or model_manager.regressor is None:
            logger.error("Duration regressor not loaded.")
            raise ModelNotFoundException("Duration regressor is not loaded.")

        try:
            df = cls.features_to_dataframe(features)
            raw_duration = float(model_manager.regressor.predict(df)[0])
            predicted_days = max(1.0, round(raw_duration, 1))

            limitations_msg = "Systematically underpredicts extreme outliers (>5 years). Associational estimate only."
            prediction_id = str(uuid.uuid4())
            now = datetime.now(timezone.utc)

            # Persist if DB session provided
            if db is not None:
                try:
                    pred_record = Prediction(
                        id=prediction_id,
                        case_id=case_id,
                        model_version=model_manager.model_version,
                        prediction_type="duration_regression",
                        predicted_duration_days=predicted_days,
                        limitations_flag=limitations_msg,
                        created_at=now
                    )
                    db.add(pred_record)
                    db.commit()
                except Exception as db_err:
                    db.rollback()
                    logger.warning(f"Failed to persist duration prediction record: {db_err}")

            return DurationPredictionResponse(
                prediction_id=prediction_id,
                predicted_duration_days=predicted_days,
                model_version=model_manager.model_version,
                limitations_flag=limitations_msg,
                timestamp=now
            )

        except Exception as e:
            logger.exception(f"Duration prediction failed: {str(e)}")
            raise InferenceException(f"Failed to generate duration prediction: {str(e)}")
