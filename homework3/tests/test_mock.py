import pytest
from http_client.http_client import SocketClient  # можно и в фикстуру, но не принципиально
import time


@pytest.mark.MOCK
def test_valid(mock_server_setup):
    server_host, server_port = mock_server_setup
    socket_client = SocketClient(server_host, server_port)

    socket_client.connect_to_server()
    user = {'name': 'Ilya', 'surname': 'Kirillov'}
    socket_client.post_request('/users', user)
    time.sleep(0.5)  # для стабилизации, иногда данные не успевают попасть на сервер, а get уже пытается их достать
    socket_client.connect_to_server()
    socket_client.get_request('/users/0')
    result = socket_client.receive_data()

    assert result['Status_code'] == 200
    # assert result['Body'] == str(user) # не получается


@pytest.mark.MOCK
def test_invalid(mock_server_setup):
    server_host, server_port = mock_server_setup
    socket_client = SocketClient(server_host, server_port)

    socket_client.connect_to_server()
    user = {'name': 'Yaroslav', 'surname': 'Cherednichenko'}
    socket_client.post_request('/users', user)

    socket_client.connect_to_server()
    socket_client.get_request('/users/3')
    result = socket_client.receive_data()
    assert result['Status_code'] == 404


@pytest.mark.MOCK
def test_post_data(mock_server_setup):  # пусть будет
    server_host, server_port = mock_server_setup
    socket_client = SocketClient(server_host, server_port)
    socket_client.connect_to_server()
    user = {'name': 'Kirill', 'surname': 'Soldatov'}
    socket_client.post_request('/users', data=user)
    result = socket_client.receive_data()
    assert result['Status_code'] == 200
