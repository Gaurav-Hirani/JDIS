import pytest
from pydantic import ValidationError
from backend.app.schemas.prediction import CaseFilingFeatures, RiskPredictionResponse
from backend.app.schemas.case import CaseCreate, CaseUpdate

def test_valid_case_filing_features(sample_case_features):
    features = CaseFilingFeatures(**sample_case_features)
    assert features.state_code == "01"
    assert features.type_name == "criminal appeal"
    assert features.filing_month == 5

def test_missing_required_fields():
    # Missing required state_code, dist_code, court_no, type_name
    invalid_data = {
        "filing_month": 5
    }
    with pytest.raises(ValidationError) as exc_info:
        CaseFilingFeatures(**invalid_data)
    
    errors = exc_info.value.errors()
    missing_fields = {e["loc"][0] for e in errors}
    assert "state_code" in missing_fields
    assert "dist_code" in missing_fields
    assert "court_no" in missing_fields
    assert "type_name" in missing_fields

def test_invalid_month_bounds(sample_case_features):
    invalid_data = sample_case_features.copy()
    invalid_data["filing_month"] = 13  # Month must be 1-12
    with pytest.raises(ValidationError):
        CaseFilingFeatures(**invalid_data)

def test_invalid_quarter_bounds(sample_case_features):
    invalid_data = sample_case_features.copy()
    invalid_data["filing_quarter"] = 5  # Quarter must be 1-4
    with pytest.raises(ValidationError):
        CaseFilingFeatures(**invalid_data)

def test_case_create_schema(sample_case_features):
    create_data = sample_case_features.copy()
    create_data["ddl_case_id"] = "case_12345"
    case = CaseCreate(**create_data)
    assert case.ddl_case_id == "case_12345"
