import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# Add the root directory to the python path to allow running this script from anywhere
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.order_book import OrderBook
from src.order_flow import OrderFlowSimulator
from src.market_maker import MarketMaker

# -----------------------
# Setup result folders
# -----------------------
BASE_DIR = "experiments/results"
PLOT_DIR = f"{BASE_DIR}/plots"
DATA_DIR = f"{BASE_DIR}/data"

os.makedirs(PLOT_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)


def run_simulation(volatility, lambda_limit, steps=5000):
    ob = OrderBook()
    sim = OrderFlowSimulator(
        ob,
        lambda_market=0.6,
        lambda_limit=lambda_limit,
        volatility=volatility
    )
    mm = MarketMaker(ob)

    for _ in range(steps):
        mm.post_quotes(volatility)
        trades, side = sim.step()
        mm.process_trades(trades, side)
        mm.record()

    df = pd.DataFrame({
        "price": sim.price_history,
        "spread": sim.spread_history[:len(sim.price_history)],
        "inventory": mm.inventory_history,
        "pnl": mm.pnl_history
    })

    return df


# =========================
# EXPERIMENT 1: VOLATILITY
# =========================
vols = [0.5, 1.0, 1.5, 2.0]

plt.figure(figsize=(10, 5))
for v in vols:
    df = run_simulation(volatility=v, lambda_limit=1.0)
    df.to_csv(f"{DATA_DIR}/volatility_{v}.csv", index=False)
    plt.plot(df["pnl"], label=f"Vol={v}")

plt.title("Market Maker PnL under Volatility Shock")
plt.xlabel("Time")
plt.ylabel("PnL")
plt.legend()
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/pnl_vs_volatility.png")
plt.close()


# =========================
# EXPERIMENT 2: LIQUIDITY
# =========================
liqs = [2.0, 1.0, 0.5, 0.2]

plt.figure(figsize=(10, 5))
for l in liqs:
    df = run_simulation(volatility=1.0, lambda_limit=l)
    df.to_csv(f"{DATA_DIR}/liquidity_{l}.csv", index=False)
    plt.plot(df["price"], label=f"Liquidity={l}")

plt.title("Price Dynamics during Liquidity Dry-Up")
plt.xlabel("Time")
plt.ylabel("Mid Price")
plt.legend()
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/price_vs_liquidity.png")
plt.close()

print("Experiments complete. Results saved in experiments/results/")
