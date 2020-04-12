import requests
import json
from api.urls import *


class Client:

    def __init__(self, email, password):
        self.base_url = 'https://target.my.com/'
        self.session = requests.Session()
        self.email = email
        self.password = password
        self.csrftoken = None
        self.login()

    def _request(self, method, url, headers=None, params=None, data=None, allow_redirects=False):
        response = self.session.request(method, url, headers=headers, params=params, data=data,
                                        allow_redirects=allow_redirects)
        return response

    def login(self):
        data = {'email': self.email,
                'password': self.password,
                'continue': CONTINUE_URL,
                'failure': FAILURE_URL}
        headers = {'Referer': self.base_url,
                   'Content-Type': 'application/x-www-form-urlencoded'}
        r = self._request('POST', AUTH_URL,
                          headers=headers,
                          data=data)
        for i in range(3):
            loc = r.headers['location']
            r = self._request('GET', loc)

        r = self._request('GET', CSRF_URL)
        self.csrftoken = r.cookies['csrftoken']

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
                                   'X-CSRFToken': self.csrftoken},
                          url=CREATE_SEGMENT_URL)
        return r

    def delete_segment(self, segment_id):
        r = self._request('DELETE',
                          headers={'Referer': 'https://target.my.com/segments/segments_list',
                                   'X-CSRFToken': self.csrftoken},
                          url=DELETE_SEGMENT_URL.format(segment_id))
        return r
