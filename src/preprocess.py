import pickle
import numpy as np
import pandas as pd
from sklearn.discriminant_analysis import StandardScaler
from sklearn.preprocessing import OneHotEncoder


def find_outliers(X):
    Q1 = np.quantile(X, 0.25, axis=0)
    Q3 = np.quantile(X, 0.75, axis=0)
    IQR = Q3-Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5*IQR
    return (X >= lower) & (X <= upper)


# Read dataset from file
df = pd.read_csv('data/raw/yield_df.csv')

# Remove duplicated rows
df.drop_duplicates(inplace=True)

# Remove outliers
df = df[np.all(find_outliers(
    df[['hg/ha_yield', 'avg_temp', 'average_rain_fall_mm_per_year']]), axis=1)]

# Remove unneded variables
df.drop(['Unnamed: 0', 'pesticides_tonnes'], axis=1, inplace=True)

# Save cleaned dataset to file
df.to_csv('data/processed/yield.csv')

# Encode categorical features
encoder = OneHotEncoder(sparse_output=False, dtype=int).fit(
    df[['Item', 'Area']])
encoded_values = pd.DataFrame(encoder.transform(
    df[['Item', 'Area']]), columns=encoder.get_feature_names_out())
df = df.drop(['Area', 'Item'], axis=1).join(encoded_values)

# Write the encoder to disk
encoder_file = open('encoder.pkl', 'wb')
pickle.dump(encoder, encoder_file)
encoder_file.close()


# Scaling numerical features
scaler = StandardScaler()
scaler.fit(df)

# Write the scaler to disk
scaler_file = open('scaler.pkl', 'wb')
pickle.dump(scaler, scaler_file)
scaler_file.close()
