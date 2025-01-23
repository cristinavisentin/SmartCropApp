import streamlit as st

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
            print("plant: ", plant, "country: ", country)
            st.write("FIRST UNIQUE PREDICTION")
            st.write("plant: ", plant, "country: ", country)
            print("avg_rainfall: ", avg_rainfall, "mm, avg_temperature: ", avg_temperature, "C")
            st.write("avg_rainfall: ", avg_rainfall, "mm, avg_temperature: ", avg_temperature, "C")



        else:
            if len(plants) != 3 or len(country) != 3:
                print("Received bad data 3")
            else:
                print("Three predictions requested")
                first_plant = plants[0]
                first_country = country[0]
                first_avg_temperature = avg_temperature[0]
                first_avg_rainfall = avg_rainfall[0]
                print("FIRST PREDICTION")
                print("plant: ", first_plant, "country: ", first_country)
                st.write("FIRST PREDICTION")
                st.write("plant: ", first_plant, "country: ", first_country)
                print("avg_rainfall: ", first_avg_rainfall, "mm, avg_temperature: ", first_avg_temperature, "C")
                st.write("avg_rainfall: ", first_avg_rainfall, "mm, avg_temperature: ", first_avg_temperature, "C")

                second_plant = plants[1]
                second_country = country[1]
                second_avg_temperature = avg_temperature[1]
                second_avg_rainfall = avg_rainfall[1]
                print("SECOND PREDICTION")
                st.write("SECOND PREDICTION")
                print("plant: ", second_plant, "country: ", second_country)
                st.write("plant: ", second_plant, "country: ", second_country)
                print("avg_rainfall: ", second_avg_rainfall, "mm, avg_temperature: ", second_avg_temperature, "C")
                st.write("avg_rainfall: ", second_avg_rainfall, "mm, avg_temperature: ", second_avg_temperature, "C")

                third_plant = plants[2]
                third_country = country[2]
                third_avg_temperature = avg_temperature[2]
                third_avg_rainfall = avg_rainfall[2]
                print("THIRD PREDICTION")
                st.write("THIRD PREDICTION")
                print("plant: ", third_plant, "country: ", third_country)
                st.write("plant: ", third_plant, "country: ", third_country)
                print("avg_rainfall: ", third_avg_rainfall, "mm, avg_temperature: ", third_avg_temperature, "C")
                st.write("avg_rainfall: ", third_avg_rainfall, "mm, avg_temperature: ", third_avg_temperature, "C")


    else:
        st.write("No data found in session state.")