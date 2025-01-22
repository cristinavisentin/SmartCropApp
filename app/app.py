import streamlit as st

st.set_page_config(
    page_title="CropML",
    page_icon="🌱",
)

from auth import sign_in_page, sign_up_page
from body_app import cultivation_page
from cookie_handler import validate_token, logout, get_persistent_session_auth_token, get_username
from menu_pages.home_page import homepage
from menu_pages.user_data import user_data_page
from menu_pages.privacy_policy import privacy_policy_page
from menu_pages.vision import vision_page

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.session_state["page"] = "sign_in"
    print("SESSION STATE NEL PRIMO IF: ", st.session_state["authenticated"])

    if not st.session_state["authenticated"] and validate_token(get_persistent_session_auth_token()):
        st.session_state["authenticated"] = True
        st.session_state["username"] = get_username(get_persistent_session_auth_token())
        st.session_state["page"] = "homepage"
        print("SESSION STATE NEL SECONDO IF: ", st.session_state["authenticated"])


def render_sidebar():
    if st.session_state["authenticated"]:
        st.sidebar.title(f"Welcome back {st.session_state['username']}!")
        if st.sidebar.button("Process data"):
            st.session_state["page"] = "crop_application"
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
    elif page == "crop_application":
        cultivation_page()
    elif page == "data":
        user_data_page()
    elif page == "homepage":
        homepage()
    elif page == "privacy_policy":
        privacy_policy_page()
    elif page == "vision":
        vision_page()

show_page()
