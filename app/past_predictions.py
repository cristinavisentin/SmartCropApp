import streamlit as st
import pandas as pd
from db_utils import get_predictions_by_username

def user_data_page():
    st.title("These are your predictions")

    if "username" in st.session_state and st.session_state.get("username") is not None:
        results = get_predictions_by_username(st.session_state["username"])
        if results:
            df = pd.DataFrame(results, columns=["Plant", "Country", "Hectares", "Prediction (quintals)"])
            st.table(df.style.format({"Prediction (quintals)": "{:.2f}"}))
        else:
            st.warning("No predictions found, make one!")
    else:
        st.warning("there is no user logged in yet")
