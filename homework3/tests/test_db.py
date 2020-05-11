import pytest

from db.models import Log
from db.ormbuilder import MysqlOrmBuilder


class TestOrmMysql:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_orm_client):
        self.connection = mysql_orm_client
        self.builder = MysqlOrmBuilder(mysql_orm_client)

    def test(self):
        for _ in range(25):
            self.builder.add_log(
                '93.180.71.3 - - [17/May/2015:08:05:32 +0000] "GET /downloads/product_1 HTTP/1.1" 403 0 "-" "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)"')
        self.connection.session.commit()
        assert len(self.connection.session.query(Log).all()) == 25
