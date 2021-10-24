import math
import time

from binance_api import create_order, get_balances, get_exchange_stepsize, get_price
from settings import BINANCE_ORDER_MIN_USDT, PAIRING, WAIT_SECONDS_BETWEEN_ORDERS


def rebalance(required_weights):
    required_changes = _get_required_changes_in_portfolio(required_weights)

    for change in required_changes:
        symbol = f'{change[0]}{PAIRING}'

        if symbol == f'{PAIRING}{PAIRING}':
            continue

        quantity = round(change[2], int(-math.log10(get_exchange_stepsize(symbol))))

        if change[1] < -BINANCE_ORDER_MIN_USDT:
            create_order(symbol, 'sell', -quantity)
            time.sleep(WAIT_SECONDS_BETWEEN_ORDERS)
        elif change[1] > BINANCE_ORDER_MIN_USDT:
            create_order(symbol, 'buy', quantity)
            time.sleep(WAIT_SECONDS_BETWEEN_ORDERS)


def _get_required_changes_in_portfolio(required_weights):
    portfolio = {s: {'balance': b} for (s, b) in get_balances().items()}

    for symbol in required_weights:
        if symbol not in portfolio:
            portfolio[symbol] = {'balance': 0}

    for symbol in portfolio:
        if symbol == PAIRING:
            price = 1
        else:
            price = get_price(symbol)
        portfolio[symbol]['price'] = price
        portfolio[symbol]['value'] = portfolio[symbol]['balance'] * price

    total_value = sum([portfolio[s]['value'] for s in portfolio])

    for symbol in portfolio:
        if symbol not in required_weights:
            portfolio[symbol]['required_change'] = -portfolio[symbol]['balance']
            portfolio[symbol]['required_change_in_value'] = portfolio[symbol]['required_change'] * portfolio[symbol]['price']
        else:
            portfolio[symbol]['required_change_in_value'] = required_weights[symbol] * total_value - portfolio[symbol]['value']
            portfolio[symbol]['required_change'] = portfolio[symbol]['required_change_in_value'] / portfolio[symbol]['price']

    required_changes = [(s, portfolio[s]['required_change_in_value'], portfolio[s]['required_change']) for s in portfolio if portfolio[s]['required_change'] != 0]

    def f(x):
        if x < 0:
            return -x  # First of all, sell assets by descending order of action value.
        if x > 0:
            return -1/x  # Then, buy assets by descending order of action value.

    required_changes.sort(key=lambda x: f(x[1]), reverse=True)

    return required_changes
