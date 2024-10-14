# filename: load_data.py

import pandas as pd

# Update this to your actual data path
data_path = "/Users/ai/Documents/sundai/automated-data-scientist/panel/homo_sapiens_genomics.csv"

# Load the data
data = pd.read_csv(data_path)

# Print the first few rows of the data
print(data.head())