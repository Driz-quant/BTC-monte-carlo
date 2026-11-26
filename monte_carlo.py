import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# Get BTC data
btc = yf.download("BTC-USD", period="1y", interval="1d")

# Calculate daily percentage returns
returns = btc["Close"].pct_change().dropna().values.flatten()

# Simulation settings
num_simulations = 1000
num_days = 90
last_price = btc["Close"].iloc[-1]

# Run the simulations
results = []

for i in range(num_simulations):
    prices = [last_price]
    for day in range(num_days):
        random_return = np.random.choice(returns)
        next_price = prices[-1] * (1 + random_return)
        prices.append(next_price)
    results.append(prices)

# Plot everything
plt.figure(figsize=(12, 6))
for prices in results:
    plt.plot(prices, alpha=0.05, color="blue")
    import numpy as np
mean_prices = np.mean(results, axis=0)
plt.plot(mean_prices, color="red", linewidth=2, label="Average")
plt.legend()

plt.title("Monte Carlo Simulation — BTC Next 90 Days (1000 scenarios)")
plt.xlabel("Days")
plt.ylabel("Price (USD)")
plt.tight_layout()
plt.show()