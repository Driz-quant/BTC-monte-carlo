import yfinance as yf
import matplotlib.pyplot as plt

# Download BTC price data (last 1 year, daily candles)
btc = yf.download("BTC-USD", period="1y", interval="1d")

# Show the last 5 rows in the terminal
print(btc.tail())

# Plot the closing price
btc["Close"].plot(title="Bitcoin Price - Last 1 Year", figsize=(12, 5))
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.tight_layout()
plt.show()
