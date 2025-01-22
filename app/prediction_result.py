import streamlit as st
from climate_data import get_climate_data

def prediction_result_page():
    st.title("Prediction Result")
    st.write("For now, these are the data that the user entered, and the data that were retrieved through external weather services")

    if "plant" in st.session_state and "location" in st.session_state:
        plants = st.session_state["plant"]
        locations = st.session_state["location"]

        print("plants: ", plants, "len: ", len(plants))
        print("locations: ", locations, "len: ", len(locations))

        if len(plants) == 1 and len(locations) != 1:
            print("Received bad data 1")
        elif len(plants) != 1 and len(locations) == 1:
            print("Received bad data 1")
        elif len(plants) == 1 and len(locations) == 1:
            print("One prediction requested")
            plant = plants[0]
            co1, co2 = locations[0]
            print("plant: ", plant, "co1: ", co1, "co2: ", co2)
            st.write("plant: ", plant, "co1: ", co1, "co2: ", co2)
            avg_temperature, avg_rainfall = get_climate_data(co1, co2)
            print("avg_rainfall: ", avg_rainfall, "avg_temperature: ", avg_temperature)
            st.write("avg_rainfall: ", avg_rainfall, "avg_temperature: ", avg_temperature)



        else:
            if len(plants) != 3 or len(locations) != 3:
                print("Received bad data 2")
            else:
                print("Three predictions requested")
                plant = plants[0]
                co1, co2 = locations[0]
                print("First prediction data: plant: ", plant, "co1: ", co1, "co2: ", co2)
                st.write("First prediction data: plant: ", plant, "co1: ", co1, "co2: ", co2)
                avg_temperature, avg_rainfall = get_climate_data(co1, co2)
                print("avg_rainfall: ", avg_rainfall, "avg_temperature: ", avg_temperature)
                st.write("avg_rainfall: ", avg_rainfall, "avg_temperature: ", avg_temperature)

                plant = plants[1]
                co1, co2 = locations[1]
                print("Second prediction data: plant: ", plant, "co1: ", co1, "co2: ", co2)
                st.write("First prediction data: plant: ", plant, "co1: ", co1, "co2: ", co2)
                avg_temperature, avg_rainfall = get_climate_data(co1, co2)
                print("avg_rainfall: ", avg_rainfall, "avg_temperature: ", avg_temperature)
                st.write("avg_rainfall: ", avg_rainfall, "avg_temperature: ", avg_temperature)

                plant = plants[2]
                co1, co2 = locations[2]
                print("Third prediction data: plant: ", plant, "co1: ", co1, "co2: ", co2)
                st.write("First prediction data: plant: ", plant, "co1: ", co1, "co2: ", co2)
                avg_temperature, avg_rainfall = get_climate_data(co1, co2)
                print("avg_rainfall: ", avg_rainfall, "avg_temperature: ", avg_temperature)
                st.write("avg_rainfall: ", avg_rainfall, "avg_temperature: ", avg_temperature)


    else:
        st.write("No data found in session state.")