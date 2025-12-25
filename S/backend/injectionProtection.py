import pytest
from unittest.mock import MagicMock, patch

from app.processing.validation import validate_applicant_data
from app.external.merge import merge_external_reports
from app.decision.eligibility import build_eligibility_report
from app.storage.repository import save_decision_to_db

"app.storage.repository.get_db_connection"
def test_backend_protection_against_injections(mock_db_conn):
    malicious_applicant_data = {
        "fullName": "Robert'); DROP TABLE users;--",
        "passport": "1234567890",
        "taxId": "123456789012"
    }

    is_valid = validate_applicant_data(malicious_applicant_data)
    assert is_valid is False

    mvd_report = {
        "criminal_record": "false; os.system('rm -rf /')",
        "restrictions": ["<script>alert(1)</script>"]
    }

    fns_report = {
        "tax_id_valid": True,
        "tax_debt": "0; DROP TABLE tax;"
    }

    merged = merge_external_reports(mvd_report, fns_report)

    assert isinstance(merged, dict)
    assert "criminal_record" in merged

    mock_cursor = MagicMock()
    mock_db_conn.return_value.cursor.return_value = mock_cursor

    report = build_eligibility_report(
        applicant_id=55,
        eligible=False,
        failed_checks=["criminal_record; DROP"],
        external_reports=merged
    )

    saved = save_decision_to_db(report)

    assert saved is True
    mock_cursor.execute.assert_called_once()
    mock_db_conn.return_value.commit.assert_called_once()
