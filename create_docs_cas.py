__author__ = 'fellipeh'
from datetime import datetime
from cassandra.cluster import Cluster

###
# Generating Cassandra Docs
#
# NOTE: Steps:
# - Create a new keyspace, named demo:
# CREATE KEYSPACE demo WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
# - Create a new table named  "clientes"
#  CREATE TABLE clientes (id text, nome text, time timestamp, PRIMARY KEY (ID));
#
# or use:
# CREATE KEYSPACE demo WITH replication = {
#   'class': 'SimpleStrategy',
#   'replication_factor': '1'
# };
#
# USE demo;
#
# CREATE TABLE clientes (
#   id text,
#   nome text,
#   time timestamp,
#   PRIMARY KEY ((id))
# ) WITH
#   bloom_filter_fp_chance=0.010000 AND
#   caching='KEYS_ONLY' AND
#   comment='' AND
#   dclocal_read_repair_chance=0.100000 AND
#   gc_grace_seconds=864000 AND
#   index_interval=128 AND
#   read_repair_chance=0.000000 AND
#   replicate_on_write='true' AND
#   populate_io_cache_on_flush='false' AND
#   default_time_to_live=0 AND
#   speculative_retry='99.0PERCENTILE' AND
#   memtable_flush_period_in_ms=0 AND
#   compaction={'class': 'SizeTieredCompactionStrategy'} AND
#   compression={'sstable_compression': 'LZ4Compressor'};
####

cluster = Cluster()
session = cluster.connect('demo')

while True:
    ID = raw_input('Please type ID field: ')
    NAME = raw_input('Please type Name field: ')

    session.execute("""
        INSERT INTO clientes (id, nome, time)
        VALUES (%s,%s, %s)
    """, (ID, NAME, datetime.now())
    )
    resp = raw_input('New Doc? [y/n]: ')
    if resp not in 'y':
        break


