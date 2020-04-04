import json

import pytest
import time
from api.client import Client


class Test:

    @pytest.fixture(scope='function')
    def api_client(self):
        email = 'QAPythonVasilievHW2@yandex.ru'
        password = 'Covid-19'
        return Client(email, password)

    # @pytest.mark.skip
    @pytest.mark.API
    def test_create_segment(self, api_client):
        name_of_segment = 'QAPython' + str(int(time.time()))
        r1 = api_client.post_segment(name_of_segment)
        assert r1.status_code == 200 and r1.json()['name'] == name_of_segment

    # @pytest.mark.skip
    @pytest.mark.API
    def test_delete_segment(self, api_client):
        name_of_segment = 'QAPython' + str(int(time.time()))
        r1 = api_client.post_segment(name_of_segment)
        segment_id = r1.json()['id']
        r2 = api_client.delete_segment(segment_id)
        assert r2.status_code == 204
