# filename: calc_volatility.py

import pandas as pd
import numpy as np

# Load dataset
data = pd.read_csv('/Users/ai/Documents/sundai/automated-data-scientist/panel/TSLA.csv')

# Calculate daily returns
data['Return'] = data['Close'].pct_change()

# Drop missing values
data.dropna(inplace=True)

# Calculate volatility
volatility = data['Return'].std() * np.sqrt(252)

print(f"The annual volatility of the TESLA stock data is: {volatility}")