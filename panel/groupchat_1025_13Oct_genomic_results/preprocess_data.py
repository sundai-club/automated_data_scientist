# filename: preprocess_data.py

import pandas as pd
import numpy as np
from sklearn import preprocessing

# Update this to your actual data path
data_path = "/Users/ai/Documents/sundai/automated-data-scientist/panel/homo_sapiens_genomics.csv"

# Load the data
data = pd.read_csv(data_path)

# Keep only the numeric columns
numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()

if len(numeric_columns) > 0:
    # Drop rows with missing values
    data = data[numeric_columns].dropna()

    if len(data) > 0:
        # Standardizing the features
        data = pd.DataFrame(preprocessing.StandardScaler().fit_transform(data), 
                            columns=numeric_columns)
        print("Data preprocess completed. The data now looks like this:")
        print(data.head())
    else:
        print("No rows left after dropping rows with missing values in numeric columns.")
else:
    print("No numeric columns found in the data.")