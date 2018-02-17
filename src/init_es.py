import os
from elasticsearch import Elasticsearch

MAPPING = {
    "url": {
        "type": "keyword",
        "index": True
    },
    "breed": {
        "type": "keyword",
        "index": True
    },
    "location": {
        "type": "keyword",
        "index": True
    },
    "description": {
        "type": "text"
    },
    "price": {
        "type": "float"
    },
    "title": {
        "type": "text"
    }
}

INDEX_NAME = "dogs"


def create_mapping():
    es = Elasticsearch()

    if es.indices.exists(INDEX_NAME):
        es.indices.delete(INDEX_NAME)
    es.indices.create(index=INDEX_NAME,
                      body={
                          "settings": {
                              "number_of_shards": os.environ.get('ELASTICSEARCH_SHARDS', 1),
                              "number_of_replicas": os.environ.get('ELASTICSEARCH_REPLICAS', 0)
                          },
                          "mappings": {
                              "items": {
                                  "properties": MAPPING
                              }
                          }
                      })

if __name__=="__main__":
    create_mapping()