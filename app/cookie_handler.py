import streamlit as st
from streamlit_cookies_controller import CookieController
import time
import datetime
import jwt

controller = CookieController(key='AgricultureAuth')
SECRET_KEY = "123"


def get_persistent_session_auth_token():
    #controller.refresh()  # IMPORTANT: Refresh the cookie cache located in streamlit session state with the actual browser cache
    time.sleep(1)
    token_auth = controller.get('SmartCrop_auth_token')
    if token_auth:
       print("Token found:", token_auth)
       return token_auth
    else:
       print("Token not found")
       return ""

def get_current_session_token():
    time.sleep(1)
    token_auth = controller.get('SmartCrop_current_session_token')
    if token_auth:
       print("Token found:", token_auth)
       return token_auth
    else:
       print("Token not found")
       return ""

def get_cookie():
    token_auth = controller.get('SmartCrop_current_session_token')
    if token_auth:
       print("Token found:", token_auth)
       return token_auth
    else:
        token_auth = controller.get('SmartCrop_auth_token')
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

def save_persistent_session_auth_token(user_id):
    controller.set("SmartCrop_auth_token", generate_token(user_id), max_age=7*86400)

def logout():
    controller.set("SmartCrop_auth_token", "", max_age=0)
    controller.set("SmartCrop_current_session_token", "", max_age=0)
    st.session_state["authenticated"] = False
    st.session_state["username"] = None

    st.write("You are correctly logged out")
    st.session_state["page"] = "sign_in"


def generate_token(user_id):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    payload = {
        "user_id": user_id,
        "exp": expiration_time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def validate_token(token):
    from db_utils import check_id_in_db
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
        print("id user in validate_token: ", user_id)
        if check_id_in_db(user_id):
            return True
        else:
            return False
    except jwt.ExpiredSignatureError:
        print("The token is expired")
        return False
    except jwt.InvalidTokenError:
        print("Token not valid")
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

