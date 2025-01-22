import streamlit as st
from streamlit_cookies_controller import CookieController
import datetime
import jwt

controller = CookieController()

SECRET_KEY = "123"


def get_persistent_session_auth_token():
    token_auth = controller.get("SmartCrop_auth_token")
    if token_auth:
        return token_auth
    else:
        return ""


def save_persistent_session_auth_token(username):
    controller.set("SmartCrop_auth_token", generate_token(username), max_age=7*86400, secure=True)


def logout():
    try:
        controller.remove("SmartCrop_auth_token")
    except Exception:
        pass
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

