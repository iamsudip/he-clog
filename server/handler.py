import dateutil.parser
import json

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

from constants import DEV, DEBUG
from models import setup_connection
from models import SubmissionTraceBySubmission, SubmissionTraceByTimestamp

try:
    from machine_settings import *
except ImportError:
    pass


class CassandraLogServiceHandler(object):
    def __init__(self, *args, **kwargs):
        setup_connection()

    def clog(self, message):
        if DEBUG: print "Received Message: ", message
        payload = json.loads(message)
        log_timestamp = dateutil.parser.parse(payload['log_timestamp'])
        payload['log_timestamp'] = log_timestamp
        SubmissionTraceBySubmission.log(**payload)
        SubmissionTraceByTimestamp.log(**payload)

