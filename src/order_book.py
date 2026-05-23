# order_book.py

class OrderBook:
    def __init__(self):
        self.bids = {}  # price -> quantity
        self.asks = {}  # price -> quantity

    # ---------- Best Prices ----------
    def best_bid(self):
        return max(self.bids.keys()) if self.bids else None

    def best_ask(self):
        return min(self.asks.keys()) if self.asks else None

    def spread(self):
        if self.best_bid() is None or self.best_ask() is None:
            return None
        return self.best_ask() - self.best_bid()

    def mid_price(self):
        if self.spread() is None:
            return None
        return (self.best_bid() + self.best_ask()) / 2

    # ---------- Limit Orders ----------
    def add_limit_buy(self, price, quantity):
        self.bids[price] = self.bids.get(price, 0) + quantity

    def add_limit_sell(self, price, quantity):
        self.asks[price] = self.asks.get(price, 0) + quantity

    # ---------- Market Orders ----------
    def market_buy(self, quantity):
        trades = []
        while quantity > 0 and self.asks:
            price = self.best_ask()
            available = self.asks[price]
            traded = min(quantity, available)

            trades.append((price, traded))
            self.asks[price] -= traded
            quantity -= traded

            if self.asks[price] == 0:
                del self.asks[price]
        return trades

    def market_sell(self, quantity):
        trades = []
        while quantity > 0 and self.bids:
            price = self.best_bid()
            available = self.bids[price]
            traded = min(quantity, available)

            trades.append((price, traded))
            self.bids[price] -= traded
            quantity -= traded

            if self.bids[price] == 0:
                del self.bids[price]
        return trades

    # ---------- Depth ----------
    def depth(self, levels=3):
        bid_levels = sorted(self.bids.items(), reverse=True)[:levels]
        ask_levels = sorted(self.asks.items())[:levels]
        return bid_levels, ask_levels
