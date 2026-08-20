import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.app.db.base import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class Explanation(Base):
    __tablename__ = "explanations"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    prediction_id = Column(String(36), ForeignKey("predictions.id", ondelete="CASCADE"), nullable=False, index=True)

    feature_name = Column(String(128), nullable=False)
    parent_feature = Column(String(128), nullable=False)
    feature_group = Column(String(64), nullable=False)
    human_readable_description = Column(Text, nullable=True)
    contribution = Column(Float, nullable=False)
    direction = Column(String(16), nullable=False)  # 'positive' (increases delay risk) or 'negative' (decreases delay risk)
    feature_value = Column(String(256), nullable=True)
    rank = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    prediction = relationship("Prediction", back_populates="explanations")
