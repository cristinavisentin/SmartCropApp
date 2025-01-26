import numpy as np
import pandas as pd


def find_outliers(x):
    q1 = np.quantile(x, 0.25, axis=0)
    q3 = np.quantile(x, 0.75, axis=0)
    iqr = q3-q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5*iqr
    return (x >= lower) & (x <= upper)


# Read dataset from file
df = pd.read_csv('data/raw/yield_df.csv', index_col=0)

# Remove unneeded variables
df.drop(['pesticides_tonnes'], axis=1, inplace=True)

# Remove duplicated rows
df.drop_duplicates(inplace=True)

# Remove outliers
df = df[np.all(find_outliers(
    df[['hg/ha_yield', 'avg_temp', 'average_rain_fall_mm_per_year']]), axis=1)]

# Save cleaned dataset to file
df.to_csv('data/processed/yield.csv', index=False)
