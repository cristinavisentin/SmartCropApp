import streamlit as st
import time
import db_utils
import datetime
import jwt
from streamlit_cookies_controller import CookieController
from db_utils import check_username_in_db

controller = CookieController()
SECRET_KEY = "123"

def logout():
    try:
        controller.remove("SmartCrop_auth_token")
        time.sleep(1)
        controller.refresh()
        st.session_state.update({
            "authenticated": False,
            "username": None,
            "valid_token_decoded": False,
            "page": "sign_in"
        })
    except KeyError as e:
        print("Failed to remove authentication token: %s", e)
    except Exception as e:
        print("An unexpected error occurred during logout: %s", e)


def generate_token(username):
    expiration_time = datetime.datetime.now() + datetime.timedelta(days=1)
    payload = {
        "username": username,
        "exp": expiration_time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def validate_token():
    try:
        controller.refresh()
        time.sleep(1)
        token = controller.get("SmartCrop_auth_token")
        print("Token found: %s", token)

        if token is None:
            return False
    except KeyError as e:
        print("Error accessing authentication token: %s", e)
        return False
    except Exception as e:
        print("Unexpected error during token retrieval: %s", e)
        return False
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("username")
        st.session_state["username"] = username
        if not username:
            print("Token payload is missing the 'username' field.")
            return False
        if check_username_in_db(username):
            return True
        else:
            print("User '%s' not found in the database.", username)
            return False
    except jwt.ExpiredSignatureError:
        print("The token has expired.")
        return False
    except jwt.InvalidTokenError:
        print("The token is invalid.")
        return False
    except Exception as e:
        print("Unexpected error during token validation: %s", e)
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
    try:
        token = generate_token(username)
        controller.set("SmartCrop_auth_token", token, max_age=7 * 86400, secure=True)
        print("Authentication token successfully saved for user '%s'.", username)
    except ValueError as e:
        print("Invalid token for username '%s': %s", username, e)
    except Exception as e:
        print("An unexpected error occurred while saving the authentication token: %s", e)



def sign_in_page():
    st.title("Sign in")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    remember = st.checkbox("Do you want to stay logged in?")
    if st.button("Sign In", key=100):
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
    if st.button("Sign Up", key=101):
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

