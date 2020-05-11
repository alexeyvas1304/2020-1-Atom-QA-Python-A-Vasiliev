from db.models import Base, Log
from db.ormclient import MysqlOrmConnection


class MysqlOrmBuilder:

    def __init__(self, connection: MysqlOrmConnection):
        self.connection = connection
        self.engine = connection.connection.engine
        self.create_logs()

    def create_logs(self):
        if not self.engine.dialect.has_table(self.engine, 'logs'):
            Base.metadata.tables['logs'].create(self.engine)

    def add_log(self, record):
        record_list = record.split()
        log = Log(
            ip=record_list[0],
            date=record_list[3][1:],
            request_type=record_list[5][1:],
            url=record_list[6],
            status_code=record_list[8],
            size=int(record_list[9])
        )

        self.connection.session.add(log)

        return log
