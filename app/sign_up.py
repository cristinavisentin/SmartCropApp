import streamlit as st
from db_utils import create_user
from sign_in import save_cookies
from sign_in import show_cookies

def sign_up_page():
    show_cookies()
    st.title("Sign Up")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    if st.button("Sign Up"):
        if create_user(username, password):
            save_cookies(username, password)
            st.success("Successful registration! Back to login page")
            st.session_state["page"] = "login"
            st.rerun()
        else:
            st.error("Error: username already exists. Choose another username")
    if st.button("Already have an account? Go to Login"):
        st.session_state["page"] = "login"
        st.rerun()



