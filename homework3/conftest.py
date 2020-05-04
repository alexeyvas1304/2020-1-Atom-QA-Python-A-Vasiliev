import pytest
from mock import mock_server
from db.ormclient import MysqlOrmConnection
import requests
from sshclient.sshclient import SSH
from user_data import *


@pytest.fixture(scope='session')
def mock_server_setup():
    server = mock_server.run_mock()

    server_host = server._kwargs['host']
    server_port = server._kwargs['port']

    yield server_host, server_port

    shutdown_url = f"http://{server_host}:{server_port}/shutdown"

    requests.get(shutdown_url)


@pytest.fixture(scope='session')
def mysql_orm_client():
    return MysqlOrmConnection('root', 'pass', 'TEST_PYTHON_ORM')


@pytest.fixture(scope='session')
def ssh_client():
    with SSH(hostname=CENTOS_HOSTNAME, username=USERNAME, password=PASSWORD,
             port=NON_DEFAULT_SSH_PORT) as client:
        yield client
