import requests
import json
from urllib.parse import urljoin


class Client:

    def __init__(self, username, password, email, logger_api):
        self.base_url = 'http://0.0.0.0:7000'
        self.logger = logger_api
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.email = email
        self.login()

    def _request(self, method, location, headers=None, params=None, data=None, allow_redirects=False):
        url = urljoin(self.base_url, location)

        self.logger.info('Performing request:')
        self.logger.info(f'URL: {url}')
        self.logger.info(f'PARAMS: {params}')
        self.logger.info(f'BODY: {data}')
        self.logger.info('-' * 20 + '\n')

        response = self.session.request(method, url, headers=headers, params=params, data=data,
                                        allow_redirects=allow_redirects)

        self.logger.info('Got response:')
        self.logger.info(f'Status code: {response.status_code}')
        self.logger.info(f'Content: {response.text}')
        self.logger.info('-' * 60 + '\n')

        return response

    def login(self):
        data = {'username': self.username,
                'password': self.password,
                'submit': 'Login'}
        headers = {'Referer': self.base_url,
                   'Content-Type': 'application/x-www-form-urlencoded'}

        r = self._request('POST', 'login',
                          headers=headers,
                          data=data)

    def add_user(self, username, password, email):
        data = {
            'username': username,
            'password': password,
            'email': email
        }
        data = json.dumps(data)

        r = self._request('POST', 'api/add_user', data=data)
        return r

    def delete_user(self, username):
        r = self._request('GET', f'api/del_user/{username}')
        return r

    def block_user(self, username):
        r = self._request('GET', f'api/block_user/{username}')
        return r

    def accept_user(self, username):
        r = self._request('GET', f'api/accept_user/{username}')
        return r
