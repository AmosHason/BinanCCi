import hashlib
import hmac
import time
from urllib.parse import urlencode

import requests

from settings import API_KEY, SECRET_KEY


def send_signed_request(http_method, url, payload=None):
    payload = payload or {}

    query = urlencode(payload, True)
    if query:
        query = '{}&timestamp={}'.format(query, _get_timestamp())
    else:
        query = 'timestamp={}'.format(_get_timestamp())

    url = url + '?' + query + '&signature=' + _hashing(query)
    params = {'url': url, 'params': {}}
    response = _dispatch_request(http_method)(**params)

    return response.json()


def _get_timestamp():
    return int(time.time() * 1000)


def _hashing(query):
    return hmac.new(SECRET_KEY.encode('utf-8'), query.encode('utf-8'), hashlib.sha256).hexdigest()


def _dispatch_request(http_method):
    session = requests.Session()
    session.headers.update({'Content-Type': 'application/json;charset=utf-8', 'X-MBX-APIKEY': API_KEY})

    return {'GET': session.get, 'POST': session.post}[http_method]
