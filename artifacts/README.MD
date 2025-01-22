# Artifacts

## Preprocessing

- In order to obtain the refined dataset, the column `pesticides_tonnes` is dropped as it encodes data not relevant to the purpose of the application and does not align with the interest of the company.
- Outliers not respecting the IQR rule are dropped from the dataset to avoid negative influence to the predictions.
- Duplicated rows are dropped from the dataset.

## Encoder

The `OneHotEncoder` object is saved to the `encoder.pkl` file to be ready to use in the application:
- it allows to take user input and encode categorical features like Country and crop item into numeric ones
- once encoded these value with `encoder.transform(input[['Item', 'Area']])` they can be used in the following steps

## Scaler

The `StandardScaler` object is saved to the `scaler.pkl` file to be ready to use in the application:
- it allows to scale encoded entries to allow their use inside the ML model.
- once scaled with `scaler.transform(input)` they can be passed to the model.

## Model

### RandomForestRegressor v1.0

The `RandomForestRegressor` object is saved to the `model.pkl` file to be ready to use in the application:
- parameters of the models are chosen across a grid of parameters using `GridSearchCV`; the best ones are
  - dio
  - la madonna
  - e sua madre
- predictions are performed with `model.predict(x)` and return a number representing the estimated **yield in hg/ha** for the given country and crop item.
- the application will only need to multiply it to the number of hectares to obtain the estimated yield in hectograms (units can change).
- metrics used to assess the model are **cross fold validation** using the standard metric of the regressor.
- other parameters we looked into are the test error:
  - **MAE**:
  - **MAPE**:
  - **MSE**:
  - **R2**: 