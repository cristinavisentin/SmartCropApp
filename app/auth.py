import streamlit as st
import time
from db_utils import check_user_credentials, create_user
from cookie_handler import show_cookies, save_cookies

def sign_in_page():
    print("cookie founded in sign_in_page: ")
    show_cookies()
    st.title("Sign in")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign In"):
        if check_user_credentials(username, password):
            save_cookies(username)
            st.session_state["user_id"] = username
            st.success(f"Welcome, {username}!")
            time.sleep(0.5)
            st.session_state["page"] = "cultivation"
            st.rerun()
        else:
            st.error("Invalid credentials. Retry")
    if st.button("Don't have an account? Register"):
        st.session_state["page"] = "sign_up"
        time.sleep(0.5)
        st.rerun()

def sign_up_page():
    print("cookie trovati in sign_up page: ")
    show_cookies()
    st.title("Sign Up")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    if st.button("Sign Up"):
        if create_user(username, password):
            save_cookies(username)
            st.success("Successful registration! Back to login page")
            st.session_state["page"] = "sign_in"
            st.rerun()
        else:
            st.error("Error: username already exists. Choose another username")
    if st.button("Already have an account? Go to Login"):
        st.session_state["page"] = "sign_in"
        time.sleep(0.5)
        st.rerun()
