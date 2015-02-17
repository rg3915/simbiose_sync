# simbiose_sync
Sync between Cassandra and ElasticSearch DBs

# How to use
- Install Cassandra and ElasticSearch (this readme not show you how to intall them :) )
- Create a new keyspace, named demo:
```CREATE KEYSPACE demo WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };```
- Create a new table named  "clientes"
```CREATE TABLE clientes (id text, nome text, time timestamp, PRIMARY KEY (ID));```

or use these schema:

```
CREATE KEYSPACE demo WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': '1'
};

USE demo;

CREATE TABLE clientes (
  id text,
  nome text,
  time timestamp,
  PRIMARY KEY ((id))
) WITH
  bloom_filter_fp_chance=0.010000 AND
  caching='KEYS_ONLY' AND
  comment='' AND
  dclocal_read_repair_chance=0.100000 AND
  gc_grace_seconds=864000 AND
  index_interval=128 AND
  read_repair_chance=0.000000 AND
  replicate_on_write='true' AND
  populate_io_cache_on_flush='false' AND
  default_time_to_live=0 AND
  speculative_retry='99.0PERCENTILE' AND
  memtable_flush_period_in_ms=0 AND
  compaction={'class': 'SizeTieredCompactionStrategy'} AND
  compression={'sstable_compression': 'LZ4Compressor'};

```

After that, create new docs into Cassandra or ElasticSearch, if you want, you can use these script: ```create_docs_cas``` for Cassandra Database and ```create_docs_es``` for ElasticSearch.

Run ```python daemon.py ``` to start sync..

**You need to create a job on Cron to repeat these script any time you want.** 

Any question or any changes on this file, feel free to submit a pull request!
