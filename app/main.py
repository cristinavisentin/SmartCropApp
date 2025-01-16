import streamlit as st
from sign_in import sign_in_page
from sign_up import sign_up_page
from body_app import cultivation_page

st.set_page_config(
    page_title="CropML",
    page_icon="🌱",
    layout="wide",
)

if "page" not in st.session_state:
    st.session_state["page"] = "login"
if st.session_state["page"] == "login":
    sign_in_page()
elif st.session_state["page"] == "sign_up":
    sign_up_page()
elif st.session_state["page"] == "cultivation":
    cultivation_page()
