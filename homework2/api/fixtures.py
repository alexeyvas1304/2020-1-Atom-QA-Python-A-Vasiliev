import pytest
from api.client import Client
from personal_data import EMAIL, PASSWORD


@pytest.fixture(scope='function')
def api_client():
    email = EMAIL
    password = PASSWORD
    return Client(email, password)
