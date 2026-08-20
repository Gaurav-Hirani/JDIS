import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from backend.app.core.config import settings
from backend.app.core.logging import setup_logging, logger
from backend.app.core.errors import (
    JDISException,
    jdis_exception_handler,
    validation_exception_handler,
    generic_exception_handler
)
from backend.app.ml.manager import model_manager
from backend.app.db.session import engine
from backend.app.models.case import Base
from backend.app.api.v1.api import api_router
from backend.app.api.v1.endpoints import health

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Setup logging, ensure tables exist, load ML models once
    setup_logging()
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION} [{settings.ENVIRONMENT}]")
    
    # Initialize DB tables (for development/sqlite fallback if alembic hasn't run)
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database schema initialized.")
    except Exception as e:
        logger.warning(f"Database table verification error: {e}")

    # Centralized model loading
    try:
        model_manager.load_models()
    except Exception as e:
        logger.error(f"Failed to load ML models at startup: {e}")

    yield

    # Shutdown
    logger.info(f"Shutting down {settings.PROJECT_NAME}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
# Judicial Delay Intelligence System (JDIS) Backend API

Dedicated backend API serving frozen machine learning models, calibrated delay risk scoring, SHAP explainability, duration estimation, case management, and judicial analytics.

## Core Capabilities
- **Delay Risk Prediction**: 29 Config D filing-time features -> Calibrated probability, JDIS risk score, and risk bands.
- **Explainable AI (XAI)**: SHAP TreeExplainer local attribution mapped to conceptual parent features.
- **Duration Regression**: Expected case disposal duration (days) with stated limitations.
- **Case Management**: PostgreSQL storage, retrieval, and filtering.
- **Judicial Analytics**: Real-time KPI aggregation across courts, case types, and risk tiers.
""",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Request Timing / Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = (time.time() - start_time) * 1000.0
    logger.info(f"{request.method} {request.url.path} - Status: {response.status_code} - Duration: {duration_ms:.2f}ms")
    return response

# Exception Handlers
app.add_exception_handler(JDISException, jdis_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Mount Health Check at root /health and /api/v1/health
app.include_router(health.router, tags=["System"])
app.include_router(health.router, prefix=settings.API_V1_STR, tags=["System"])

# Mount API v1 Routes
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", include_in_schema=False)
def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs",
        "health_url": "/health",
        "api_v1_url": settings.API_V1_STR
    }
