from db.models import User


class MysqlOrmWorker:

    def __init__(self, connection):
        self.connection = connection
        self.engine = connection.connection.engine

    def find_count_by_name(self, name):
        return self.connection.session.query(User.username).filter(User.username == name).count()

    def find_count_by_email(self, email):
        return self.connection.session.query(User.email).filter(User.email == email).count()

    def get_access_status_by_name(self, name):
        return self.connection.session.query(User.username, User.access).filter(
            User.username == name).one().access

    def get_active_status_by_name(self, name):
        return self.connection.session.query(User.username, User.active).filter(
            User.username == name).one().active
