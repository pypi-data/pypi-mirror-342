import requests
import json
from typing import List
from collections import defaultdict

class VIAFPersonRecord:
    def __init__(self, 
            record: dict, 
            allowed_sources: List[str] = ["LC", "DNB", "LNB", "NLL", "ERRR", "J9U"]
        ):
        self.__record: dict = record
        self.__record_data: dict = {}
        self.__allowed_sources: List[str] = allowed_sources
        self.__viaf_id: int = None
        self.__name_variations: List[str] = []
        self.__birth_date: str = None 
        self.__death_date: str = None
        self.__occupations: List[str] = []
        self.__all_fields: dict = {}
        self.__nationality: str = ""
    
    @property
    def viaf_id(self) -> int:
        if not self.__viaf_id:
            self.__viaf_id = self.record_data.get("viafID", "")
        return self.__viaf_id
    
    def __get_data(self, field_name: str) -> List[str]:
        entries = self.record_data.get(field_name, {}).get("data", [])

        data = []
        for entry in entries:
            sources = entry.get("sources", {}).get("s", [])
            if set(self.__allowed_sources).intersection(set(sources)):
                data.append(entry.get("text", ""))
        return data
    
    @property
    def record_data(self) -> dict:
        if not self.__record_data:
            try:
                self.__record_data = self.__record["queryResult"]
            except:
                self.__record_data = self.__record["recordData"]["VIAFCluster"]

        return self.__record_data

    @property
    def name_variations(self) -> List[str]:
        if not self.__name_variations:
            self.__name_variations = self.__get_data("mainHeadings")
        return self.__name_variations
    
    @property
    def birth_date(self) -> str:
        if not self.__birth_date:
            self.__birth_date = self.record_data.get("birthDate", None)
        return self.__birth_date
        
    
    @property 
    def death_date(self) -> str:
        if not self.__death_date:
            self.__death_date = self.record_data.get("deathDate", None)
        return self.__death_date
    
    @property
    def occupations(self) -> List[str]:
        if not self.__occupations:
            self.__occupations = self.__get_data("occupation")
        return self.__occupations
   
    
    @property
    def nationality(self) -> str:
        if not self.__nationality:
            nationalities = self.__get_data("nationalityOfEntity")
            nationalities_dict = defaultdict(int)
            for n in nationalities:
                nationalities_dict[n.lower()]+=1
            if nationalities:
                self.__nationality = sorted(nationalities_dict.items(), key=lambda x: x[1], reverse=True)[0][0]
        return self.__nationality
    
    @property 
    def all_fields(self) -> dict:
        if not self.__all_fields:
            self.__all_fields = {
                "name_variations": self.name_variations,
                "birth_date": self.birth_date,
                "death_date": self.death_date,
                "occupations": self.occupations,
                "nationality": self.nationality
            }
        return self.__all_fields
            
    
class VIAFLinker:
    def __init__(self, viaf_api_url: str = "https://viaf.org/api"):
        self.root_url = viaf_api_url.strip("/")
        self.record_url = f"{self.root_url}/cluster-record"
        self.auto_suggest_url = f"{self.root_url}/auto-suggest"
        self.search_url = f"{self.root_url}/search"
        self.headers = {
            "Accept": "application/json", 
            "Content-Type": "application/json"
        }
        
    def _send_request(self, url: str, data: dict) -> dict:
        response = requests.post(url, data=json.dumps(data), headers=self.headers)
        if response.status_code != 200:
            raise Exception(
                f"Unsuccessful query with payload = '{data}'. " \
                f"VIAF API returned status code '{response.status_code}'."
            )
        return response.json()
        
    def auto_suggest(self, search_term: str) -> dict:
        data = {
            "reqValues":{
                "autoSuggestTerm": search_term
            }
        }
        response = self._send_request(url=self.auto_suggest_url, data=data)
        return response
    
    def get_records_by_search_term(self, 
            search_term: str, 
            index: str = "viaf", 
            field: str = "local.names",
            page_index: int = 0,
            page_size: int = 50          
        ) -> dict:
        data = {
            "reqValues": {
                "field": field,
                "index": index,
                "searchTerms": search_term
            },
            "meta":{
                "env": "prod",
                "pageIndex": page_index,
                "pageSize": page_size
            }
        }
        response = self._send_request(url=self.search_url, data=data)
        return response
    
    def get_records_by_viaf_id(self, record_id: str) -> dict:
        data = {
            "reqValues": {
                "recordId": str(record_id)
            }
        }
        response = self._send_request(url=self.record_url, data=data)
        return response
