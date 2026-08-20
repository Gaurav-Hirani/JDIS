from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from backend.app.core.logging import logger

class JDISException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class ModelNotFoundException(JDISException):
    def __init__(self, message: str = "ML model artifact not found or could not be loaded"):
        super().__init__(message=message, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

class InferenceException(JDISException):
    def __init__(self, message: str = "Failed to run ML inference on provided features", details: dict = None):
        super().__init__(message=message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, details=details)

class CaseNotFoundException(JDISException):
    def __init__(self, case_id: str):
        super().__init__(message=f"Case with ID '{case_id}' was not found", status_code=status.HTTP_404_NOT_FOUND)

class PredictionNotFoundException(JDISException):
    def __init__(self, prediction_id: str):
        super().__init__(message=f"Prediction with ID '{prediction_id}' was not found", status_code=status.HTTP_404_NOT_FOUND)

async def jdis_exception_handler(request: Request, exc: JDISException) -> JSONResponse:
    logger.error(f"JDIS Domain Exception on {request.method} {request.url.path}: {exc.message} (details: {exc.details})")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.message,
            "details": exc.details,
            "path": request.url.path
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.warning(f"Validation Error on {request.method} {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": True,
            "message": "Input validation error",
            "details": exc.errors(),
            "path": request.url.path
        }
    )

async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(f"Unhandled Exception on {request.method} {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "An internal server error occurred. Please contact the administrator.",
            "path": request.url.path
        }
    )
