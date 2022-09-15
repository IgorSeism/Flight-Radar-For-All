"""
TODO: add login cookies (trackers, etc.)
TODO: check login response for success
"""
import json
import re
from time import sleep

import requests

import ipv4
from flight import Flight

ipv4.patch()

COMMON_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) '
        'Gecko/20100101 Firefox/95.0'
    ),

    'Referer': 'https://www.flightradar24.com/',

    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',

    'Origin': 'https://www.flightradar24.com',
    'Connection': 'keep-alive',
    'DNT': '1',

    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin'
}


class Client:
    WEB_BASE_URL = 'https://www.flightradar24.com'
    API_BASE_URL = 'https://api.flightradar24.com/common/v1/'

    # login
    LOGIN_URL = WEB_BASE_URL + '/user/login'
    LOGIN_HEADERS = {
        **COMMON_HEADERS,

        'Alt-Used': 'www.flightradar24.com',
        'TE': 'trailers'
    }

    # logout
    LOGOUT_URL = WEB_BASE_URL + '/user/logout'
    LOGOUT_HEADERS = {
        **COMMON_HEADERS
    }

    def __init__(self, email, password):
        self.email = email
        self.password = password

        self.logged_in = False
        self.session = requests.Session()
        self.token = None

        self.next_query = None

    def login(self):
        response = self.session.post(
            Client.LOGIN_URL,
            headers=Client.LOGIN_HEADERS,
            files={
                'email': (None, self.email),
                'password': (None, self.password),
                'remember': (None, 'true'),
                'type': (None, 'web')
            }
        )

        response_data = response.json()
        self.token = response_data['userData']['subscriptionKey']

        self.logged_in = True

    def logout(self):
        # make a request to the main page to obtain `sessionToken`
        response = \
            self.session.get(Client.WEB_BASE_URL, headers=COMMON_HEADERS)
        session_token = re.findall(r'"sessionToken": "(.*)",', response.text)

        response = self.session.post(
            Client.LOGOUT_URL,
            headers=Client.LOGOUT_HEADERS,
            data=json.dumps({
                'SignOut': True,
                'sessionToken': session_token
            })
        )

        self.logged_in = False

    def _set_next_query(self, response_data):

        if response_data['result']['response'].get('data') is None:
            self.next_query = None

            return

        if not response_data['result']['response']['page']['more']:
            print(3)
            self.next_query = None

            return

        last_flight = response_data['result']['response']['data'][-1]

        timestamp = last_flight['time']['scheduled']['departure']
        older_then_flight_id = last_flight['identification']['id']

        self.next_query['page'] += 1
        self.next_query['timestamp'] = timestamp
        self.next_query['older_then_flight_id'] = older_then_flight_id

    def _reset_next_query(self):
        self.next_query = {
            'page': 1,
            'timestamp': '',
            'older_then_flight_id': ''
        }

    def _iter_data_page(self, query):
        params = {
            'query': query.strip().lower(),
            'fetchBy': 'reg',
            'page': self.next_query['page'],
            'pk': '',
            'limit': '100',

            # a cookie set @ login, lives throughout session, `FR24ID`
            'token': self.token,

            # empty for first request
            'timestamp': self.next_query['timestamp'],
            'olderThenFlightId': self.next_query['older_then_flight_id']
        }

        sleep(1.0)

        response = self.session.get(
            Client.API_BASE_URL + 'flight/list.json',
            headers=COMMON_HEADERS,
            params=params
        )

        # -------------------------------------------------------------------

        if response.status_code in (402, ):
            return

        if response.status_code in (429, ):
            print('--- sleeping')

            return

        # -------------------------------------------------------------------

        response_data = response.json()

        # -------------------------------------------------------------------

        # if response_data['errors']['message'] == (
        #         'Your requests have been rate limited.'
        # ):
        #     return

        # -------------------------------------------------------------------

        self._set_next_query(response_data)

        # noinspection PyBroadException
        try:
            flights_list = response_data['result']['response']['data']

            if flights_list is None:
                flights_list = []

        except Exception as e:
            print(e)
            flights_list = []

        for flight_info in flights_list:
            flight = Flight.from_dict(flight_info)

            yield flight

    def iter_flights(self, reg_num):
        self._reset_next_query()

        while True:
            if self.next_query is None:
                return

            for flight in self._iter_data_page(reg_num):
                yield flight


if __name__ == '__main__':
    c = Client(
        '***@yandex.ru',
        '***'
    )

    c.login()

    qq = get_reg_num_list('G600.xlsx')

    for q in qq:
        for fd in c.iter_flights(q):
            print(fd)

    c.logout()
