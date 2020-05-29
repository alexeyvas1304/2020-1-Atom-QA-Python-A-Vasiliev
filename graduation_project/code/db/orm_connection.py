import sqlalchemy
from sqlalchemy.orm import sessionmaker
from db.models import User


class MysqlOrmConnection:

    def __init__(self, user, password, db_name):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = '*'
        self.port = 3306

        self.connection = self.connect()

        session = sessionmaker(bind=self.connection.engine,
                               autocommit=True,
                               autoflush=True,
                               enable_baked_queries=False,
                               expire_on_commit=True)
        self.session = session()

    def connect(self):
        engine = sqlalchemy.create_engine(
            'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'.format(user=self.user,
                                                                          password=self.password,
                                                                          host=self.host,
                                                                          port=self.port,
                                                                          db=self.db_name),
            encoding='utf8'
        )

        return engine.connect()

    def execute_query(self, query):
        res = self.connection.execute(query)  # не используется, но пусть будет

    def find_count_by_name(self, name):
        return self.session.query(User.username).filter(User.username == name).count()
