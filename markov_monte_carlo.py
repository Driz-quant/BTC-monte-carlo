import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# Get BTC data
btc = yf.download("BTC-USD", period="1y", interval="1d")
returns = btc["Close"].pct_change().dropna().values.flatten()

# Step 1 — Label each day as bear, sideways or bull
def get_state(r):
    if r < -0.01:
        return 0  # bear
    elif r > 0.01:
        return 2  # bull
    else:
        return 1  # sideways

states = [get_state(r) for r in returns]

# Step 2 — Build the transition matrix
# 3x3 table: rows = today's state, columns = tomorrow's state
matrix = np.zeros((3, 3))

for i in range(len(states) - 1):
    today = states[i]
    tomorrow = states[i + 1]
    matrix[today][tomorrow] += 1

# Convert counts to probabilities (each row adds up to 1)
for i in range(3):
    row_total = matrix[i].sum()
    if row_total > 0:
        matrix[i] = matrix[i] / row_total

print("Transition matrix (rows=today, cols=tomorrow):")
print("        Bear  Sideways  Bull")
labels = ["Bear    ", "Sideways", "Bull    "]
for i, row in enumerate(matrix):
    print(f"{labels[i]}  {row[0]:.2f}     {row[1]:.2f}     {row[2]:.2f}")

# Step 3 — Group returns by state
bear_returns   = [r for r, s in zip(returns, states) if s == 0]
sideways_returns = [r for r, s in zip(returns, states) if s == 1]
bull_returns   = [r for r, s in zip(returns, states) if s == 2]

# Step 4 — Run simulation
num_simulations = 1000
num_days = 90
last_price = btc["Close"].iloc[-1].item()

results = []

for i in range(num_simulations):
    prices = [last_price]
    current_state = states[-1]  # start from where BTC is today

    for day in range(num_days):
        # Pick tomorrow's state based on today's probabilities
        current_state = np.random.choice([0, 1, 2], p=matrix[current_state])

        # Pick a random return from that state's historical returns
        if current_state == 0:
            r = np.random.choice(bear_returns)
        elif current_state == 1:
            r = np.random.choice(sideways_returns)
        else:
            r = np.random.choice(bull_returns)

        next_price = prices[-1] * (1 + r)
        prices.append(next_price)

    results.append(prices)

# Step 5 — Plot
plt.figure(figsize=(12, 6))
for prices in results:
    plt.plot(prices, alpha=0.05, color="blue")

mean_prices = np.mean(results, axis=0)
plt.plot(mean_prices, color="red", linewidth=2, label="Average")
plt.legend()
plt.title("Markov Chain Monte Carlo — BTC Next 90 Days (1000 scenarios)")
plt.xlabel("Days")
plt.ylabel("Price (USD)")
plt.tight_layout()
plt.show()