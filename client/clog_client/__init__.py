import datetime
import json
import sys

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from tclog import CassandraLogService


class SubmissionState(object):
    # Submission first time created
    SUBMISSION_CREATED = {
        'value': 10,
        'state_verbose': 'Submission created'
    }

    # IN evaluate_code, just before async call to compile_code
    PREPARING_MESSAGE_FOR_COMPILING = {
        'value': 20,
        'state_verbose': 'Preparing message for compiling'
    }

    # In copile_code, just before caling CompileClient
    QUEUED_FOR_COMPILING = {
        'value': 30,
        'state_verbose': 'Queued for compilation'
    }


    # IN code checker, just before calling code_checker_server
    IN_COMPILE_CODE_CHECKER = {
        'value': 40,
        'state_verbose': 'Code checker worker received'
    }


    # Received from code_checker_server, just before queueing to
    # compile_callback_queue
    OUT_COMPILE_CODE_CHECKER = {
        'value': 50,
        'state_verbose': 'Queueing to callback from code checker'
    }


    # Compile worker received the message
    COMPILE_WORKER_RECEIVED = {
        'value': 60,
        'state_verbose': 'Compile callback worker received'
    }


    # Run status bulk created in compile_callback_worker, message also contains
    # run_ids list which got created
    RUN_STATUS_CREATED = {
        'value': 70,
        'state_verbose': 'Run status objects created'
    }


    # In run_code, just before calling RunClient
    QUEUED_FOR_RUN = {
        'value': 80,
        'state_verbose': 'Queueing for run'
    }


    # After all async call finised, just before leaving compile_callback_worker
    OUT_COMPILE_WORKER = {
        'value': 90,
        'state_verbose': 'Compile worker job finished'
    }


    RUN_WORKER_RECEIVED = {
        'value': 100,
        'state_verbose': 'Run worker received'
    }



class TraceLogClient(object):
    hostname = 'tracelog.hackerearth.com'
    port = 9000

    @classmethod
    def new_transport(cls):
        # Make socket
        socket = TSocket.TSocket(cls.hostname, cls.port)

        socket.setTimeout(5)

        # Buffering is critical. Raw sockets are very slow
        transport = TTransport.TFramedTransport(socket)

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
            raise Exception("Context should be of <type 'dict'>")

        if state and not isinstance(state, dict):
            raise Exception("state should be of <type 'dict'> with 'value', 'state_verbose' as keys")

        state, state_verbose = state['value'], state['state_verbose']

        log_timestamp = datetime.datetime.now()
        kwargs = {
            'submission_id': submission_id,
            'log_timestamp': log_timestamp.isoformat(),
            'user_id': user_id,
            'state': state,
            'state_verbose': state_verbose,
            'run_id': run_id,
            'context': context,
        }
        message = json.dumps(kwargs)
        result = client.clog(message)
        transport.close()
        return result

