import streamlit as st
import time
import db_utils
import uuid
import datetime
import jwt
from streamlit_cookies_controller import CookieController

controller = CookieController()
SECRET_KEY = "123"

def logout():
    try:
        controller.remove("SmartCrop_auth_token")
    except Exception:
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.write("You are correctly logged out")
        st.session_state["page"] = "sign_in"


def generate_token(username):
    expiration_time = datetime.datetime.now() + datetime.timedelta(days=1)
    payload = {
        "username": username,
        "exp": expiration_time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def validate_token(token):
    if token is None:
        return False
    from db_utils import check_username_in_db
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("username")
        print("username CORRECTLY DECODED in validate_token: ", username)
        if not username:
            print("Token payload missing 'username'")
            return False
        if check_username_in_db(username):
            return True
        print("Session ID or User ID not found in database")
        return False
    except jwt.ExpiredSignatureError:
        print("The token is expired")
        return False
    except jwt.InvalidTokenError:
        print("Token not valid during token validation")
        return False




def get_username(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("username")
        if not username:
            print("Invalid token: 'user_id' not found")
            return ""
        print("username found in get_username: ", username)
        if username:
            return username
    except jwt.ExpiredSignatureError:
        print("Error: Token has expired")
        return ""
    except jwt.InvalidTokenError:
        print("Error: Invalid token")
        return ""
    except Exception as e:
        print("Unexpected error:", e)
        return ""





def save_persistent_session_auth_token(username):
    controller.set("SmartCrop_auth_token", generate_token(username), max_age=7*86400, secure=True)

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
        result, error_message = db_utils.check_user_credentials(username, password)
        if error_message:
            st.error("There is a problem with the database. We apologize for the inconvenience, please try again later")
        else:
            if result:
                if remember:
                    save_persistent_session_auth_token(username)
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.success(f"Welcome, {username}!")
                time.sleep(0.5)
                st.session_state["page"] = "homepage"
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
        result, error_message = db_utils.create_user(username, password)
        if error_message:
            st.error("There is a problem with the database. We apologize for the inconvenience, please try again later")
        else:
            if result:
                st.success("Successful registration! Back to login page")
                st.session_state["page"] = "sign_in"
                st.rerun()
            else:
                st.error("Error: username already exists. Choose another username")
    if st.button("Already have an account? Go to Login"):
        st.session_state["page"] = "sign_in"
        time.sleep(0.5)
        st.rerun()

