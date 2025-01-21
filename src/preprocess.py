import numpy as np
import pandas as pd


def find_outliers(X):
    Q1 = np.quantile(X, 0.25, axis=0)
    Q3 = np.quantile(X, 0.75, axis=0)
    IQR = Q3-Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5*IQR
    return (X >= lower) & (X <= upper)


# Read dataset from file
df = pd.read_csv('data/raw/yield_df.csv', index_col=0)

# Remove unneded variables
df.drop(['pesticides_tonnes'], axis=1, inplace=True)

# Remove duplicated rows
df.drop_duplicates(inplace=True)

# Remove outliers
df = df[np.all(find_outliers(
    df[['hg/ha_yield', 'avg_temp', 'average_rain_fall_mm_per_year']]), axis=1)]

# Save cleaned dataset to file
df.to_csv('data/processed/yield.csv', index=False)
