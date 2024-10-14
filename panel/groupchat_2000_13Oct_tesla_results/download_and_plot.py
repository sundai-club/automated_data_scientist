# filename: download_and_plot.py

import pandas as pd
import matplotlib.pyplot as plt

try:
    # Load the data
    df = pd.read_csv('/Users/ai/Documents/sundai/automated-data-scientist/panel/TSLA.csv')
except FileNotFoundError:
    print("The specified file could not be found.")
    exit()

try:
    # Print the fields of the dataset
    print("Fields in the dataset: ", df.columns.tolist())
    
    # Verify existence of required fields
    assert set(['Date', 'High', 'Low']).issubset(df.columns), "Required fields don't exist in the CSV file"
    
    # Confirm data type of 'High' and 'Low' columns
    assert pd.api.types.is_numeric_dtype(df['High']), "'High' column should be numeric"
    assert pd.api.types.is_numeric_dtype(df['Low']), "'Low' column should be numeric"

    # Confirm there are no missing values in 'High' and 'Low' columns
    assert df['High'].notnull().all(), "'High' column contains missing values"
    assert df['Low'].notnull().all(), "'Low' column contains missing values"
    
    # Calculate daily volatility
    df['Volatility'] = df['High'] - df['Low']

    # Create a plot
    plt.figure(figsize=(10,5))
    plt.plot(df['Date'], df['Volatility'])
    plt.xlabel('Date')
    plt.ylabel('Volatility')
    plt.title('Daily Volatility of TSLA')
    plt.grid()

    # Save the plot to a file
    plt.savefig('TSLA_Volatility.png')

    print("The plot has been saved as 'TSLA_Volatility.png'.")
except Exception as e:
    print(f"An error occurred: {str(e)}")