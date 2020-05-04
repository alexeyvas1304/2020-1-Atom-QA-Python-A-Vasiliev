from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Log(Base):
    __tablename__ = 'logs'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(30), nullable=False)
    date = Column(String(30), nullable=False)
    request_type = Column(String(10), nullable=False)
    url = Column(String(50), nullable=False)
    status_code = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Log(" \
               f"id='{self.id}'," \
               f"ip='{self.ip}', " \
               f"date='{self.date}', " \
               f"request_type='{self.request_type}'" \
               f"url='{self.url}'" \
               f"status_code='{self.status_code}'" \
               f"size='{self.size}'" \
               f")>"
