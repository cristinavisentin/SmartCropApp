import streamlit as st
import geocoder
from geopy.geocoders import Nominatim
import time
from climate_data import get_climate_data

plant_options = ["Rice", "Cassava", "Maize", "Plantains", "Potatoes", "Sorghum", "Soybeans", "Sweet potatoes", "Potatoes",
           "Wheat", "Yams"]

country_options = [
    "Albania", "Algeria", "Angola", "Area", "Argentina", "Armenia",
    "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain",
    "Bangladesh", "Belarus", "Belgium", "Botswana", "Brazil",
    "Bulgaria", "Burkina Faso", "Burundi", "Cameroon", "Canada",
    "Central African Republic", "Chile", "Colombia", "Croatia",
    "Denmark", "Dominican Republic", "Ecuador", "Egypt", "El Salvador",
    "Eritrea", "Estonia", "Finland", "France", "Germany", "Ghana",
    "Greece", "Guatemala", "Guinea", "Guyana", "Haiti", "Honduras",
    "Hungary", "India", "Indonesia", "Iraq", "Ireland", "Italy",
    "Jamaica", "Japan", "Kazakhstan", "Kenya", "Latvia", "Lebanon",
    "Lesotho", "Libya", "Lithuania", "Madagascar", "Malawi", "Malaysia",
    "Mali", "Mauritania", "Mauritius", "Mexico", "Montenegro",
    "Morocco", "Mozambique", "Namibia", "Nepal", "Netherlands",
    "New Zealand", "Nicaragua", "Niger", "Norway", "Pakistan",
    "Papua New Guinea", "Peru", "Poland", "Portugal", "Qatar",
    "Romania", "Rwanda", "Saudi Arabia", "Senegal", "Slovenia",
    "South Africa", "Spain", "Sri Lanka", "Sudan", "Suriname",
    "Sweden", "Switzerland", "Tajikistan", "Thailand", "Tunisia",
    "Turkey", "Uganda", "Ukraine", "United Kingdom", "Uruguay",
    "Zambia", "Zimbabwe"
]


def get_coordinates_from_country(country_name):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(country_name, timeout=5)

    if not location:
        raise ValueError(f"Unable to find coordinates for country: {country_name}")
    return location.latitude, location.longitude

def get_country_from_coordinates(latitude, longitude):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    if location and "country" in location.raw["address"]:
        return location.raw["address"]["country"]
    else:
        raise ValueError("Unable to determine the country from the provided coordinates.")


def get_geolocation():
    st.write(f"Getting position...")
    g = geocoder.ip("me")
    if g.ok:
        lat, lon = g.latlng
        st.success(f"Your position is: Lat {lat}, Lon {lon}")
        print("country got from geolocation: ", lat, lon)
        return lat, lon
    return None


def multiple_prediction_page():
    st.title("Comparison")
    col1, col2, col3 = st.columns(3)

    with col1:
        acres1 = st.number_input("Number of acres", min_value=1, max_value=1000, value=1, key = "acres1")
        chosen_plant1 = st.selectbox("Select the plant:", plant_options, key="plant1")
        chosen_country1 = st.selectbox("Select the Country:", country_options, key="country1")

    with col2:
        acres2 = st.number_input("Number of acres", min_value=1, max_value=1000, value=1, key = "acres2")
        chosen_plant2 = st.selectbox("Select the plant:", plant_options, key="plant2")
        chosen_country2 = st.selectbox("Select the Country:", country_options, key="country2")

    with col3:
        acres3 = st.number_input("Number of acres", min_value=1, max_value=1000, value=1, key = "acres3")
        chosen_plant3 = st.selectbox("Select the plant:", plant_options, key="plant3")
        chosen_country3 = st.selectbox("Select the Country:", country_options, key="country3")

    if st.button("Go to prediction"):
        co11, co12 = get_coordinates_from_country(chosen_country1)
        time.sleep(2)
        avg_temperature1, avg_rainfall1 = get_climate_data(co11, co12)
        print("avg_temperature1: ", avg_temperature1, " avg_rainfall1: ", avg_rainfall1)
        co21, co22 = get_coordinates_from_country(chosen_country2)
        time.sleep(2)
        avg_temperature2, avg_rainfall2 = get_climate_data(co21, co22)
        print("avg_temperature2: ", avg_temperature2, " avg_rainfall2: ", avg_rainfall2)
        co31, co32 = get_coordinates_from_country(chosen_country3)
        time.sleep(1)
        avg_temperature3, avg_rainfall3 = get_climate_data(co31, co32)
        print("avg_temperature3: ", avg_temperature3, " avg_rainfall3: ", avg_rainfall3)


        st.session_state["plant"] = [chosen_plant1, chosen_plant2, chosen_plant3]
        st.session_state["acres_to_cultivate"] = [acres1, acres2, acres3]
        st.session_state["country"] = [chosen_country1, chosen_country2, chosen_country3]
        st.session_state["avg_temperature"] = [avg_temperature1, avg_temperature2, avg_temperature3]
        st.session_state["avg_rainfall"] = [avg_rainfall1, avg_rainfall2, avg_rainfall3]
        st.session_state["page"] = "prediction_result"
        st.rerun()

    if st.button("Go back and make a unique prediction"):
        st.session_state["page"] = "crop_application_single_prediction"
        st.rerun()



def single_prediction_page():
    st.title("Cultivation page")
    st.header("Choose an option")

    chosen_plant = st.selectbox("Select which plant you want to grow:", plant_options)
    acres_quantity = st.number_input("In how many acres of land do you want to grow this plant?", min_value=1, max_value=1000, value=1, key = "acres")
    print(f"The number of  acres is: {acres_quantity}")
    st.session_state["acres_to_cultivate"] = [acres_quantity]

    st.write("You can select your country in two ways...")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("get geolocation and go to prediction"):
            co1, co2 = get_geolocation()
            time.sleep(2)
            avg_temperature, avg_rainfall = get_climate_data(co1, co2)
            print("avg_temperature: ", avg_temperature, " avg_rainfall: ", avg_rainfall)
            time.sleep(1)
            st.session_state["plant"] = [chosen_plant]
            st.session_state["country"] = [get_country_from_coordinates(co1, co2)]
            st.session_state["avg_temperature"] = [avg_temperature]
            st.session_state["avg_rainfall"] = [avg_rainfall]

            st.session_state["page"] = "prediction_result"

            st.rerun()
    with col2:
        chosen_country = st.selectbox("Select your Country:", country_options)
        if st.button("Go to prediction"):
            co1, co2 = get_coordinates_from_country(chosen_country)
            time.sleep(2)
            avg_temperature, avg_rainfall = get_climate_data(co1, co2)
            print("avg_temperature: ", avg_temperature, " avg_rainfall: ", avg_rainfall)
            time.sleep(1)
            st.session_state["plant"] = [chosen_plant]
            st.session_state["country"] = [chosen_country]
            st.session_state["avg_temperature"] = [avg_temperature]
            st.session_state["avg_rainfall"] = [avg_rainfall]

            st.session_state["page"] = "prediction_result"
            time.sleep(3)
            st.rerun()

    if st.button("Compare multiple predictions"):
        st.session_state["page"] = "crop_application_multiple_prediction"
        st.rerun()


    st.caption("Developed to help farmers improve productivity!")
