import pytest

from app.decision.eligibility import (
    check_eligibility,
    aggregate_failed_checks,
    build_eligibility_report
)

def test_eligibility_positive_decision():
    applicant_facts = {
        "age": 30,
        "has_criminal_record": False,
        "admin_violations_count": 0,
        "residency_years": 8,
        "medical_clear": True,
        "documents_complete": True
    }

    result = check_eligibility(applicant_facts)

    assert result["eligible"] is True
    assert result["failed_checks"] == []

def test_eligibility_negative_decision_with_multiple_reasons():
    applicant_facts = {
        "age": 22,
        "has_criminal_record": True,
        "admin_violations_count": 3,
        "residency_years": 1,
        "medical_clear": True,
        "documents_complete": False
    }

    result = check_eligibility(applicant_facts)

    assert result["eligible"] is False

    assert set(result["failed_checks"]) == {
        "criminal_record",
        "residency_duration",
        "required_documents"
    }

def test_aggregate_failed_checks_returns_only_failed_items():
    check_results = {
        "criminal_record": False,
        "residency_duration": True,
        "medical_status": False,
        "documents": True
    }

    result = aggregate_failed_checks(check_results)

    assert result == ["residency_duration"]

def test_build_eligibility_report_creates_valid_structure():
    applicant_id = 55
    eligible = False
    failed_checks = ["criminal_record"]

    external_reports = {
        "mvd": {"criminal_record": True},
        "fns": {"tax_debt": False}
    }

    report = build_eligibility_report(
        applicant_id=applicant_id,
        eligible=eligible,
        failed_checks=failed_checks,
        external_reports=external_reports
    )

    assert report["application_id"] == 55
    assert report["eligible"] is False
    assert report["failed_checks"] == ["criminal_record"]
    assert report["external_reports"] == external_reports