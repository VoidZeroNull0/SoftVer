import pytest
from unittest.mock import patch, MagicMock

from app.external.mvd import verify_data_from_mvd
from app.external.fns import verify_data_from_fns
from app.external.merge import merge_external_reports
from app.processing.extract import extract_domain_facts
from app.decision.eligibility import check_eligibility, build_eligibility_report
from app.storage.repository import save_decision_to_db

"app.external.mvd.verify_data_from_mvd"
"app.external.fns.verify_data_from_fns"
"app.storage.repository.get_db_connection"
def test_full_pipeline_success(
    mock_db_conn,
    mock_verify_fns,
    mock_verify_mvd
):
    mock_verify_mvd.return_value = {
        "is_valid": True,
        "criminal_record": False,
        "restrictions": []
    }

    mock_verify_fns.return_value = {
        "tax_id_valid": True,
        "tax_debt": False
    }

    mock_cursor = MagicMock()
    mock_db_conn.return_value.cursor.return_value = mock_cursor

    applicant_data = {
        "birth_date": "1990-05-12",
        "documents": ["passport", "medical_certificate"]
    }

    passport = "1234567890"
    tax_id = "123456789012"

    mvd_report = verify_data_from_mvd(passport)
    fns_report = verify_data_from_fns(tax_id)

    external_reports = merge_external_reports(mvd_report, fns_report)

    facts = extract_domain_facts(applicant_data, external_reports)

    decision = check_eligibility(facts)

    report = build_eligibility_report(
        applicant_id=55,
        eligible=decision["eligible"],
        failed_checks=decision["failed_checks"],
        external_reports={
            "mvd": mvd_report,
            "fns": fns_report
        }
    )

    saved = save_decision_to_db(report)

    assert report["application_id"] == 55
    assert "eligible" in report
    assert "failed_checks" in report
    assert saved is True

    mock_cursor.execute.assert_called_once()
    mock_db_conn.return_value.commit.assert_called_once()