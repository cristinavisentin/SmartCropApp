import sqlite3
import jwt
import datetime
import hashlib
import os

SECRET_KEY = "123"
user_name = "nullo"

print("username in db_utils: ", user_name)
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

def check_user_credentials(username, password):
    conn = create_connection("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT hashed_password, salt FROM users WHERE username=?", (username,))
    user_data = cursor.fetchone()

    if user_data:
        hashed_password, salt = user_data
        retrieved_salt = bytes.fromhex(salt)
        if user_data[0] == hash_password(password, retrieved_salt):
            conn.close()
            return True
    return False


def generate_token(username):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    payload = {
        "username": username,
        "exp": expiration_time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def validate_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        global user_name
        user_name = payload["username"]
        print("username in validate_token: ", user_name)
        conn = create_connection("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username=?", (user_name,))
        user = cursor.fetchone()
        if user:
            print(f"Token valid for the user: {user_name}")
            return True
        else:
            print("Username not found in database")
            return False
    except jwt.ExpiredSignatureError:
        print("The token is expired")
        return False
    except jwt.InvalidTokenError:
        print("Token not valid")
        return False