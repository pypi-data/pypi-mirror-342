from abc import abstractmethod

from rara_linker.config import LOGGER
from rara_linker.kata_config import Config
from rara_linker.linkers.es_linker import ElasticLinker
from rara_linker.linkers.linking_result import LinkingResult
from rara_linker.linkers.viaf_linker import VIAFLinker

logger = LOGGER

DEFAULT_LINKING_CONFIG = {
    "fuzziness": 2,
    "prefix_length": 1,
    "min_similarity": 0.9
}


class BaseLinker:
    def __init__(self, config: Config, **kwargs):
        self.config = config
        self.es_linker = ElasticLinker(config, **kwargs)
        self.viaf_linker = VIAFLinker()
        self.json_field = self.config.json_field
        self.marc_field = self.config.marc_field
        self.id_field = self.config.identifier_field
        self.viaf_field = self.config.viaf_field

    @abstractmethod
    def entity_type(self) -> str:
        pass

    @abstractmethod
    def link(self) -> LinkingResult:
        pass

    def link_entity(self, entity: str, **kwargs) -> LinkingResult:
        es_linker_config = {
            "entity": entity,
            "fuzziness": kwargs.get(
                "fuzziness",
                DEFAULT_LINKING_CONFIG["fuzziness"]
            ),
            "prefix_length": kwargs.get(
                "prefix_length",
                DEFAULT_LINKING_CONFIG["prefix_length"]
            ),
            "min_similarity": kwargs.get(
                "min_similarity",
                DEFAULT_LINKING_CONFIG["min_similarity"]
            ),
            "context": kwargs.get("context", None)
        }

        linked = self.es_linker.link(**es_linker_config)
        add_viaf_info = kwargs.get("add_viaf_info", False)

        if add_viaf_info and self.viaf_field:
            for doc in linked:
                identifier = doc.get(self.id_field, "")
                if identifier:
                    viaf_info = self.viaf_linker.get_records_by_search_term(
                        search_term=identifier,
                        field=self.viaf_field
                    )
                    doc["viaf"] = viaf_info

        linking_config = es_linker_config
        linking_config.update({"add_viaf_info": add_viaf_info})

        result = LinkingResult(
            entity=entity,
            entity_type=self.entity_type,
            linked_docs=linked,
            config=self.config,
            linking_config=linking_config
        )
        return result
