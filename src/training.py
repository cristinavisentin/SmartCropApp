from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from random import shuffle
from pickle import dump
import numpy as np
import pandas as pd

# Load dataset from disk
df = np.array(pd.read_csv('data/processed/yield.csv'))

# Columns:
# 0: Area
# 1: Item
# 2: Year
# 3: hg/ha_yield
# 4: average_rain_fall_mm_per_year
# 5: avg_temp

# Fit the encoder (columns Area and Item)
encoder = OneHotEncoder(sparse_output=False).fit(
    df[:, 0:2])

# Write the encoder to disk
with open('artifacts/encoder.pkl', 'wb') as encoder_file:
    dump(encoder, encoder_file)

# Encode categorical
encoded_values = pd.DataFrame(encoder.transform(
    df[:, 0:2]))

# Remove categorical (Area and Item), target (hg/ha_yield) and append encoded
X = np.concatenate(
    (df[:, [2]], df[:, 4:], encoded_values), axis=1)

# Fitting the scaler
scaler = StandardScaler()
scaler.fit(X)

# Write the scaler to disk
with open('artifacts/scaler.pkl', 'wb') as scaler_file:
    dump(scaler, scaler_file)


# Separate independent and dependent variable
X = scaler.transform(X)
y = df[:, 3]

# Shuffle data
to_shuffle = np.arange(X.shape[0])
shuffle(to_shuffle)
X = X[to_shuffle]
y = y[to_shuffle]

# Grid search
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

# Write the best estimator to disk
with open('artifacts/model.pkl', 'wb') as model_file:
    dump(grid.best_estimator_, model_file)
