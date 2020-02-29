import pytest
from random import randint


# сделал чисто для интереса, чтоб потрогать
@pytest.fixture()
def random_int():
    return randint(1, 10)
