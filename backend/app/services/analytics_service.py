from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from backend.app.models.case import Case
from backend.app.models.prediction import Prediction
from backend.app.schemas.analytics import (
    AnalyticsSummaryResponse,
    RiskDistributionItem,
    CourtRiskItem,
    CaseTypeRiskItem
)

class AnalyticsService:
    @staticmethod
    def get_summary(db: Session) -> AnalyticsSummaryResponse:
        """Calculates system-wide key metrics from stored cases and predictions."""
        total_cases = db.query(Case).count()
        total_predictions = db.query(Prediction).count()

        if total_predictions == 0:
            return AnalyticsSummaryResponse(
                total_cases=total_cases,
                total_predictions=0,
                high_risk_cases_count=0,
                high_risk_cases_percentage=0.0,
                average_risk_score=0.0,
                average_predicted_duration_days=0.0
            )

        high_risk_count = db.query(Prediction).filter(
            Prediction.risk_band.in_(["High", "Very High"])
        ).count()

        avg_score = db.query(func.avg(Prediction.risk_score)).filter(
            Prediction.risk_score.isnot(None)
        ).scalar() or 0.0

        avg_duration = db.query(func.avg(Prediction.predicted_duration_days)).filter(
            Prediction.predicted_duration_days.isnot(None)
        ).scalar() or 0.0

        high_risk_pct = round((high_risk_count / total_predictions) * 100.0, 2)

        return AnalyticsSummaryResponse(
            total_cases=total_cases,
            total_predictions=total_predictions,
            high_risk_cases_count=high_risk_count,
            high_risk_cases_percentage=high_risk_pct,
            average_risk_score=round(float(avg_score), 2),
            average_predicted_duration_days=round(float(avg_duration), 1)
        )

    @staticmethod
    def get_risk_distribution(db: Session) -> List[RiskDistributionItem]:
        """Calculates the proportion of predictions falling into each risk band."""
        total_preds = db.query(Prediction).filter(Prediction.risk_band.isnot(None)).count()

        if total_preds == 0:
            return [
                RiskDistributionItem(risk_band=b, count=0, percentage=0.0)
                for b in ["Low", "Moderate", "High", "Very High"]
            ]

        band_counts = db.query(
            Prediction.risk_band,
            func.count(Prediction.id).label("count")
        ).filter(
            Prediction.risk_band.isnot(None)
        ).group_by(
            Prediction.risk_band
        ).all()

        count_dict = {b: 0 for b in ["Low", "Moderate", "High", "Very High"]}
        for band, count in band_counts:
            if band in count_dict:
                count_dict[band] = count

        return [
            RiskDistributionItem(
                risk_band=b,
                count=count_dict[b],
                percentage=round((count_dict[b] / total_preds) * 100.0, 2)
            )
            for b in ["Low", "Moderate", "High", "Very High"]
        ]

    @staticmethod
    def get_court_analytics(db: Session, limit: int = 15) -> List[CourtRiskItem]:
        """Aggregates caseload and risk scores by court establishment."""
        results = db.query(
            Case.state_code,
            Case.dist_code,
            Case.court_no,
            func.count(Case.id).label("case_count"),
            func.avg(Prediction.risk_score).label("avg_risk"),
            func.avg(Prediction.predicted_duration_days).label("avg_duration"),
            func.sum(
                case((Prediction.risk_band.in_(["High", "Very High"]), 1), else_=0)
            ).label("high_risk_count")
        ).join(
            Prediction, Case.id == Prediction.case_id, isouter=True
        ).group_by(
            Case.state_code, Case.dist_code, Case.court_no
        ).order_by(
            func.count(Case.id).desc()
        ).limit(limit).all()

        items: List[CourtRiskItem] = []
        for state, dist, court, count, avg_risk, avg_dur, high_risk in results:
            court_id = f"State {state} / Dist {dist} / Court {court}"
            high_pct = round((float(high_risk or 0) / count) * 100.0, 2) if count > 0 else 0.0
            items.append(
                CourtRiskItem(
                    court_identifier=court_id,
                    state_code=state,
                    dist_code=dist,
                    court_no=court,
                    case_count=count,
                    average_risk_score=round(float(avg_risk or 0.0), 2),
                    high_risk_percentage=high_pct,
                    average_duration_days=round(float(avg_dur or 0.0), 1)
                )
            )
        return items

    @staticmethod
    def get_case_type_analytics(db: Session, limit: int = 15) -> List[CaseTypeRiskItem]:
        """Aggregates delay likelihood across case types."""
        results = db.query(
            Case.type_name,
            func.count(Case.id).label("case_count"),
            func.avg(Prediction.risk_score).label("avg_risk"),
            func.sum(
                case((Prediction.risk_band.in_(["High", "Very High"]), 1), else_=0)
            ).label("high_risk_count")
        ).join(
            Prediction, Case.id == Prediction.case_id, isouter=True
        ).group_by(
            Case.type_name
        ).order_by(
            func.count(Case.id).desc()
        ).limit(limit).all()

        items: List[CaseTypeRiskItem] = []
        for type_name, count, avg_risk, high_risk in results:
            high_pct = round((float(high_risk or 0) / count) * 100.0, 2) if count > 0 else 0.0
            items.append(
                CaseTypeRiskItem(
                    type_name=type_name,
                    case_count=count,
                    average_risk_score=round(float(avg_risk or 0.0), 2),
                    high_risk_percentage=high_pct
                )
            )
        return items
