from binance_api import get_balances
from constituents import calculate_weights
from portfolio_rebalancing import rebalance

balances = get_balances()
print(f'Portfolio before rebalance: {balances}')
weights = calculate_weights()
print(f'Updated weights: {weights}')
rebalance(weights, balances)
print(f'Portfolio after rebalance: {get_balances()}')
