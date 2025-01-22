

import pickle
from random import shuffle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Load dataset from disk
df = pd.read_csv('data/processed/yield.csv')

# Fit the encoder
encoder = OneHotEncoder(sparse_output=False).fit(
    df[['Item', 'Area']])

# Write the encoder to disk
with open('artifacts/encoder.pkl', 'wb') as encoder_file:
    pickle.dump(encoder, encoder_file)

# Encode categorical
encoded_values = pd.DataFrame(encoder.transform(
    df[['Item', 'Area']]))

X = np.array(df.drop(['Area', 'Item', 'hg/ha_yield'],
             axis=1).join(encoded_values))

# Fitting the scaler
scaler = StandardScaler()
scaler.fit(X)

# Write the scaler to disk
with open('artifacts/scaler.pkl', 'wb') as scaler_file:
    pickle.dump(scaler, scaler_file)


# Separate independent and depenedent variable
X = scaler.transform(X)
y = np.array(df['hg/ha_yield'])

# Shuffle data
to_shuffle = np.arange(X.shape[0])
shuffle(to_shuffle)
X = X[to_shuffle]
y = y[to_shuffle]

forest = RandomForestRegressor(random_state=666)
param_grid = {
    'n_estimators': [10, 25, 50],
    'min_samples_split': [4, 10],
    'min_samples_leaf': [2, 4],
    'criterion': ['squared_error', 'friedman_mse', 'poisson'],
    'max_features': [None, 1, 'sqrt', 'log2']
}
grid = GridSearchCV(forest, param_grid, n_jobs=-1, verbose=1)
grid.fit(X, y)

with open('artifacts/model.pkl', 'wb') as model_file:
    pickle.dump(grid.best_estimator_, model_file)
