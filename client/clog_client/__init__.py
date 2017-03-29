import json
import sys

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from tclog import CassandraLogService


class CassandraLogClient(object):
    def __init__(self, hostname='localhost', port=9090, *args, **kwargs):
        self.hostname = hostname
        self.port = port

    def new_transport(self):
        # Make socket
        transport = TSocket.TSocket(self.hostname, self.port)

        # Buffering is critical. Raw sockets are very slow
        transport = TTransport.TFramedTransport(transport)

        # Wrap in a protocol
        protocol = TBinaryProtocol.TBinaryProtocol(transport)

        # Create a client to use the protocol encoder
        client = CassandraLogService.Client(protocol)

        # Connect!
        try:
            transport.open()
        except Exception, e:
            print "Failed to connect"
            print e
            sys.exit()
        return transport, client

    def clog(self, **kwargs):
        transport, client = self.new_transport()
        message = json.dumps(kwargs)
        result = client.clog(message)
        transport.close()
        return result

