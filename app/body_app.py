import streamlit as st
import geocoder
from geopy.geocoders import Nominatim

def get_city():
    g = geocoder.ip("me")
    if g.ok:
        lat, lon = g.latlng
        st.success(f"Your position is: Lat {lat}, Lon {lon}")
        st.map(data={"lat": [lat], "lon": [lon]}, zoom=10)
        geolocator = Nominatim(user_agent="my_geopy_app")
        location = geolocator.reverse(f"{lat},{lon}")

        print(location)
        address = location.raw['address']
        print(address)
        country = address.get('country', '')
        st.write("You are in the following Country: ", country)


def cultivation_page():
    st.title("Cultivation page")
    st.header("Choose an option")
    options = ["Option 1", "Option 2", "Option 3"]
    choice = st.selectbox("Choose an option:", options)
    if st.button("Go"):
        st.write(f"You chose: {choice}")
        st.write(f"Getting position...")
        get_city()
    st.caption("Developed to help farmers improve productivity!")
