import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.app.db.base import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    case_id = Column(String(36), ForeignKey("cases.id", ondelete="CASCADE"), nullable=True, index=True)
    model_version = Column(String(64), nullable=False)
    prediction_type = Column(String(32), nullable=False, default="delay_classification")  # 'delay_classification' or 'duration_regression'

    # Delay Classification Metrics
    raw_probability = Column(Float, nullable=True)
    calibrated_probability = Column(Float, nullable=True)
    risk_score = Column(Integer, nullable=True, index=True)
    risk_band = Column(String(32), nullable=True, index=True)  # Low, Moderate, High, Very High

    # Duration Regression Metrics
    predicted_duration_days = Column(Float, nullable=True)
    limitations_flag = Column(Text, nullable=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)

    # Relationships
    case = relationship("Case", back_populates="predictions")
    explanations = relationship("Explanation", back_populates="prediction", cascade="all, delete-orphan", order_by="Explanation.rank")
