import sqlite3
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

def check_user_credentials(username, password, session_id):
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
            if session_id != 0:
                save_persistent_session_auth_token(id_user, session_id)
                save_session_to_db(id_user, session_id)
            conn.close()
            return True
    return False


def save_session_to_db(user_id, session_id):
    conn = create_connection("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users_sessions (user_id, session_id) VALUES (?, ?)",
        (user_id, session_id)
    )
    print("SESSION ID per ", user_id, " SALVATO IN DB: ", session_id)
    conn.commit()
    conn.close()

def check_id_in_db(user_id, session_id):
    try:
        with sqlite3.connect("users.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM users_sessions WHERE user_id = ? AND session_id = ?", (user_id, session_id)
            )
            result = cursor.fetchone()
            print("RESULT OF DATABASE QUERY: ", result)
            return result is not None
    except sqlite3.Error as e:
        print("Database error: ", e)
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
    except sqlite3.Error:
        return ""


