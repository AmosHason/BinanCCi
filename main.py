from binance_api import get_balances
from constituents import calculate_weights
from portfolio_rebalancing import rebalance

print(f'Portfolio before rebalance: {get_balances()}')
weights = calculate_weights()
print(f'Updated weights: {weights}')
rebalance(weights)
print(f'Portfolio after rebalance: {get_balances()}')
