# BTC Monte Carlo

Monte Carlo and Markov chain simulations of Bitcoin's price, built in Python on real market data. A learning project exploring how quants think about uncertainty: instead of predicting one price, simulate thousands of possible futures and look at the spread.

**Tech:** Python, yfinance, NumPy, pandas, Matplotlib

---

## What's in here

| Script | What it does |
|---|---|
| `btc_data.py` | Downloads 1 year of daily BTC-USD candles from Yahoo Finance, prints the latest rows, and plots the closing price. |
| `monte_carlo.py` | Simulates 1,000 possible 90-day price paths by randomly resampling historical daily returns. Plots every path with the average path in red. |
| `markov_monte_carlo.py` | The upgrade. Labels each day as bear, sideways or bull, learns how those states follow each other, and simulates 1,000 paths where tomorrow's state depends on today's. |

---

## How it works

### Monte Carlo (`monte_carlo.py`)
1. Download a year of daily prices and convert them to daily percentage returns.
2. Start from today's price.
3. For each of the next 90 days, pick one historical daily return at random and apply it: `new_price = price * (1 + return)`.
4. Repeat for 1,000 scenarios and plot them all.

Each line on the chart is one possible future. The cloud widens over time because uncertainty compounds.

### Markov chain (`markov_monte_carlo.py`)
Real markets have momentum and clustering, so picking days completely at random misses something. This version adds memory:

1. **Label each day** as one of three states:
   - Bear: down more than 1%
   - Sideways: between -1% and +1%
   - Bull: up more than 1%
2. **Build a transition matrix**: a 3x3 table of probabilities answering "if today is X, what is the chance tomorrow is Y?"
3. **Simulate**: starting from the latest real state, pick tomorrow's state from the matrix, then draw a random historical return from that state. Repeat for 90 days and 1,000 scenarios.

Example transition matrix from one run (values change with the data window):

```
        Bear  Sideways  Bull
Bear     0.41    0.34    0.26
Sideways 0.24    0.47    0.30
Bull     0.34    0.45    0.21
```

Reading the first row: after a bear day, there was a 41% chance the next day was also a bear day. Sideways days were the stickiest in this sample, and bull days were the least likely to continue.

---

## Getting started

Requires Python 3.

```bash
pip install yfinance numpy matplotlib
```

Run any script from the project folder:

```bash
python btc_data.py
python monte_carlo.py
python markov_monte_carlo.py
```

The scripts pull fresh data every time (`period="1y"` means "the last year from today"), so the charts and the transition matrix will differ from run to run as the market moves.

---

## Limitations

- **Only one year of history.** Results depend heavily on the window. A recent crash or rally will skew everything.
- **The future is assumed to look like the past.** Both models resample returns that already happened, so they can't produce events outside that history.
- **Simple memory.** Monte Carlo treats every day as independent. The Markov version only looks back one day.
- **Simulates price, not trading results.** There is no strategy, fees or slippage here.
- **Not predictions and not financial advice.** This is an educational project.

---

## Ideas for next steps

- Probability stats from the simulations, such as the share of paths ending above or below a chosen price, and Value at Risk
- More states or different thresholds in the Markov model
- Feeding a trading strategy's returns into the simulation instead of raw BTC returns
- Testing other assets
