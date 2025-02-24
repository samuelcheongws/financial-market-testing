import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Load interest rate data
interest_rate_data = pd.read_csv("fed-funds-rate-2010-2025.csv", parse_dates=["date"], dayfirst=True)
interest_rate_data.set_index("date", inplace=True)

# Download historical data for QQQ, TQQQ, and QLD
symbols = ["QQQ", "TQQQ", "QLD"]
data = yf.download(symbols, start="2022-01-01", end="2024-01-01")['Close']

# Calculate daily returns
daily_returns = data.pct_change().dropna()

# Ensure 'date' is in datetime format for both DataFrames
# daily_returns['date'] = daily_returns.index
# interest_rate_data['date'] = interest_rate_data.index
interest_rate_data['value'] = interest_rate_data['value'].fillna(method='ffill')
print(daily_returns)
print(interest_rate_data)


# Calculate daily interest rate
# Add whole numbers to adjust interest rate. Add 1 for 1 percent.
actual_bank_ir_adjustment = 1
interest_rate_data['daily_ir'] = (interest_rate_data['value'] + actual_bank_ir_adjustment) / 252 / 100

# Merge on the 'date' column using an exact match
daily_returns = daily_returns.join(interest_rate_data)


# Construct portfolio returns
portfolio_returns = 0.5 * daily_returns["TQQQ"] + 0.5 * daily_returns["QQQ"]

# Traditional 2x leverage with variable interest cost
leverage_factor = 2.0
leveraged_returns = leverage_factor * daily_returns["QQQ"] - (leverage_factor - 1) * daily_returns["daily_ir"]

# print(data)
print(daily_returns)
print(interest_rate_data)


# Calculate cumulative returns
cumulative_returns_50_50 = (1 + portfolio_returns).cumprod()
cumulative_returns_qld = (1 + daily_returns["QLD"]).cumprod()
cumulative_returns_leveraged = (1 + leveraged_returns).cumprod()

# Plot performance
plt.figure(figsize=(12, 6))
plt.plot(cumulative_returns_50_50, label='50% TQQQ + 50% QQQ', linestyle='--')
plt.plot(cumulative_returns_qld, label='100% QLD', linestyle='dashdot')
plt.plot(cumulative_returns_leveraged, label='Traditional 2x Leverage on QQQ', linestyle='-')
plt.title('Backtest: 50% TQQQ + 50% QQQ vs 100% QLD vs Traditional 2x Leverage')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.legend()
plt.grid()
plt.show()
