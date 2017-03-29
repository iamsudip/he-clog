from thrift.protocol import TBinaryProtocol
from thrift.server import TServer, TNonblockingServer
from thrift.transport import TSocket
from thrift.transport import TTransport

from tclog import CassandraLogService
from handler import CassandraLogServiceHandler


def start_clog_service():
    handler = CassandraLogServiceHandler()
    processor = CassandraLogService.Processor(handler)
    transport = TSocket.TServerSocket(port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    tfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TNonblockingServer.TNonblockingServer(
        processor, transport, threads=20)
    print "Cassandra Log Server Running..."
    server.serve()


if __name__ == '__main__':
    try:
        start_clog_service()
    except KeyboardInterrupt:
        print "Server interrupted."

