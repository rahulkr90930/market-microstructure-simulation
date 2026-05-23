# order_flow.py

import numpy as np

class OrderFlowSimulator:
    def __init__(self, order_book,
                 lambda_market=0.5,
                 lambda_limit=1.0,
                 volatility=1.0,
                 buy_prob=0.5):

        self.ob = order_book
        self.lambda_market = lambda_market
        self.lambda_limit = lambda_limit
        self.volatility = volatility
        self.buy_prob = buy_prob

        self.price_history = []
        self.spread_history = []

    def step(self):
        if np.random.rand() < self.lambda_market / (self.lambda_market + self.lambda_limit):
            trades, side = self.generate_market_order()
        else:
            trades, side = self.generate_limit_order()

        if self.ob.mid_price() is not None:
            self.price_history.append(self.ob.mid_price())
            self.spread_history.append(self.ob.spread())

        return trades, side

    # ---------- Market Orders ----------
    def generate_market_order(self):
        side = "buy" if np.random.rand() < self.buy_prob else "sell"
        size = max(1, int(np.random.exponential(scale=5 * self.volatility)))

        if side == "buy":
            trades = self.ob.market_buy(size)
        else:
            trades = self.ob.market_sell(size)

        return trades, side

    # ---------- Limit Orders ----------
    def generate_limit_order(self):
        mid = self.ob.mid_price() or 100
        side = "buy" if np.random.rand() < 0.5 else "sell"

        distance = max(1, int(np.random.exponential(scale=self.volatility)))
        price = mid - distance if side == "buy" else mid + distance
        size = max(1, int(np.random.exponential(scale=10)))

        if side == "buy":
            self.ob.add_limit_buy(price, size)
        else:
            self.ob.add_limit_sell(price, size)

        return [], side
