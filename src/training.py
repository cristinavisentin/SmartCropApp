

import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Load dataset from disk
df = pd.read_csv('data/processed/yield.csv')

# Fit the encoder
encoder = OneHotEncoder(sparse_output=False).fit(
    df[['Item', 'Area']])

# Write the encoder to disk
encoder_file = open('artifacts/encoder.pkl', 'wb')
pickle.dump(encoder, encoder_file)
encoder_file.close()

# Encode categorical
encoded_values = pd.DataFrame(encoder.transform(
    df[['Item', 'Area']]), columns=encoder.get_feature_names_out())
X = df.drop(['Area', 'Item', 'hg/ha_yield'], axis=1).join(encoded_values)

# Fitting the scaler
scaler = StandardScaler()
scaler.fit(X)

# Write the scaler to disk
scaler_file = open('artifacts/scaler.pkl', 'wb')
pickle.dump(scaler, scaler_file)
scaler_file.close()


# Separate independent and depenedent variable
X = scaler.transform(X)
y = df['hg/ha_yield']

forest = RandomForestRegressor(n_estimators=50, n_jobs=-1, random_state=666)

forest.fit(X, y)
pickle.dump(forest, open('artifacts/model.pkl', 'wb'))
