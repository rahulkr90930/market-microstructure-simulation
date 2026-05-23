# market_maker.py

class MarketMaker:
    def __init__(self, order_book,
                 base_spread=2,
                 inventory_limit=100):

        self.ob = order_book
        self.base_spread = base_spread
        self.inventory_limit = inventory_limit

        self.inventory = 0
        self.cash = 0

        self.pnl_history = []
        self.inventory_history = []

    def mid_price(self):
        return self.ob.mid_price() or 100

    def inventory_skew(self):
        return self.inventory / self.inventory_limit

    def current_spread(self, volatility):
        return self.base_spread * volatility

    def post_quotes(self, volatility):
        mid = self.mid_price()
        spread = self.current_spread(volatility)
        skew = self.inventory_skew()

        bid = round(mid - spread / 2 - skew, 2)
        ask = round(mid + spread / 2 - skew, 2)

        self.ob.add_limit_buy(bid, 10)
        self.ob.add_limit_sell(ask, 10)

    def process_trades(self, trades, side):
        for price, qty in trades:
            if side == "buy":
                self.inventory -= qty
                self.cash += price * qty
            else:
                self.inventory += qty
                self.cash -= price * qty

    def mark_to_market(self):
        return self.cash + self.inventory * self.mid_price()

    def record(self):
        self.pnl_history.append(self.mark_to_market())
        self.inventory_history.append(self.inventory)
