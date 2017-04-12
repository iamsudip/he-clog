import datetime
import json
import sys

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from tclog import CassandraLogService


class TraceLogClient(object):
    hostname = 'tracelog-cassandra.hackerearth.com'
    port = 9000

    @classmethod
    def new_transport(cls):
        # Make socket
        transport = TSocket.TSocket(cls.hostname, cls.port)

        # Buffering is critical. Raw sockets are very slow
        transport = TTransport.TFramedTransport(transport)

        # Wrap in a protocol
        protocol = TBinaryProtocol.TBinaryProtocol(transport)

        # Create a client to use the protocol encoder
        client = CassandraLogService.Client(protocol)

        # Connect!
        try:
            transport.open()
        except Exception as e:
            print e
            sys.exit()
        return transport, client

    @classmethod
    def log(cls, submission_id, user_id, state, run_id=None, context=None):
        transport, client = cls.new_transport()
        if context and not isinstance(context, dict):
            raise Exception("Context should be of <type 'dict<string:string>'")
        log_timestamp = datetime.datetime.now()
        kwargs = {
            'submission_id': submission_id,
            'log_timestamp': log_timestamp.isoformat(),
            'user_id': user_id,
            'state': state,
            'run_id': run_id,
            'context': context,
        }
        message = json.dumps(kwargs)
        result = client.clog(message)
        transport.close()
        return result

