from typing import List, Dict, Any, Tuple, Optional
import pandas as pd
import numpy as np
from backend.app.ml.manager import model_manager
from backend.app.schemas.prediction import SHAPExplanationItem
from backend.app.schemas.explanation import ExplanationDetail, PredictionExplanationResponse
from backend.app.core.logging import logger

PARENT_MAPPING: Dict[str, Tuple[str, str, str]] = {
    'filing_month': ('filing_month', 'Basic Case', 'Month of case filing'),
    'filing_day_of_week': ('filing_day_of_week', 'Basic Case', 'Day of the week of case filing'),
    'filing_quarter': ('filing_quarter', 'Basic Case', 'Quarter of case filing'),
    'type_name_': ('type_name', 'Basic Case', 'Granular case type identifier'),
    'case_type_str_': ('case_type_str', 'Basic Case', 'Standardized case type category'),
    'case_category': ('case_category', 'Basic Case', 'Broad case classification category'),
    'is_criminal_code': ('is_criminal_code', 'Basic Case', 'Civil vs Criminal jurisdiction code'),
    'statutory_act_count': ('statutory_act_count', 'Basic Case', 'Number of statutory acts involved'),
    'ipc_section_count': ('ipc_section_count', 'Basic Case', 'Number of IPC sections cited'),
    'bailable_ipc_flag': ('bailable_ipc_flag', 'Basic Case', 'Bailable vs Non-bailable IPC offenses'),
    'primary_act_id_': ('primary_act_id', 'Basic Case', 'Primary statutory governing act'),
    'female_defendant_clean': ('female_defendant_clean', 'Demographics', 'Presence of female defendant'),
    'female_petitioner_clean': ('female_petitioner_clean', 'Demographics', 'Presence of female petitioner'),
    'female_adv_def_clean': ('female_adv_def_clean', 'Demographics', 'Female defense legal counsel representation'),
    'female_adv_pet_clean': ('female_adv_pet_clean', 'Demographics', 'Female petitioner legal counsel representation'),
    'state_code_': ('state_code', 'Court Geography', 'State judicial jurisdiction'),
    'dist_code_': ('dist_code', 'Court Geography', 'District judicial administrative region'),
    'court_no_': ('court_no', 'Court Geography', 'Specific courtroom establishment number'),
    'state_str_': ('state_str', 'Court Geography', 'State jurisdictional name'),
    'district_str_': ('district_str', 'Court Geography', 'District jurisdictional establishment'),
    'court_str_': ('court_str', 'Court Geography', 'Court establishment name'),
    'ddl_filing_judge_id_': ('ddl_filing_judge_id', 'Judge Attributes', 'Filing judge historical assignment ID'),
    'judge_position_clean_': ('judge_position_clean', 'Judge Attributes', 'Standardized judicial seniority position'),
    'judge_gender_': ('judge_gender', 'Judge Attributes', 'Judge gender designation'),
    'judge_tenure_days': ('judge_tenure_days', 'Judge Attributes', 'Judicial tenure duration at time of filing'),
    'court_prior_delay_rate': ('court_prior_delay_rate', 'Historical Throughput', 'Historical court delay baseline (>24m rate)'),
    'court_prior_avg_duration': ('court_prior_avg_duration', 'Historical Throughput', 'Court historical average disposal duration (days)'),
    'court_prior_active_backlog': ('court_prior_active_backlog', 'Historical Throughput', 'Active pending case backlog at time of filing'),
    'casetype_prior_delay_rate': ('casetype_prior_delay_rate', 'Historical Throughput', 'Historical delay rate for this specific case type')
}

class ExplanationService:
    @staticmethod
    def map_feature_to_parent(feature_name: str) -> Tuple[str, str, str]:
        """Maps transformed model feature name to its parent concept, group, and human-readable description."""
        for prefix, (parent, group, desc) in PARENT_MAPPING.items():
            if feature_name.startswith(prefix) or feature_name == parent:
                return parent, group, desc
        return feature_name, "Other", f"Feature: {feature_name}"

    @classmethod
    def explain_instance(
        cls,
        df_row: pd.DataFrame,
        top_n: int = 5
    ) -> List[SHAPExplanationItem]:
        """
        Calculates local SHAP explanation for a single case input vector.
        Aggregates one-hot contributions into conceptual parent features.
        """
        if not model_manager.is_loaded or model_manager.explainer is None:
            logger.warning("SHAP Explainer not available in ModelManager; returning empty explanations")
            return []

        try:
            preprocessor = model_manager.preprocessor
            feature_names = model_manager.feature_names
            explainer = model_manager.explainer

            # Transform raw features
            X_trans = preprocessor.transform(df_row)
            X_dense = X_trans.toarray() if hasattr(X_trans, "toarray") else X_trans
            X_df = pd.DataFrame(X_dense, columns=feature_names)

            # Compute SHAP values
            shap_values = explainer.shap_values(X_df)
            case_shap = shap_values[0]

            # Aggregate SHAP contributions by parent feature
            parent_contributions: Dict[str, Dict[str, Any]] = {}
            for i, feat_name in enumerate(feature_names):
                val_contrib = float(case_shap[i])
                if abs(val_contrib) < 1e-5:
                    continue

                parent, group, desc = cls.map_feature_to_parent(feat_name)
                
                if parent not in parent_contributions:
                    parent_contributions[parent] = {
                        "contribution": 0.0,
                        "feature_group": group,
                        "description": desc,
                        "components": []
                    }
                
                parent_contributions[parent]["contribution"] += val_contrib
                parent_contributions[parent]["components"].append((feat_name, val_contrib))

            # Sort parents by magnitude of total contribution
            sorted_parents = sorted(
                parent_contributions.items(),
                key=lambda x: abs(x[1]["contribution"]),
                reverse=True
            )

            results: List[SHAPExplanationItem] = []
            for parent, info in sorted_parents[:top_n]:
                contrib = round(info["contribution"], 4)
                direction = "positive" if contrib >= 0 else "negative"
                results.append(
                    SHAPExplanationItem(
                        feature_name=parent,
                        contribution=contrib,
                        direction=direction,
                        feature_group=info["feature_group"],
                        human_readable_description=info["description"]
                    )
                )

            return results

        except Exception as e:
            logger.exception(f"Error computing local SHAP explanation: {str(e)}")
            return []

    @classmethod
    def get_detailed_explanation(
        cls,
        df_row: pd.DataFrame,
        prediction_id: str,
        calibrated_prob: Optional[float] = None,
        risk_score: Optional[int] = None,
        risk_band: Optional[str] = None,
        top_n: int = 8
    ) -> PredictionExplanationResponse:
        """Generates comprehensive explanation with summary narrative."""
        items = cls.explain_instance(df_row, top_n=top_n)

        details: List[ExplanationDetail] = []
        for rank, item in enumerate(items, 1):
            parent, group, desc = cls.map_feature_to_parent(item.feature_name)
            details.append(
                ExplanationDetail(
                    feature_name=item.feature_name,
                    parent_feature=parent,
                    feature_group=item.feature_group or group,
                    human_readable_description=item.human_readable_description or desc,
                    contribution=item.contribution,
                    direction=item.direction,
                    rank=rank
                )
            )

        # Generate human-readable narrative summary
        pos_drivers = [d.parent_feature for d in details if d.direction == "positive"][:2]
        neg_drivers = [d.parent_feature for d in details if d.direction == "negative"][:2]

        summary_parts = []
        if pos_drivers:
            summary_parts.append(f"Primary factors driving delay risk higher include: {', '.join(pos_drivers)}.")
        if neg_drivers:
            summary_parts.append(f"Mitigating factors pulling delay risk lower include: {', '.join(neg_drivers)}.")
        
        summary = " ".join(summary_parts) if summary_parts else "Delay risk reflects baseline court and case type throughput characteristics."

        return PredictionExplanationResponse(
            prediction_id=prediction_id,
            model_version=model_manager.model_version,
            calibrated_probability=calibrated_prob,
            risk_score=risk_score,
            risk_band=risk_band,
            top_contributors=details,
            summary=summary
        )
