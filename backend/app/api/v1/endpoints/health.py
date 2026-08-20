from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.app.db.session import get_db
from backend.app.ml.manager import model_manager

router = APIRouter()

@router.get("/health", summary="System Health Check", tags=["System"])
def health_check(db: Session = Depends(get_db)):
    """
    Returns system health status:
    - API operational state
    - PostgreSQL database connectivity
    - ML model loading state and version metadata
    """
    db_status = "ok"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {str(e)}"

    ml_health = model_manager.get_health_status()

    overall_status = "ok" if (db_status == "ok" and ml_health["status"] == "ok") else "degraded"

    return {
        "status": overall_status,
        "database": db_status,
        "models": ml_health["status"],
        "model_version": ml_health["version"],
        "details": {
            "classifier_loaded": ml_health["classifier_loaded"],
            "regressor_loaded": ml_health["regressor_loaded"],
            "shap_ready": ml_health["shap_explainer_ready"]
        }
    }
