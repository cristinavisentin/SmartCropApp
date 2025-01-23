import streamlit as st
import pickle

import os
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
    print("VALUED USED IN THIS PREDICTION:", plant, country, avg_temperature, avg_rainfall)
    encoded = encoder.transform([[country, plant]])
    other_vals = [[2025, avg_rainfall, avg_temperature]]

    other_vals[0].extend(encoded[0])
    to_predict = scaler.transform(other_vals)

    print("hectares received: ", hectares)
    prediction = model.predict(to_predict)[0]
    print("model in get_prediction(): ", prediction)
    predicted_quintals = round(((prediction / 1000) * hectares), 2)
    return predicted_quintals

def display_result_and_add_to_db(plant, country, avg_temperature, avg_rainfall, hectares):
    st.write("plant: ", plant, "country: ", country)
    st.write("avg_rainfall: ", avg_rainfall, "mm, avg_temperature: ", avg_temperature, "C")
    prediction = get_prediction(plant, country, avg_temperature, avg_rainfall, hectares)
    add_prediction_to_db(st.session_state["username"], plant, country, int(hectares), prediction)
    st.write("prediction: ", prediction, "ounces/hectare")


def prediction_result_page():
    st.title("Prediction Result")
    if "plant" in st.session_state and "country" in st.session_state:
        plants = st.session_state["plant"]
        country = st.session_state["country"]
        avg_temperature = st.session_state["avg_temperature"]
        avg_rainfall = st.session_state["avg_rainfall"]
        hectares = st.session_state["acres_to_cultivate"]
        if (len(plants) == 1 and len(country) != 1) or (len(plants) != 1 and len(country) == 1):
            print("Received bad data 1")
        elif len(plants) == 1 and len(country) == 1 and len(hectares) == 1:
            print("One prediction requested")
            plant = plants[0]
            country = country[0]
            avg_temperature = avg_temperature[0]
            avg_rainfall = avg_rainfall[0]
            hectares = hectares[0]

            print("FIRST UNIQUE PREDICTION")
            display_result_and_add_to_db(plant, country, avg_temperature, avg_rainfall, hectares)


        else:
            if len(plants) != 3 or len(country) != 3:
                print("Received bad data 3")
            else:
                print("Three predictions requested")
                display_result_and_add_to_db(plants[0], country[0], avg_temperature[0], avg_rainfall[0], hectares[0])
                display_result_and_add_to_db(plants[1], country[1], avg_temperature[1], avg_rainfall[1], hectares[1])
                display_result_and_add_to_db(plants[2], country[2], avg_temperature[2], avg_rainfall[2], hectares[2])

    else:
        st.write("No data found in session state.")



