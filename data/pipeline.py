import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import kagglehub
from sklearn.preprocessing import OneHotEncoder

path = kagglehub.dataset_download("patelris/crop-yield-prediction-dataset")
df = pd.read_csv(path + '/yield_df.csv')
df.dropna(inplace=True)
encoder = OneHotEncoder()
encoded = pd.DataFrame(encoder.fit_transform(df[['Area', 'Item']]))
encoder.get_feature_names_out()
