import pytest
from datetime import date

from app.processing.applicant_data import (
    validate_applicant_data,
    extract_domain_facts
)

def test_validate_applicant_data_with_valid_input():
    applicant_data = {
        "full_name": "Иванов Иван Иванович",
        "passport": "1234567890",
        "tax_id": "123456789012",
        "birth_date": "1990-05-12"
    }

    result = validate_applicant_data(applicant_data)

    assert result is True

def test_validate_applicant_data_with_invalid_tax_id():
    applicant_data = {
        "full_name": "Иванов Иван Иванович",
        "passport": "1234567890",
        "tax_id": "1234567890",
        "birth_date": "1990-05-12"
    }

    result = validate_applicant_data(applicant_data)

    assert result is False

def test_extract_domain_facts_from_valid_data():
    applicant_data = {
        "birth_date": "1990-05-12",
        "documents": ["passport", "medical_certificate"]
    }

    external_reports = {
        "criminal_record": False,
        "admin_violations": 1,
        "residency_years": 10
    }

    facts = extract_domain_facts(applicant_data, external_reports)

    assert facts["has_criminal_record"] is False
    assert facts["admin_violations_count"] == 1
    assert facts["residency_years"] == 10
    assert facts["documents_provided"] == ["passport", "medical_certificate"]

    assert facts["age"] >= 30
    assert facts["age"] <= 40
