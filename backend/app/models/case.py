import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from backend.app.db.base import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class Case(Base):
    __tablename__ = "cases"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    ddl_case_id = Column(String(64), nullable=True, index=True)

    # Basic Case Features
    filing_month = Column(Integer, nullable=True)
    filing_day_of_week = Column(Integer, nullable=True)
    filing_quarter = Column(Integer, nullable=True)
    type_name = Column(String(128), nullable=False, index=True)
    case_type_str = Column(String(128), nullable=True)
    case_category = Column(String(64), nullable=True)
    is_criminal_code = Column(Integer, nullable=True, default=0)
    statutory_act_count = Column(Integer, nullable=True, default=0)
    ipc_section_count = Column(Integer, nullable=True, default=0)
    bailable_ipc_flag = Column(String(32), nullable=True)
    primary_act_id = Column(String(128), nullable=True)

    # Demographic / Representation Features
    female_defendant_clean = Column(String(32), nullable=True)
    female_petitioner_clean = Column(String(32), nullable=True)
    female_adv_def_clean = Column(String(32), nullable=True)
    female_adv_pet_clean = Column(String(32), nullable=True)

    # Court & Geography Features
    state_code = Column(String(32), nullable=False, index=True)
    dist_code = Column(String(32), nullable=False, index=True)
    court_no = Column(String(32), nullable=False, index=True)
    state_str = Column(String(128), nullable=True)
    district_str = Column(String(128), nullable=True)
    court_str = Column(String(256), nullable=True)

    # Judge Features
    ddl_filing_judge_id = Column(String(64), nullable=True, index=True)
    judge_position_clean = Column(String(128), nullable=True)
    judge_gender = Column(String(32), nullable=True)
    judge_tenure_days = Column(Float, nullable=True)

    # Historical Throughput Features
    court_prior_delay_rate = Column(Float, nullable=True)
    court_prior_avg_duration = Column(Float, nullable=True)
    court_prior_active_backlog = Column(Float, nullable=True)
    casetype_prior_delay_rate = Column(Float, nullable=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    predictions = relationship("Prediction", back_populates="case", cascade="all, delete-orphan", order_by="desc(Prediction.created_at)")

    __table_args__ = (
        Index("ix_cases_state_dist_court", "state_code", "dist_code", "court_no"),
    )
