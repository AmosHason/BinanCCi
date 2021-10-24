# BinanCCi

#### Rebalance your Binance portfolio according to the [CCi30](https://cci30.com/) index.

So you want to invest in the cryptocurrency market, but, like me, you are a passive investor who only looks for a **sufficient exposure**. Surely you can try the other index-tracking solutions, but why pay high fees when you can simply run this script once a month?

## Instructions

1. Install **Python 3** (tested on Python 3.9).
2. Install **packages** from *requirements.txt*.
3. Fill your Binance **API key** and **secret key** in *credentials.py*.
4. Adjust **settings** in *settings.py*. You would most likely want to adjust **FIAT_RATIO**, **RESELECT_CONSTITUENTS** and **CONSTITUENTS_AMOUNT** according to your plan.
5. Run ***main.py***.
6. Wait **a few minutes** (almost nothing is printed to console, so it may just look like nothing happens).

### Settings

1. **PAIRING**: Symbol on Binance of the desired USD stablecoin against which to perform orders (tested on the default, USDT).
2. **FIAT_RATIO**: Desired ratio of **PAIRING** (USD stablecoin) in the portfolio. The remainder will be invested according to the index.
3. **COINGECKO_REQUEST_INTERVAL**: Interval between adjacent requests to CoinGecko API (in seconds).
4. **CONSTITUENTS_FILE**: File in which to save the CoinGecko IDs of the current constituents.
5. **RESELECT_CONSTITUENTS**: *True* to rebalance on a reselection of constituents (this will regardless happen on the first run); *False* to rebalance on the current constituents (saved in **CONSTITUENTS_FILE**).
6. **CONSTITUENTS_AMOUNT**: Desired amount of constituents.
7. **BINANCE_ORDER_MIN_USD**: Minimal order value in USD on Binance (currently 10).
8. **WAIT_SECONDS_BETWEEN_ORDERS**: Interval between adjacent orders on Binance.
9. **API_BASE**: Binance API base address.

## Notes

1. The constituents are selected according to the CCi30 selection algorithm, with a few caveats:
   1. You may adjust the number of constituents (not necessarily 30).
   2. The algorithm is run on market data from the top 250 cryptocurrencies by current market cap.
   3. Only cryptocurrencies which are traded on Binance may be selected.
   4. In addition to stablecoins, the algorithm filters out cryptocurrencies that belong to either of the Asset-backed, Wrapped, Seigniorage, Staking, Synths, Rebase, Index, Aave, Tokenized, Compound and Mirrored categories, as these are mostly kinds of derivatives.
2. The official CCi30 index constituents are **reselected on the first day of each quarter** and **reweighted on the first day of each month**. You may get different results depending on the timings of your runs, but overall the concept is the same.
