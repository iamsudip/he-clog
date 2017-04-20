import datetime
import json
import sys

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from tclog import CassandraLogService


class SubmissionState(object):
    # Submission first time created
    SUBMISSION_CREATED = 10

    # IN evaluate_code, just before async call to compile_code
    PREPARING_MESSAGE_FOR_COMPILING = 20

    # In copile_code, just before caling CompileClient
    QUEUED_FOR_COMPILING = 30

    # IN code checker, just before calling code_checker_server
    IN_COMPILE_CODE_CHECKER = 40

    # Received from code_checker_server, just before queueing to
    # compile_callback_queue
    OUT_COMPILE_CODE_CHECKER = 50

    # Compile worker received the message
    COMPILE_WORKER_RECEIVED = 60

    # Run status bulk created in compile_callback_worker, message also contains
    # run_ids list which got created
    RUN_STATUS_CREATED = 70

    # In run_code, just before calling RunClient
    QUEUED_FOR_RUN = 80

    # After all async call finised, just before leaving compile_callback_worker
    OUT_COMPILE_WORKER = 90

    RUN_WORKER_RECEIVED = 100


class TraceLogClient(object):
    hostname = 'tracelog-submission.hackerearth.com'
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
        transport.open()
        return transport, client

    @classmethod
    def log(cls, submission_id, user_id, state, run_id=None, context=None):
        try:
            transport, client = cls.new_transport()
        except:
            return
        if context and not isinstance(context, dict):
            raise Exception("Context should be of <type 'dict'")
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

