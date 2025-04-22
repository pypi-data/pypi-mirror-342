import pytest
import os

from rara_linker.parsers.mrc_parsers.ems_parser import EMSMARCParser
from rara_linker.parsers.mrc_parsers.person_parser import PersonsMARCParser
from rara_linker.parsers.mrc_parsers.organization_parser import OrganizationsMARCParser

MARC_ROOT_DIR = os.path.join("tests", "test_data", "marc_records")
EMS_TEST_FILE = os.path.join(MARC_ROOT_DIR, "ems_test_subset.mrc")
PER_TEST_FILE = os.path.join(MARC_ROOT_DIR, "per_test_subset.mrc")
ORG_TEST_FILE = os.path.join(MARC_ROOT_DIR, "org_test_subset.mrc")

def test_ems_parser_without_variations():
    ems_marc_parser = EMSMARCParser(EMS_TEST_FILE, add_variations=False)
    for record in ems_marc_parser.record_generator():
        assert "keyword" in record.full_record
        assert "link_variations" not in record.full_record

def test_ems_parser_with_variations():
    ems_marc_parser = EMSMARCParser(EMS_TEST_FILE, add_variations=True)
    for record in ems_marc_parser.record_generator():
        assert "keyword" in record.full_record
        assert "link_variations" in record.full_record
        
def test_persons_parser_without_variations():
    per_marc_parser = PersonsMARCParser(PER_TEST_FILE, add_variations=False)
    for record in per_marc_parser.record_generator():
        assert "name" in record.full_record
        assert "link_variations" not in record.full_record


def test_organizations_parser_without_variations():
    org_marc_parser = OrganizationsMARCParser(ORG_TEST_FILE, add_variations=False)
    for record in org_marc_parser.record_generator():
        assert "name" in record.full_record
        assert "link_variations" not in record.full_record