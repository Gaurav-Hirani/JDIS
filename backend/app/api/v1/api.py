from fastapi import APIRouter

from backend.app.api.v1.endpoints import (
    health,
    predictions,
    cases,
    analytics
)

api_router = APIRouter()

# Health router at root or under /api/v1
api_router.include_router(predictions.router, prefix="/predictions", tags=["Predictions & Risk"])
api_router.include_router(cases.router, prefix="/cases", tags=["Case Management"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics & KPIs"])
