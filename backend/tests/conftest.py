import pytest
from typing import Generator, Dict, Any
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from backend.app.main import app
from backend.app.db.base import Base
from backend.app.db.session import get_db

# Use an in-memory SQLite database for isolated test execution
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def sample_case_features() -> Dict[str, Any]:
    """Sample payload containing the exact 29 Config D features."""
    return {
        "state_code": "01",
        "dist_code": "01",
        "court_no": "01",
        "type_name": "criminal appeal",
        "filing_month": 5,
        "filing_day_of_week": 2,
        "filing_quarter": 2,
        "case_type_str": "criminal",
        "case_category": "criminal",
        "is_criminal_code": 1,
        "statutory_act_count": 1,
        "ipc_section_count": 2,
        "bailable_ipc_flag": "bailable",
        "primary_act_id": "act_ipc",
        "female_defendant_clean": "0",
        "female_petitioner_clean": "0",
        "female_adv_def_clean": "0",
        "female_adv_pet_clean": "0",
        "state_str": "Maharashtra",
        "district_str": "Mumbai",
        "court_str": "Chief Metropolitan Magistrate",
        "ddl_filing_judge_id": "judge_101",
        "judge_position_clean": "magistrate",
        "judge_gender": "male",
        "judge_tenure_days": 500.0,
        "court_prior_delay_rate": 0.45,
        "court_prior_avg_duration": 650.0,
        "court_prior_active_backlog": 1200.0,
        "casetype_prior_delay_rate": 0.38
    }
