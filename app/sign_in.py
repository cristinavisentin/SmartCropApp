import streamlit as st
from db_utils import check_user_credentials

def sign_in_page():
    st.title("Sign in")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign In"):
        if check_user_credentials(username, password):
            st.success(f"Welcome, {username}!")
            st.session_state["page"] = "cultivation"
            st.rerun()
        else:
            st.error("Invalid credentials. Retry")
    if st.button("Don't have an account? Register"):
        st.session_state["page"] = "sign_up"
        st.rerun()
