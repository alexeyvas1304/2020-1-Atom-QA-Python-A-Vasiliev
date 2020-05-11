import socket
from user_data import SOCKET_HOST, SOCKET_PORT


class SocketClient:
    def __init__(self, target_host, target_port):
        self.target_host = target_host
        self.target_port = target_port
        self.client = None

    def connect_to_server(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.client.connect((self.target_host, self.target_port))
                break
            except ConnectionRefusedError:
                pass

    def get_request(self, url):
        request = f'GET {url} HTTP/1.1\r\nHost:{self.target_host}\r\n\r\n'
        self.client.send(request.encode())

    def post_request(self, url, data):
        data_string = f'name={data["name"]}&surname={data["surname"]}'
        request = f'POST {url} HTTP/1.1\r\nHost: {self.target_host}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {len(data_string)}\r\n\r\n{data_string}'
        self.client.send(request.encode())

    def receive_data(self):
        total_data = []

        while True:
            data = self.client.recv(16384)
            if data:
                total_data.append(data.decode())
            else:
                break
        data = ''.join(total_data).splitlines()

        status_code = data[0].split()[1]

        if status_code == '200':
            res_json = {'Status_code': int(status_code), 'Headers': data[1:-2], 'Body': data[-1]}
        else:
            res_json = {'Status_code': int(status_code), 'Headers': data[1:-5]}

        return res_json


if __name__ == '__main__':  # при запущенном сервере
    client = SocketClient(SOCKET_HOST, SOCKET_PORT)

    client.connect_to_server()  # хорошо бы сделать keepalive соединение
    client.post_request('/users', {'name': 'Simon', 'surname': 'Galushkin'})
    print(client.receive_data())
    client.client.close()

    client.connect_to_server()
    client.get_request('/users/0')
    print(client.receive_data())
    client.client.close()

    client.connect_to_server()
    client.get_request('/users/1')
    print(client.receive_data())
    client.client.close()
