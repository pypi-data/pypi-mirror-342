import logging
import os
from enum import Enum


class EntityType(Enum):
    PER = "PER"
    ORG = "ORG"
    KEYWORD = "EMS_KEYWORD"
    LOC = "LOC"
    UNK = "UNKNOWN"


class KeywordType(Enum):
    LOC = "Kohamärksõnad"
    TIME = "Ajamärksõnad"
    TOPIC = "Teemamärksõnad"
    GENRE = "Vormimärksõnad"


LOGGER_NAME = "rara-norm-linker"
LOGGER = logging.getLogger(LOGGER_NAME)

ELASTIC_HOST = os.environ.get("ES_URL", "http://localhost:9200")

EMS_CONFIG = {
    "es_host": ELASTIC_HOST,
    "es_index": "rara_linker_ems_partial_v2",
    "search_field": "link_variations",
    "alt_search_field": "synonyms_en",
    "key_field": "keyword",
    "json_field": "full_record_json",
    "marc_field": "full_record_marc",
    "identifier_field": "ems_id"
}

LOC_CONFIG = {
    "es_host": ELASTIC_HOST,
    "es_index": "rara_linker_ems_loc_v3",
    "search_field": "link_variations",
    "alt_search_field": "synonyms_en",
    "key_field": "keyword",
    "json_field": "full_record_json",
    "marc_field": "full_record_marc",
    "identifier_field": "ems_id"
}

PER_CONFIG = {
    "es_host": ELASTIC_HOST,
    "es_index": "rara_linker_persons_knn_v2",
    "search_field": "link_variations",
    "key_field": "name",
    "vector_field": "vector",
    "json_field": "full_record_json",
    "marc_field": "full_record_marc",
    "identifier_field": "identifier",
    "viaf_field": "local.personalNames"
}

ORG_CONFIG = {
    "es_host": ELASTIC_HOST,
    "es_index": "rara_linker_organizations_knn_v2",
    "search_field": "link_variations",
    "alt_search_field": "link_acronyms",
    "key_field": "name",
    "vector_field": "vector",
    "json_field": "full_record_json",
    "marc_field": "full_record_marc",
    "identifier_field": "identifier",
    "viaf_field": "local.corporateNames"
}

VECTORIZER_CONFIG = {
    "model_name": "BAAI/bge-m3",
    "system_configuration": {
        "use_fp16": False,
        "device": None,
        "normalize_embeddings": True
    },
    "inference_configuration": {
        "batch_size": 12,
        "return_dense": True,
        "max_length": 1000
    },
    "model_directory": "../vectorizer_data",
}
