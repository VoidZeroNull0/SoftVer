import pytest

from services.mvd import verify_data_from_mvd
from services.errors import ExternalAPIError
from services.merge import merge_external_reports

def test_verify_data_from_mvd_success(mocker):
    """UT-8: успешный ответ МВД"""

    mock_response = {
        "is_valid": True,
        "criminal_record": False,
        "restrictions": []
    }

    mocker.patch(
        "services.mvd.call_mvd_api",
        return_value=mock_response
    )

    result = verify_data_from_mvd("1234567890")

    assert result["is_valid"] is True
    assert result["criminal_record"] is False
    assert result["restrictions"] == []

def test_verify_data_from_mvd_api_error(mocker):
    """UT-9: ошибка внешнего сервиса МВД"""

    mocker.patch(
        "services.mvd.call_mvd_api",
        side_effect=ExternalAPIError(
            source="MVD",
            message="internal_server_error"
        )
    )

    with pytest.raises(ExternalAPIError) as exc:
        verify_data_from_mvd("9999999999")

    assert exc.value.source == "MVD"


def test_merge_external_reports_success():
    """UT-10: корректное объединение отчётов МВД и ФНС"""

    mvd_report = {
        "is_valid": True,
        "criminal_record": False,
        "restrictions": []
    }

    fns_report = {
        "tax_id_valid": True,
        "tax_debt": False
    }

    result = merge_external_reports(mvd_report, fns_report)

    assert result == {
        "passport_valid": True,
        "criminal_record": False,
        "mvd_restrictions": [],
        "tax_id_valid": True,
        "tax_debt": False
    }
