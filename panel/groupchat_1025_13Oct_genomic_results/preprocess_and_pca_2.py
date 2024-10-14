# filename: preprocess_and_pca_2.py

import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Update this to your actual data path
data_path = "/Users/ai/Documents/sundai/automated-data-scientist/panel/homo_sapiens_genomics.csv"

# Load the data
data = pd.read_csv(data_path)

# Convert all columns to numeric, errors='coerce' forces invalid values to NaN
data = data.apply(pd.to_numeric, errors='coerce')

# Now drop the columns with all NaN values
data = data.dropna(axis=1, how='all')

# Now select the numeric columns
numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()

# Fill NA values with the column means
data[numeric_columns] = data[numeric_columns].fillna(data.mean())

# Standardizing the features
data[numeric_columns] = preprocessing.StandardScaler().fit_transform(data[numeric_columns])

# Perform PCA
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(data[numeric_columns])

principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])

plt.figure(figsize=(8,6))
plt.scatter(principalDf['principal component 1'], principalDf['principal component 2'])
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('2-Component PCA')
plt.show()