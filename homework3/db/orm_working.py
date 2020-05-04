from db.models import Log
from db.ormclient import MysqlOrmConnection
from db.ormbuilder import MysqlOrmBuilder
from sqlalchemy import func, desc

connection = MysqlOrmConnection(user='root', password='pass', db_name='HW_ORM')
builder = MysqlOrmBuilder(connection=connection)


def fill_db():
    with open('log.txt', 'r') as f:
        lst_of_logs = f.read().splitlines()
        for log in lst_of_logs:
            builder.add_log(log)
        connection.session.commit()


fill_db()

print("Всего запросов:")
first = connection.session.query(Log.id).count()
print(first)

print("Запросы, сгрупированные по методам:")
second = connection.session.query(Log.request_type, func.count(Log.request_type)).group_by(Log.request_type).all()
print(second)

print("Топ-10 запросов по размеру:")
third = connection.session.query(Log.url, Log.status_code, Log.size).order_by(desc(Log.size)).limit(10).all()
print(*third, sep='\n')

print("Топ-10 самых встречаемых 400-ых запросов сгруппированных по конкретной ошибке и урлу:")
fourth = connection.session.query(Log.url, Log.status_code, func.count()).filter(Log.status_code.like('4%')).group_by(
    Log.status_code, Log.url).order_by(desc(func.count())).all()
print(*fourth, sep='\n')

print("Топ-10 400-ых запросов по размеру:")
fifth = connection.session.query(Log.ip, Log.url, Log.status_code, Log.size).filter(
    Log.status_code.like('4%')).order_by(desc(Log.size)).limit(10).all()
print(*fifth, sep='\n')
