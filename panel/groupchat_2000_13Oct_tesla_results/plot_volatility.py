# filename: plot_volatility.py

import pandas as pd
import matplotlib.pyplot as plt

# Read the TSLA.csv data
try:
    data = pd.read_csv('TSLA.csv')
except FileNotFoundError:
    print("TSLA.csv not found in the current directory.")
    exit()

# Ensure 'Date' and 'Close' columns exist
if 'Date' not in data.columns or 'Close' not in data.columns:
    print("Required 'Date' and/or 'Close' column(s) missing in the CSV file.")
    exit()

# Print the fields in the dataset
print("Fields in the dataset:")
print(data.columns.tolist())

# Convert Date to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Set Date as the index 
data.set_index('Date', inplace=True)

# Calculate the daily return 
data['Returns'] = data['Close'].pct_change()

# Calculate the rolling standard deviation of returns over a window you define, e.g., 50 days
data['Volatility'] = data['Returns'].rolling(window=50).std()

# Drop the 'Returns' column
data = data.drop(columns=['Returns'])

# Print some data statistics before visualizing it
print("\nData description:\n")
print(data.describe())

# Plot the daily volatility
plt.plot_date(data.index, data['Volatility'])
plt.title('Tesla - Daily Volatility')
plt.xlabel('Date')
plt.ylabel('Volatility')

# Save the plot to a file
plt.savefig('TSLA_volatility.png')