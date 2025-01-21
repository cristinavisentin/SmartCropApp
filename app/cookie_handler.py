import streamlit as st
from streamlit_cookies_controller import CookieController
import time
import datetime
import jwt

controller = CookieController()

SECRET_KEY = "123"

def get_token_with_prefix(prefix):
    cookies = controller.getAll()
    time.sleep(0.5)
    print("all cookies:", cookies)
    for name, value in cookies.items():
        if name.startswith(prefix):
            return value
    return None

def get_persistent_session_auth_token():
    cookie_name = get_token_with_prefix("SmartCrop_auth_token")
    token_auth = controller.get(cookie_name)
    if token_auth:
        print("Token found for session:", token_auth)
        return token_auth
    else:
        return ""


def save_persistent_session_auth_token(user_id, session_id):
    controller.set("SmartCrop_auth_token" + session_id, generate_token(user_id, session_id), max_age=7*86400, path="/", secure=True)


def logout():
    controller.set("SmartCrop_auth_token", "", max_age=7*86400, path="/", secure=True)

    st.session_state["authenticated"] = False
    st.session_state["username"] = None

    st.write("You are correctly logged out")
    st.session_state["page"] = "sign_in"


def generate_token(user_id, session_id):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    payload = {
        "user_id": user_id,
        "session_id": session_id,
        "exp": expiration_time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def validate_token(token):
    from db_utils import check_id_in_db
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        session_id = payload.get("session_id")
        print("SESSION ID CORRECTLY DECODED: ", session_id)
        if not user_id or not session_id:
            print("Token payload missing 'user_id' or 'session_id'")
            return False
        print(f"User ID: {user_id}, Session ID: {session_id} in validate_token")

        print("CONTROLLO SE SESSION ID è già in uso")



        if check_id_in_db(user_id, session_id):
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
        user_id = payload.get("user_id")
        if not user_id:
            print("Invalid token: 'user_id' not found")
            return ""

        print("user_id found in get_username: ", user_id)

        from db_utils import get_username_from_db
        username = get_username_from_db(user_id)
        if username:
            return username
        else:
            print(f"No username found in DB for user_id: {user_id}")
            return ""
    except jwt.ExpiredSignatureError:
        print("Error: Token has expired")
        return ""
    except jwt.InvalidTokenError:
        print("Error: Invalid token")
        return ""
    except Exception as e:
        print("Unexpected error:", e)
        return ""

