import pytest
from unittest.mock import MagicMock

from app.storage.repository import (
    save_decision_to_db,
    load_eligibility_report,
    ReportNotFoundError
)

def test_save_decision_to_db_success(mocker):
    mock_connection = mocker.patch("app.storage.repository.get_db_connection")
    mock_cursor = MagicMock()

    mock_connection.return_value.cursor.return_value = mock_cursor

    eligibility_report = {
        "application_id": 55,
        "eligible": False,
        "failed_checks": ["criminal_record"],
        "external_reports": {
            "mvd": {"criminal_record": True},
            "fns": {"tax_debt": False}
        }
    }

    result = save_decision_to_db(eligibility_report)

    mock_cursor.execute.assert_called_once()
    mock_connection.return_value.commit.assert_called_once()

    assert result is True

def test_load_eligibility_report_success(mocker):
    mock_connection = mocker.patch("app.storage.repository.get_db_connection")
    mock_cursor = MagicMock()

    stored_report = {
        "application_id": 55,
        "eligible": False,
        "failed_checks": ["criminal_record"],
        "external_reports": {}
    }

    mock_cursor.fetchone.return_value = [stored_report]
    mock_connection.return_value.cursor.return_value = mock_cursor

    result = load_eligibility_report(55)

    assert result == stored_report

def test_load_eligibility_report_not_found(mocker):
    mock_connection = mocker.patch("app.storage.repository.get_db_connection")
    mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = None
    mock_connection.return_value.cursor.return_value = mock_cursor

    with pytest.raises(ReportNotFoundError):
        load_eligibility_report(999)
