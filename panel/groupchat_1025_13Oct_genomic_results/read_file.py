# filename: read_file.py

import pandas as pd

# Provide the path to the file
file_path = "/Users/ai/Documents/sundai/automated-data-scientist/panel/homo_sapiens_genomics.csv"

# Use pandas to read the CSV file
df = pd.read_csv(file_path)

# Print the content of the file
print(df)