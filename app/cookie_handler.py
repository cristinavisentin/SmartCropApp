import streamlit as st
from db_utils import generate_token
from streamlit_cookies_controller import CookieController
import time
import auth

controller = CookieController(key='AgricultureAuth')

def get_cookies():
    #controller.refresh()  # IMPORTANT: Refresh the cookie cache located in streamlit session state with the actual browser cache
    time.sleep(1)
    token_auth = controller.get('AgricultureAuth_Token')
    if token_auth:
       print("Token found:", token_auth)
       return token_auth
    else:
       print("Token not found")
       return ""


def show_cookies():
    cookies = controller.getAll()
    time.sleep(1)
    print("show_cookies: ", cookies)

def save_cookies(username):
    controller.set("AgricultureAuth_Token", generate_token(username), max_age=7*86400)

def logout():
    controller.set("AgricultureAuth_Token", "", max_age=0)
    auth.is_logged_in = False
    st.write("You are correctly logged out")
    st.session_state["page"] = "sign_in"