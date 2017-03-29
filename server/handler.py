import json

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

from constants import DEV, DEBUG
try:
    from machine_settings import *
except ImportError:
    pass


class CassandraLogServiceHandler(object):
    def __init__(self, *args, **kwargs):
        self._cluster = Cluster()
        self._keyspace = 'testks' if DEV else 'submissions'

    def get_session(self):
        return self._cluster.connect()

    def terminate_session(self):
        self._cluster.shutdown()

    def clog(self, message):
        if DEBUG: print "Received Message: ", message
        kwrags = json.loads(message)
        session = self.get_session()
        # Insert logic to insert into cassandra

        self.terminate_session()

