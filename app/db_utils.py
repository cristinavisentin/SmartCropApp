import sqlite3
import jwt
import hashlib
import os
from cookie_handler import save_persistent_session_auth_token
SECRET_KEY = "123"

def hash_password(password, salt):
    hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()
    return hashed_password

def create_connection(db_file):
    return sqlite3.connect(db_file)

def create_user(username, password):
    conn = create_connection("users.db")
    cursor = conn.cursor()
    salt = os.urandom(16)
    try:
        cursor.execute("INSERT INTO users (username, hashed_password, salt) VALUES (?, ?, ?)", (username, hash_password(password, salt), salt.hex()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        conn.close()

def check_user_credentials(username, password, stay_connected):
    conn = create_connection("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id_username, username, hashed_password, salt FROM users WHERE username=?", (username,))
    user_data = cursor.fetchone()
    print("user_data: ", user_data)

    if user_data:
        id_user, user_name, hashed_password, salt = user_data
        retrieved_salt = bytes.fromhex(salt)
        print("id_user: ", id_user, "user_name: ", user_name, ", hashed_password: ", hashed_password, ", retrieved_salt: ", retrieved_salt)
        if user_data[2] == hash_password(password, retrieved_salt):
            if stay_connected:
                save_persistent_session_auth_token(id_user)
            conn.close()
            return True
    return False


def check_id_in_db(user_id):
    try:
        with sqlite3.connect("users.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE id_username=?", (user_id,))
            user = cursor.fetchone()
            print("user found in check_id_in_db: ", user[0])
            if user is not None:
                return True
    except sqlite3.Error:
        return False


def get_username_from_db(user_id):
    try:
        conn = create_connection("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE id_username=?", (user_id,))
        user = cursor.fetchone()
        if user:
            print("user found in get_username: ", user[0])
            return user[0]
        else:
            print("No user found for user_id:", user_id)
            return ""
    except jwt.ExpiredSignatureError:
        print("Token expired")
        return ""
    except jwt.InvalidTokenError:
        print("Invalid token")
        return ""
    except Exception as e:
        print("Unexpected error:", e)
        return ""


