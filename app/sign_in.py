import streamlit as st
from db_utils import check_user_credentials
from streamlit_cookies_controller import CookieController
import time

controller = CookieController(key='AgricultureAuth')


def sign_in_page():
    show_cookies()
    st.title("Sign in")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign In"):
        if check_user_credentials(username, password):
            save_cookies(username, password)
            st.success(f"Welcome, {username}!")
            st.session_state["page"] = "cultivation"
            st.rerun()
        else:
            st.error("Invalid credentials. Retry")
    if st.button("Don't have an account? Register"):
        st.session_state["page"] = "sign_up"
        st.rerun()


def save_cookies(username, password):
    controller.set("AgricultureAuth_username", username)
    controller.set("AgricultureAuth_password", password)
    cookies = controller.getAll()
    time.sleep(1)  # Aggiunge un leggero ritardo
    st.write("Cookie aggiornati:", cookies)

def show_cookies():
    cookies = controller.getAll()
    time.sleep(1)  # Aggiunge un leggero ritardo
    st.write("Cookie inizialmente trovati:", cookies)


