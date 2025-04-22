from typing import List, NoReturn
from pymarc.record import Record
from pymarc import MARCReader
from abc import abstractmethod
from collections.abc import Iterator, Iterable
import jsonlines


class GeneralMARCParser:
    def __init__(self, 
            marc_file_path: str, 
            add_variations: bool = False, 
            fields_to_vectorize: List[str] = []
    ) -> NoReturn:
        self.add_variations = add_variations
        self.marc_file_path = marc_file_path
        self.fields_to_vectorize = fields_to_vectorize
        
        
    def _write_line(self, line: dict, file_path: str) -> NoReturn:
        with jsonlines.open(file_path, "a") as f:
            f.write(line)
                 
    def marc_record_generator(self) -> Iterator[Record]:
        with open(self.marc_file_path, "rb") as fh:
            reader = MARCReader(fh)
            for record in reader:
                if record:
                    yield record

    @abstractmethod  
    def record_generator(self) -> Iterator:
        pass
    
    def save_as_jl(self, jl_file_path: str) -> NoReturn:
        for record in self.record_generator():
            self._write_line(record.full_record, jl_file_path)