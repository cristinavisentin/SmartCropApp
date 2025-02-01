import streamlit as st
import pickle
import time
import os
import pandas as pd
from db_utils import add_prediction_to_db

base_dir = os.path.dirname(os.path.abspath(__file__))
encoder_path = os.path.join(base_dir, '../artifacts/encoder.pkl')

with open(os.path.join(base_dir, '../artifacts/encoder.pkl'), 'rb') as file:
    encoder = pickle.load(file)
with open(os.path.join(base_dir, '../artifacts/scaler.pkl'), 'rb') as file:
    scaler = pickle.load(file)
with open(os.path.join(base_dir, '../artifacts/model.pkl'), 'rb') as file:
    model = pickle.load(file)


def get_prediction(plant, country, avg_temperature, avg_rainfall, hectares):
    print("user: [", st.session_state["username"], "] VALUED USED IN THIS PREDICTION:", plant, country, avg_temperature, avg_rainfall)
    try:
        encoded = encoder.transform([[country, plant]])
        other_vals = [[2025, avg_rainfall, avg_temperature]]

        other_vals[0].extend(encoded[0])
        to_predict = scaler.transform(other_vals)
    except Exception as e:
        st.error("the data you entered is not compatible with the model")
        print("the data user entered is not compatible with the model: ", e)
        st.session_state["page"] = "crop_application_single_prediction"
        time.sleep(3)
        st.rerun()
    prediction = model.predict(to_predict)[0]
    predicted_quintals = round(((prediction / 1000) * hectares), 2)
    return predicted_quintals

def display_result_and_add_to_db(plant, country, avg_temperature, avg_rainfall, hectares):
    prediction = get_prediction(plant, country, avg_temperature, avg_rainfall, hectares)
    add_prediction_to_db(st.session_state["username"], plant, country, int(hectares), prediction)
    st.markdown(f"### {prediction} quintals")
    st.write("\n\n")

def display_table_of_inserted_values(plants, country, hectares):
    results = list(zip(plants, country, hectares))
    df = pd.DataFrame(results, columns=["Plant", "Country", "Hectares"])
    if len(plants) == 0:
        df.index = ""
    else:
        df.index = df.index + 1
    st.table(df)

def prediction_result_page():
    st.title("Prediction Result")
    st.write("After some research, we were able to get other data from your area, such as annual rainfall and temperatures, we used this data to best predict the production you can achieve in your fields")
    if "plant" in st.session_state and "country" in st.session_state:
        plants = st.session_state["plant"]
        country = st.session_state["country"]
        avg_temperature = st.session_state["avg_temperature"]
        avg_rainfall = st.session_state["avg_rainfall"]
        hectares = st.session_state["acres_to_cultivate"]

        if len(plants) == len(country) == len(avg_temperature) == len(avg_rainfall) == len(hectares) == 1:
            display_table_of_inserted_values(plants, country, hectares)
            display_result_and_add_to_db(plants[0], country[0], avg_temperature[0], avg_rainfall[0], hectares[0])

        elif len(plants) == len(country) == len(avg_temperature) == len(avg_rainfall) == len(hectares) == 3:
            display_table_of_inserted_values(plants, country, hectares)
            st.markdown("## First prediction:")
            display_result_and_add_to_db(plants[0], country[0], avg_temperature[0], avg_rainfall[0], hectares[0])
            st.markdown("## Second prediction:")
            display_result_and_add_to_db(plants[1], country[1], avg_temperature[1], avg_rainfall[1], hectares[1])
            st.markdown("## Third prediction:")
            display_result_and_add_to_db(plants[2], country[2], avg_temperature[2], avg_rainfall[2], hectares[2])
        else:
            st.write("You inserted bad data")
    else:
        st.write("No data found in session state.")



