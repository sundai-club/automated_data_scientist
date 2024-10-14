# filename: visualize_tesla_volatility.py

import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the CSV file
df = pd.read_csv('./TSLA.csv')

# Step 2: Print the data fields
print(df.columns)

# Step 3: Calculate the daily volatility
df['Volatility'] = df['Close'].pct_change()

# print the head of the data frame to check if the 'Volatility' column has been added
print(df.head())

# Step 4: Plot daily volatility
plt.figure(figsize=(10, 8))
plt.plot(df['Date'], df['Volatility'])
plt.title('Tesla Daily Volatility')
plt.xlabel('Date')
plt.ylabel('Volatility')

# Step 5: Save the plot to a file
plt.savefig('tesla_volatility.png')

print("Visualizing data and saving the plot is completed.")