import pytest

from app.external.merge import merge_external_reports
from app.processing.extract import extract_domain_facts

def test_conflicting_external_sources():
    mvd_report = {
        "criminal_record": True,
        "restrictions": ["weapon_ban"]
    }

    fns_report = {
        "tax_id_valid": True,
        "tax_debt": False
    }

    applicant_data = {
        "birth_date": "1995-01-01",
        "documents": ["passport"]
    }

    merged = merge_external_reports(mvd_report, fns_report)
    facts = extract_domain_facts(applicant_data, merged)

    assert facts["has_criminal_record"] is True
    assert "criminal_record" in facts
