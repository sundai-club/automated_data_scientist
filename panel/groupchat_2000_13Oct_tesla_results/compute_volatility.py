# filename: compute_volatility.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('/Users/ai/Documents/sundai/automated-data-scientist/panel/TSLA.csv')

# Ensure the data is sorted by date
data = data.sort_values('Date')

# Calculate the daily returns
data['daily_return'] = data['Close'].pct_change()

# Drop NA values
data = data.dropna()

# Calculate the standard deviation of daily returns
volatility = data['daily_return'].std()

# Print the volatility
print(f"The volatility of the stock is {volatility}")

# Generate a plot of the daily return volatility
plt.figure(figsize=(10,8))
plt.plot(data['Date'], data['daily_return'])
plt.title('Volatility of TSLA')
plt.xlabel('Date')
plt.ylabel('Daily Returns')
plt.grid(True)
plt.show()