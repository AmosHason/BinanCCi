import json
from math import exp, log, sqrt

from market_data import get_market_data
from settings import CONSTITUENTS_AMOUNT, CONSTITUENTS_FILE, FIAT_RATIO, PAIRING, RESELECT_CONSTITUENTS


def calculate_weights():
    if RESELECT_CONSTITUENTS:
        coin_ids = None
    else:
        try:
            with open(CONSTITUENTS_FILE) as f:
                coin_ids = json.load(f)
        except FileNotFoundError:
            coin_ids = None

    market_data = get_market_data(coin_ids)
    adjusted_market_caps = {c: _ewma(m['market_caps']) for (c, m) in market_data.items()}
    adjusted_market_caps = dict(sorted(adjusted_market_caps.items(), key=lambda i: i[1], reverse=True)[:CONSTITUENTS_AMOUNT])

    with open(CONSTITUENTS_FILE, 'w') as f:
        json.dump(list(adjusted_market_caps.keys()), f)

    return {**{PAIRING: FIAT_RATIO}, **{market_data[c]['symbol']: (1 - FIAT_RATIO) * w for (c, w) in _constituents_weights(adjusted_market_caps).items()}}


def _ewma(series, half_life=3):
    decay_rate = log(2) / half_life

    return sum([market_cap * exp(- decay_rate * i) for i, market_cap in enumerate(series)]) / \
        sum([exp(- decay_rate * i) for i in range(len(series))])


def _constituents_weights(adjusted_market_caps):
    sqrt_adjusted_market_caps = {coin_id: sqrt(adjusted_market_cap) for (coin_id, adjusted_market_cap) in adjusted_market_caps.items()}
    sqrt_adjusted_market_caps_sum = sum(sqrt_adjusted_market_caps.values())

    return {coin_id: sqrt_adjusted_market_cap / sqrt_adjusted_market_caps_sum for (coin_id, sqrt_adjusted_market_cap) in sqrt_adjusted_market_caps.items()}
