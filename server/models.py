from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.management import sync_table, drop_table
from cassandra.cqlengine.management import create_keyspace_simple


class BaseModel(Model):
    __abstract__ = True
    @classmethod
    def log(cls, **kwargs):
        obj = cls.create(**kwargs)
        return obj


class SubmissionTraceBySubmission(BaseModel):
    submission_id = columns.Integer(partition_key=True)
    log_timestamp = columns.DateTime(primary_key=True)
    state = columns.Integer(primary_key=True)
    user_id = columns.Integer()
    run_id = columns.Integer()
    context = columns.Map(columns.Text(), columns.Text())


class SubmissionTraceByTimestamp(BaseModel):
    log_timestamp_3 = columns.DateTime(partition_key=True)
    submission_id = columns.Integer(primary_key=True, clustering_order="DESC")
    log_timestamp = columns.DateTime()
    state = columns.Integer(primary_key=True)
    user_id = columns.Integer()
    run_id = columns.Integer()
    context = columns.Map(columns.Text(), columns.Text())

    @staticmethod
    def get_partition_key(datetime_obj):
        dt = datetime_obj.replace(minute=0, second=0, microsecond=0, hour=datetime_obj.hour/3)
        return dt
        
    @classmethod
    def log(cls, **kwargs):
        log_timestamp = kwargs.get('log_timestamp')
        if not log_timestamp:
            raise Exception('Timestamp should be provided.')
        log_timestamp_3 = cls.get_partition_key(log_timestamp)
        obj = cls.create(log_timestamp_3=log_timestamp_3, **kwargs)
        return obj


KEYSPACE = 'tracelog'


def create_keyspace():
    create_keyspace_simple(KEYSPACE, replication_factor=1)


def setup_connection():
    connection.setup(['127.0.0.1'], KEYSPACE, protocol_version=3)


def setup_models():
    setup_connection()
    sync_table(SubmissionTraceBySubmission)
    sync_table(SubmissionTraceByTimestamp)


def drop_models():
    setup_connection()
    drop_table(SubmissionTraceBySubmission)
    drop_table(SubmissionTraceByTimestamp)
