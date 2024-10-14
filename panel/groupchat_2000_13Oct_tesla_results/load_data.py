# filename: load_data.py

import pandas as pd

# Load dataset
data = pd.read_csv('/Users/ai/Documents/sundai/automated-data-scientist/panel/TSLA.csv')

# Print the top 5 rows of the dataframe
print(data.head())