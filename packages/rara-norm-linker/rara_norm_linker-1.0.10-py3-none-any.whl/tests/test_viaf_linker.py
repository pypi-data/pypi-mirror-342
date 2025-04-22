import pytest
from rara_linker.linkers.viaf_linker import VIAFLinker, VIAFPersonRecord

TEST_PERSON_RECORD_ID = "7432247"
VIAF_ALLOWED_SOURCES = ["LC", "DNB", "LNB", "NLL", "ERRR", "J9U"]

def test_viaf_get_records_by_viaf_id_query():
    linker = VIAFLinker()
    record = linker.get_records_by_viaf_id(TEST_PERSON_RECORD_ID)
    viaf_record = VIAFPersonRecord(record, allowed_sources=VIAF_ALLOWED_SOURCES)
    assert viaf_record.all_fields
    assert "name_variations" in viaf_record.all_fields
    assert len(viaf_record.all_fields["name_variations"]) > 0
