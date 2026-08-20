from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List

from backend.app.db.session import get_db
from backend.app.schemas.analytics import (
    AnalyticsSummaryResponse,
    RiskDistributionItem,
    CourtRiskItem,
    CaseTypeRiskItem
)
from backend.app.services.analytics_service import AnalyticsService

router = APIRouter()

@router.get(
    "/summary",
    response_model=AnalyticsSummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="System Analytics Summary",
    description="Returns aggregate key performance indicators including total cases, high-risk case proportion, and average duration."
)
def get_analytics_summary(db: Session = Depends(get_db)):
    return AnalyticsService.get_summary(db=db)

@router.get(
    "/risk-distribution",
    response_model=List[RiskDistributionItem],
    status_code=status.HTTP_200_OK,
    summary="Risk Band Distribution",
    description="Returns the distribution count and percentage across Low, Moderate, High, and Very High risk bands."
)
def get_risk_distribution(db: Session = Depends(get_db)):
    return AnalyticsService.get_risk_distribution(db=db)

@router.get(
    "/courts",
    response_model=List[CourtRiskItem],
    status_code=status.HTTP_200_OK,
    summary="Court-Level Delay Analytics",
    description="Returns court establishment delay metrics, average risk score, and high-risk case frequency."
)
def get_court_analytics(
    limit: int = Query(15, ge=1, le=50, description="Max number of courts to return"),
    db: Session = Depends(get_db)
):
    return AnalyticsService.get_court_analytics(db=db, limit=limit)

@router.get(
    "/case-types",
    response_model=List[CaseTypeRiskItem],
    status_code=status.HTTP_200_OK,
    summary="Case-Type Delay Analytics",
    description="Returns delay risk rates and case counts grouped by procedural case type identifier."
)
def get_case_type_analytics(
    limit: int = Query(15, ge=1, le=50, description="Max number of case types to return"),
    db: Session = Depends(get_db)
):
    return AnalyticsService.get_case_type_analytics(db=db, limit=limit)
