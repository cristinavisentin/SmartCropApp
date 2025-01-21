import streamlit as st
import time
import db_utils
import uuid
from cookie_handler import save_persistent_session_auth_token
def get_session_id():
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = str(uuid.uuid4())
    return st.session_state["session_id"]

def sign_in_page():
    st.title("Sign in")
    session_id = get_session_id()
    st.session_state["session_id_" + session_id] = session_id

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    remember = st.checkbox("Do you want to stay logged in?")
    if st.button("Sign In"):
        result = db_utils.check_and_mem_user_credentials(username, password)
        if result:
            if remember:
                save_persistent_session_auth_token(username)
            st.session_state["authenticated"] = True
            st.session_state["username"] = username

            st.success(f"Welcome, {username}!")
            time.sleep(0.5)
            st.session_state["page"] = "crop_application"
            st.rerun()
        else:
            st.error("Invalid credentials. Retry")
    if st.button("Don't have an account? Register"):
        st.session_state["page"] = "sign_up"
        time.sleep(0.5)
        st.rerun()

def sign_up_page():
    st.title("Sign Up")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    if st.button("Sign Up"):
        if db_utils.create_user(username, password):
            st.success("Successful registration! Back to login page")
            st.session_state["page"] = "sign_in"
            st.rerun()
        else:
            st.error("Error: username already exists. Choose another username")
    if st.button("Already have an account? Go to Login"):
        st.session_state["page"] = "sign_in"
        time.sleep(0.5)
        st.rerun()

