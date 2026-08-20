from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from backend.app.db.session import get_db
from backend.app.schemas.case import (
    CaseCreate,
    CaseUpdate,
    CaseResponse,
    CaseDetailResponse,
    CaseListResponse
)
from backend.app.services.case_service import CaseService

router = APIRouter()

@router.post(
    "",
    response_model=CaseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Case & Run Initial Prediction",
    description="Registers a new judicial case filing in PostgreSQL and automatically executes the frozen filing-time prediction model."
)
def create_case(
    case_in: CaseCreate,
    auto_predict: bool = Query(True, description="Automatically calculate and attach initial delay risk prediction"),
    db: Session = Depends(get_db)
):
    return CaseService.create_case(case_in=case_in, db=db, auto_predict=auto_predict)

@router.get(
    "/{case_id}",
    response_model=CaseDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Case Details by ID",
    description="Retrieves a specific case record including complete historical prediction runs and risk assessments."
)
def get_case_by_id(
    case_id: str,
    db: Session = Depends(get_db)
):
    return CaseService.get_case(case_id=case_id, db=db)

@router.get(
    "",
    response_model=CaseListResponse,
    status_code=status.HTTP_200_OK,
    summary="List & Filter Cases",
    description="Lists cases with pagination and optional filtering by jurisdiction, case type, and risk band."
)
def list_cases(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    state_code: Optional[str] = Query(None, description="Filter by state code"),
    dist_code: Optional[str] = Query(None, description="Filter by district code"),
    court_no: Optional[str] = Query(None, description="Filter by court number"),
    type_name: Optional[str] = Query(None, description="Search by case type name"),
    risk_band: Optional[str] = Query(None, description="Filter by risk band (Low, Moderate, High, Very High)"),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * page_size
    return CaseService.list_cases(
        db=db,
        skip=skip,
        limit=page_size,
        state_code=state_code,
        dist_code=dist_code,
        court_no=court_no,
        type_name=type_name,
        risk_band=risk_band
    )

@router.patch(
    "/{case_id}",
    response_model=CaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Case Metadata",
    description="Updates supported case attributes."
)
def update_case(
    case_id: str,
    case_in: CaseUpdate,
    db: Session = Depends(get_db)
):
    return CaseService.update_case(case_id=case_id, case_in=case_in, db=db)
