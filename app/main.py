import streamlit as st
st.set_page_config(
    page_title="CropML",
    page_icon="🌱",
)

from auth import sign_in_page, sign_up_page
from body_app import cultivation_page
from cookie_handler import validate_token, logout, get_cookie, get_persistent_session_auth_token, get_username
from menu_pages.info import info_page
from menu_pages.user_data import user_data_page

is_persistent_session = False

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["username"] = None

if not st.session_state["authenticated"]:
    is_persistent_session = validate_token(get_persistent_session_auth_token())
    if is_persistent_session:
        st.session_state["username"] = get_username(get_cookie())

is_auth = is_persistent_session or st.session_state["authenticated"]

if is_auth:
    dynamic_title = f"Welcome back {st.session_state["username"]}!"
    st.sidebar.title(dynamic_title)
    st.sidebar.title("Welcome")
    print("2 Welcome back ", st.session_state["username"])
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
if is_auth:
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




