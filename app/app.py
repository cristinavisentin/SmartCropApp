import streamlit as st

st.set_page_config(
    page_title="CropML",
    page_icon="🌱",
)

from auth import sign_in_page, sign_up_page, validate_token, logout, get_username
from body_app import single_prediction_page, multiple_prediction_page
from menu_pages.home_page import homepage
from menu_pages.user_data import user_data_page
from menu_pages.privacy_policy import privacy_policy_page
from menu_pages.vision import vision_page
from prediction_result import prediction_result_page
from streamlit_cookies_controller import CookieController

controller = CookieController()
token = controller.get("SmartCrop_auth_token")

if "authenticated" not in st.session_state: # first open or refresh
    st.session_state["authenticated"] = False
    st.session_state["valid_token_decoded"] = False
    st.session_state["username"] = None
    st.session_state["page"] = "sign_in"
    print("first open or refresh")


if validate_token(token):
        st.session_state["valid_token_decoded"] = True

if not st.session_state["authenticated"] and st.session_state["valid_token_decoded"]: # first open or refresh AND VALID TOKEN
        st.session_state["authenticated"] = True
        st.session_state["username"] = get_username(token)
        st.session_state["page"] = "homepage"
        print("first open or refresh AND VALID TOKEN: ", token)


def render_sidebar():
    if st.session_state["authenticated"]:
        st.sidebar.title(f"Welcome back {st.session_state['username']}!")
        if st.sidebar.button("Process data"):
            st.session_state["page"] = "crop_application_single_prediction"
        if st.sidebar.button("My data"):
            st.session_state["page"] = "data"
        if st.sidebar.button("What is this app?"):
            st.session_state["page"] = "homepage"
        if st.sidebar.button("Privacy policy"):
            st.session_state["page"] = "privacy_policy"
        if st.sidebar.button("Our vision"):
            st.session_state["page"] = "vision"
        if st.sidebar.button("Log Out"):
            logout()
            st.session_state["authenticated"] = False
            st.session_state["username"] = None
            st.session_state["page"] = "sign_in"
            st.rerun()
    else:
        st.sidebar.title("Menu")
        if st.sidebar.button("Log In"):
            st.session_state["page"] = "sign_in"
        if st.sidebar.button("Don't have an account?"):
            st.session_state["page"] = "sign_up"
        if st.sidebar.button("What is this app?"):
            st.session_state["page"] = "homepage"
        if st.sidebar.button("Privacy policy"):
            st.session_state["page"] = "privacy_policy"
        if st.sidebar.button("Our vision"):
            st.session_state["page"] = "vision"

render_sidebar()


def show_page():
    page = st.session_state["page"]
    if page == "sign_in":
        sign_in_page()
    elif page == "sign_up":
        sign_up_page()
    elif page == "crop_application_single_prediction":
        single_prediction_page()
    elif page == "crop_application_multiple_prediction":
        multiple_prediction_page()
    elif page == "prediction_result":
        prediction_result_page()
    elif page == "data":
        user_data_page()
    elif page == "homepage":
        homepage()
    elif page == "privacy_policy":
        privacy_policy_page()
    elif page == "vision":
        vision_page()

show_page()
