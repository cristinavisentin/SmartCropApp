# Read dataset from file
import pandas as pd


df = pd.read_csv('data/raw/yield_df.csv', index_col=0)

# Remove unneded variables
df.drop(['pesticides_tonnes'], axis=1, inplace=True)

df.to_csv('data/processed/yield.csv', index_label=False)
