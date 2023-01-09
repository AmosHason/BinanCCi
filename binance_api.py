import requests

from settings import API_BASE, PAIRING
from signed_requests import send_signed_request


def get_balances():
    res = send_signed_request('GET', f'{API_BASE}/api/v3/account')

    balances = {}
    for item in res['balances']:
        quantity = float(item['free'])
        if quantity > 0:
            balances[item['asset']] = quantity

    return balances


def get_exchange_stepsize(symbol):
    filters = requests.get(f'{API_BASE}/api/v3/exchangeInfo?symbol={symbol}').json()['symbols'][0]['filters']

    return float([f for f in filters if f['filterType'] == 'LOT_SIZE'][0]['stepSize'])


def get_price(symbol):
    try:
        return float(requests.get(f'{API_BASE}/api/v3/ticker/price?symbol={symbol}{PAIRING}').json()['price'])
    except KeyError:
        return None


def create_order(symbol, side, quantity):
    path = f'{API_BASE}/api/v3/order'
    params = {'symbol': symbol,
              'side': side,
              'quantity': quantity,
              'type': 'MARKET'}

    return send_signed_request('POST', path, params)
