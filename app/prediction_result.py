import streamlit as st
import pickle

import os
base_dir = os.path.dirname(os.path.abspath(__file__))
encoder_path = os.path.join(base_dir, '../artifacts/encoder.pkl')

with open(os.path.join(base_dir, '../artifacts/encoder.pkl'), 'rb') as file:
    encoder = pickle.load(file)
with open(os.path.join(base_dir, '../artifacts/scaler.pkl'), 'rb') as file:
    scaler = pickle.load(file)
with open(os.path.join(base_dir, '../artifacts/model.pkl'), 'rb') as file:
    model = pickle.load(file)


def get_prediction(plant, country, avg_temperature, avg_rainfall):
    encoded = encoder.transform([['Wheat', 'Italy']])
    other_vals = [[2025, 0.3, 4.5]]

    other_vals[0].extend(encoded[0])
    to_predict = scaler.transform(other_vals)

    print("modello ottenuto in get_prediction(): ", model.predict(to_predict))
    return 1

def display_result(plant, country, avg_temperature, avg_rainfall):
    print("plant: ", plant, "country: ", country)
    st.write("plant: ", plant, "country: ", country)
    print("avg_rainfall: ", avg_rainfall, "mm, avg_temperature: ", avg_temperature, "C")
    st.write("avg_rainfall: ", avg_rainfall, "mm, avg_temperature: ", avg_temperature, "C")
    predit = get_prediction(plant, country, avg_temperature, avg_rainfall)
    print("predit: ", predit, "etti/ettaro")
    st.write("predit: ", predit, "etti/ettaro")


def prediction_result_page():
    st.title("Prediction Result")
    st.write("For now, these are the data that the user entered, and the data that were retrieved through external weather services")

    if "plant" in st.session_state and "country" in st.session_state:
        plants = st.session_state["plant"]
        country = st.session_state["country"]
        avg_temperature = st.session_state["avg_temperature"]
        avg_rainfall = st.session_state["avg_rainfall"]

        print("plants: ", plants)

        if len(plants) == 1 and len(country) != 1:
            print("Received bad data 1")
        elif len(plants) != 1 and len(country) == 1:
            print("Received bad data 2")
        elif len(plants) == 1 and len(country) == 1:
            print("One prediction requested")
            plant = plants[0]
            country = country[0]
            avg_temperature = avg_temperature[0]
            avg_rainfall = avg_rainfall[0]

            print("FIRST UNIQUE PREDICTION")
            display_result(plant, country, avg_temperature, avg_rainfall)


        else:
            if len(plants) != 3 or len(country) != 3:
                print("Received bad data 3")
            else:
                print("Three predictions requested")
                first_plant = plants[0]
                first_country = country[0]
                first_avg_temperature = avg_temperature[0]
                first_avg_rainfall = avg_rainfall[0]

                display_result(first_plant, first_country, first_avg_temperature, first_avg_rainfall)

                second_plant = plants[1]
                second_country = country[1]
                second_avg_temperature = avg_temperature[1]
                second_avg_rainfall = avg_rainfall[1]

                display_result(second_plant, second_country, second_avg_temperature, second_avg_rainfall)

                third_plant = plants[2]
                third_country = country[2]
                third_avg_temperature = avg_temperature[2]
                third_avg_rainfall = avg_rainfall[2]

                display_result(third_plant, third_country, third_avg_temperature, third_avg_rainfall)

    else:
        st.write("No data found in session state.")



