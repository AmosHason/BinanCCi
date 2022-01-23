from time import sleep

from pycoingecko import CoinGeckoAPI
from retrying import retry

from settings import COINGECKO_REQUEST_INTERVAL, PAIRING

cg = CoinGeckoAPI()
retry = retry(wait_fixed=3000, stop_max_delay=120000)


def get_market_data(coin_ids=None):
    if coin_ids is None:
        coins = _get_top_market_cap_coins()
    else:
        coins = _get_coins_metadata(coin_ids)
    for coin_id in coins:
        coins[coin_id]['market_caps'] = _get_coin_market_cap_daily_history_sorted_from_latest_to_earliest(coin_id)
        sleep(COINGECKO_REQUEST_INTERVAL)

    return coins


def _get_top_market_cap_coins():
    coin_ids = [c['id'] for c in cg.get_coins_markets(vs_currency='USD', order='market_cap_desc', per_page=250)]

    return _get_coins_metadata(coin_ids)


def _get_coins_metadata(coin_ids):
    coins_metadata = {}
    for coin_id in coin_ids:
        coin_metadata = retry(cg.get_coin_by_id)(coin_id)
        sleep(COINGECKO_REQUEST_INTERVAL)
        coins_metadata[coin_id] = \
            {
                'symbol': _symbol_on_binance(coin_id),
                'blacklisted': _is_coin_blacklisted(coin_metadata)
            }
        sleep(COINGECKO_REQUEST_INTERVAL)
    coins_metadata = {c: m for (c, m) in coins_metadata.items() if m['symbol'] is not None and not m['blacklisted']}

    return coins_metadata


@retry
def _symbol_on_binance(coin_id):
    tickers = cg.get_coin_ticker_by_id(coin_id, exchange_ids='binance', order='volume_desc')
    symbols = set([t['base'] for t in tickers['tickers'] if t['target'] == PAIRING])

    if len(symbols) > 0:
        return PAIRING if len(symbols) > 1 else symbols.pop()
    else:
        return None


def _is_coin_blacklisted(coin_metadata):
    unwanted = ['Stablecoin', 'Asset-backed', 'Wrapped', 'Seigniorage', 'Staking', 'Synths', 'Rebase', 'Index', 'Aave', 'Tokenized', 'Compound', 'Mirrored']

    return any([any([x in c for x in unwanted]) for c in coin_metadata['categories'] if c is not None])


@retry
def _get_coin_market_cap_daily_history_sorted_from_latest_to_earliest(coin_id, days=30):
    return [x[1] for x in cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='USD', days=days, interval='daily')['market_caps'][:days]][::-1]
