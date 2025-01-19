import streamlit as st
st.set_page_config(
    page_title="CropML",
    page_icon="🌱",
    layout="wide",
)

from auth import sign_in_page, sign_up_page
from body_app import cultivation_page
from cookie_handler import get_cookies, show_cookies
from db_utils import validate_token

if "page" not in st.session_state:
    if validate_token(get_cookies()):
        st.session_state["page"] = "cultivation"
    else:
        st.session_state["page"] = "sign_in"
if st.session_state["page"] == "sign_in":
    sign_in_page()
elif st.session_state["page"] == "sign_up":
    sign_up_page()
elif st.session_state["page"] == "cultivation":
    cultivation_page()
