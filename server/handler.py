import json

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

from constants import DEV
try:
    from machine_settings import DEV
except ImportError:
    pass


class CassandraLogServiceHandler(object):
    def __init__(self, *args, **kwargs):
        self._cluster = Cluster()

    def get_session(self):
        return self._cluster.connect()

    def terminate_session(self):
        self._cluster.shutdown()

    def clog(self, message):
        if DEV: print "Received Message: ", message
        kwrags = json.loads(message)
        session = self.get_session()
        # Insert logic to insert into cassandra

        self.terminate_session()

