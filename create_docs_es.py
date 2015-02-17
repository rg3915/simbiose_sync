__author__ = 'fellipeh'

from datetime import datetime
from elasticsearch import Elasticsearch

###
# Generating ElasticSearch Docs

es = Elasticsearch()

while True:
    ID = raw_input('Please type ID field: ')
    NAME = raw_input('Please type Name field: ')

    doc = {
        'nome': NAME,
        'timestamp': datetime.now()
    }

    res = es.index(index="cliente-index", doc_type='cliente', id=ID, body=doc)
    print(res['created'])

    resp = raw_input('New Doc? [y/n]: ')
    if resp not in 'y':
        break
