from typing import NoReturn, List
from collections.abc import Iterator
from rara_linker.parsers.mrc_parsers.general_parser import GeneralMARCParser
from rara_linker.parsers.mrc_records.person_record import PersonRecord


class PersonsMARCParser(GeneralMARCParser):
    def __init__(self, 
            marc_file_path: str, 
            add_variations: bool = False
        ) -> NoReturn:
        
        super().__init__(
            marc_file_path=marc_file_path, 
            add_variations=add_variations
        )
           
    def record_generator(self) -> Iterator[PersonRecord]:
        for record in self.marc_record_generator():
            person_record = PersonRecord(
                record=record, 
                add_variations=self.add_variations
            )
            yield person_record
            
            
         