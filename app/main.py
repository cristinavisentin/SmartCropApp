import streamlit as st
st.set_page_config(
    page_title="CropML",
    page_icon="🌱",
)

from auth import sign_in_page, sign_up_page, is_logged_in
from body_app import cultivation_page
from cookie_handler import get_cookies, show_cookies, logout
from db_utils import validate_token, user_name
from menu_pages.info import info_page
from menu_pages.user_data import user_data_page


is_auth = validate_token(get_cookies())
print("Welcome back ", user_name)

if is_auth or is_logged_in:
    dynamic_title = f"Welcome back, {user_name}!"
    st.sidebar.title(dynamic_title)
    print("2 Welcome back ", user_name)
    if st.sidebar.button("Process data") and st.session_state["page"] != "cultivation":
        st.session_state["page"] = "cultivation"
        st.rerun()
else:
    st.sidebar.title("Menu")
    if st.sidebar.button("Log In"):
        st.session_state["page"] = "sign_in"
        st.rerun()

if st.sidebar.button("What is this app?") and st.session_state["page"] != "info":
    st.session_state["page"] = "info"
    info_page()
if is_auth or is_logged_in:
    if st.sidebar.button("My data") and st.session_state["page"] != "data":
        st.session_state["page"] = "data"
        st.rerun()

    if st.sidebar.button("Log Out"):
        logout()
        st.rerun()

if "page" not in st.session_state:
    if is_auth:
        st.session_state["page"] = "cultivation"
        if st.sidebar.button("Log out"):
            logout()
    else:
        st.session_state["page"] = "sign_in"
if st.session_state["page"] == "sign_in":
    sign_in_page()
elif st.session_state["page"] == "sign_up":
    sign_up_page()
elif st.session_state["page"] == "cultivation":
    cultivation_page()
elif st.session_state["page"] == "data":
    user_data_page()




