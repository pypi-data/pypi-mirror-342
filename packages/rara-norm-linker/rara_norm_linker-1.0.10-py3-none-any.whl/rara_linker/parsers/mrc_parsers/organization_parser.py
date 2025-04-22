from typing import NoReturn
from collections.abc import Iterator
from rara_linker.parsers.mrc_parsers.general_parser import GeneralMARCParser
from rara_linker.parsers.mrc_records.organization_record import OrganizationRecord


class OrganizationsMARCParser(GeneralMARCParser):
    def __init__(self, 
            marc_file_path: str, 
            add_variations: bool = False
        ) -> NoReturn:
        
        super().__init__(
            marc_file_path=marc_file_path, 
            add_variations=add_variations
        )
           
    def record_generator(self) -> Iterator[OrganizationRecord]:
        for record in self.marc_record_generator():
            org_record = OrganizationRecord(
                record=record, 
                add_variations=self.add_variations
            )
            yield org_record