__author__ = 'fellipeh'

from datetime import datetime
from elasticsearch import Elasticsearch
from cassandra.cluster import Cluster

es = Elasticsearch()
ca_cluster = Cluster()
ca_session = ca_cluster.connect('demo')

# first get all from ElasticSearch

es.indices.refresh(index="cliente-index")

res_es = es.search(index="cliente-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res_es['hits']['total'])

for hit in res_es['hits']['hits']:
    hit_source = hit["_source"]
    res_ca = ca_session.execute("SELECT * FROM clientes where (id=%s)",
                                (hit["_id"]))[0]
    if res_ca:
        t_es = datetime.strptime(hit_source['timestamp'], "%Y-%m-%dT%H:%M:%S.%f")
        t_ca = res_ca.time

        latest = max((t_es, t_ca))
        if latest == t_es:
            prep_stmt = ca_session.prepare("UPDATE clientes SET (nome=?,time=?) "
                                           "WHERE (id = ?)")
            bound_stmt = prep_stmt.bind([hit_source['nome'], hit_source['timestamp'],
                                         hit['_id']])
            stmt = ca_session.execute(bound_stmt)
    else:
        prep_stmt = ca_session.prepare("INSERT INTO clientes (id, nome, time) "
                                       "VALUES (?, ?, ?)")
        bound_stmt = prep_stmt.bind([hit['_id'], hit_source['nome'],
                                     datetime.now()])
        stmt = ca_session.execute(bound_stmt)

# Now get all from cassandra

ca_clientes = ca_session.execute("SELECT * FROM clientes")
for hit in ca_clientes:
    es.indices.refresh(index="cliente-index")

    doc_search = {
        "query":
            {
                "query_string":
                    {
                        "query": "" + hit.id + "", "fields": ["_id"]
                    }
            }
    }
    res_es = es.search(index="cliente-index", body=doc_search)
    doc = {
        'nome': hit.nome,
        'timestamp': datetime.now()
    }

    res = es.index(index="cliente-index", doc_type='cliente', id=hit.id, body=doc)





