import requests
import json
from requests.cookies import cookiejar_from_dict
from api.urls import *


class Client:

    def __init__(self, email, password):
        self.base_url = 'https://target.my.com/'
        self.session = requests.Session()
        self.email = email
        self.password = password
        self.csrftoken = None  # можно и не акцентировать, там не только он нужен
        self.login()

    def _request(self, method, url, headers=None, params=None, data=None, allow_redirects=False):
        response = self.session.request(method, url, headers=headers, params=params, data=data,
                                        allow_redirects=allow_redirects)
        return response

    def login(self):
        # 1 часть
        data = {'email': self.email,
                'password': self.password,
                'continue': CONTINUE_URL,
                'failure': FAILURE_URL}
        headers = {'Referer': self.base_url,
                   'Content-Type': 'application/x-www-form-urlencoded'}  # необязательный
        r = self._request('POST', AUTH_URL,
                          headers=headers,
                          data=data)
        loc = r.headers['location']
        mc = r.cookies['mc']
        ssdc = r.cookies['ssdc']
        mrcu = r.cookies['mrcu']
        self.session.cookies = cookiejar_from_dict({'mc': mc, 'ssdc': ssdc, 'mrcu': mrcu})

        # 2 часть
        r = self._request('GET', loc)
        loc = r.headers['Location']

        # 3 часть
        r = self._request('GET', loc)
        loc = r.headers['Location']
        mc = r.cookies['mc']
        ssdc = r.cookies['ssdc']
        self.session.cookies = cookiejar_from_dict({'mc': mc, 'ssdc': ssdc, 'mrcu': mrcu})

        # 4 часть
        r = self._request('GET', loc)
        sdcs = r.cookies['sdcs']
        self.session.cookies = cookiejar_from_dict({'sdcs': sdcs, 'mc': mc, 'ssdc': ssdc, 'mrcu': mrcu})

        # 5 часть
        r = self._request('GET', CSRF_URL)
        self.csrftoken = r.cookies['csrftoken']
        self.session.cookies = cookiejar_from_dict(
            {'sdcs': sdcs, 'mc': mc, 'ssdc': ssdc, 'mrcu': mrcu, 'csrftoken': self.csrftoken})

    def post_segment(self, name_of_segment):
        data = {
            'name': name_of_segment,
            'pass_condition': 1,
            'relations': [{
                'object_type': "remarketing_player",
                'params': {
                    'type': "positive",
                    'left': 365,
                    'right': 0}}]
        }
        data = json.dumps(data)

        r = self._request('POST',
                          data=data,
                          headers={'Referer': 'https://target.my.com/segments/segments_list/new',
                                   'X-CSRFToken': self.session.cookies['csrftoken']},
                          url=CREATE_SEGMENT_URL)
        return r

    def delete_segment(self, segment_id):
        r = self._request('DELETE',
                          headers={'Referer': 'https://target.my.com/segments/segments_list',
                                   'X-CSRFToken': self.session.cookies['csrftoken']},
                          url=DELETE_SEGMENT_URL.format(segment_id))
        return r
