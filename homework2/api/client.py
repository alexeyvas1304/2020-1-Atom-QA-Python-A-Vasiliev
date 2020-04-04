import requests
import json
from requests.cookies import cookiejar_from_dict
import time


class Client:

    def __init__(self, email, password):
        self.base_url = 'https://target.my.com'
        self.session = requests.Session()
        self.email = email
        self.password = password
        self.login()

    def _request(self, method, url, headers=None, params=None, data=None, allow_redirects=False):
        response = self.session.request(method, url, headers=headers, params=params, data=data,
                                        allow_redirects=allow_redirects)
        return response

    def login(self):
        # 1 часть
        data = {'email': self.email,
                'password': self.password,
                'continue': 'https://target.my.com/auth/mycom?state=target_login%3D1#email',
                'failure': 'https://account.my.com/login/'}
        headers = {'Referer': 'https://target.my.com/'}
        r = self._request('POST', 'https://auth-ac.my.com/auth?lang=ru&nosavelogin=0',
                          headers=headers,
                          data=data,
                          allow_redirects=False)
        loc = r.headers['location']
        mc = r.cookies['mc']
        ssdc = r.cookies['ssdc']
        mrcu = r.cookies['mrcu']
        self.session.cookies = cookiejar_from_dict({'mc': mc, 'ssdc': ssdc, 'mrcu': mrcu})
        # 2 часть
        r = self._request('GET', loc, allow_redirects=False)
        loc = r.headers['Location']
        # 3 часть
        r = self._request('GET', loc, allow_redirects=False)
        loc = r.headers['Location']
        mc = r.cookies['mc']
        ssdc = r.cookies['ssdc']
        self.session.cookies = cookiejar_from_dict({'mc': mc, 'ssdc': ssdc, 'mrcu': mrcu})
        # 4 часть
        r = self._request('GET', loc, allow_redirects=False)
        sdcs = r.cookies['sdcs']
        self.session.cookies = cookiejar_from_dict({'sdcs': sdcs, 'mc': mc, 'ssdc': ssdc, 'mrcu': mrcu})
        # 5 часть
        r = self._request('GET', 'https://target.my.com/csrf/')
        csrftoken = r.cookies['csrftoken']
        self.session.cookies = cookiejar_from_dict(
            {'sdcs': sdcs, 'mc': mc, 'ssdc': ssdc, 'mrcu': mrcu, 'csrftoken': csrftoken})

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
                          url='https://target.my.com/api/v2/remarketing/segments.json?fields=relations__object_type,relations__object_id,relations__params,relations_count,id,name,pass_condition,created,campaign_ids,users,flags')
        return r

    def delete_segment(self, segment_id):
        r = self._request('DELETE',
                          headers={'Referer': 'https://target.my.com/segments/segments_list',
                                   'X-CSRFToken': self.session.cookies['csrftoken']},
                          url=f'https://target.my.com/api/v2/remarketing/segments/{segment_id}.json')
        return r

