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
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def check_and_mem_user_credentials(username, password):
    conn = create_connection("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, hashed_password, salt FROM users WHERE username=?", (username,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        user_name, hashed_password, salt = user_data
        retrieved_salt = bytes.fromhex(salt)
        if user_data[1] == hash_password(password, retrieved_salt):
            return True
    return False


def check_username_in_db(username):
    conn = create_connection("users.db")
    cursor = conn.cursor()
    # Stampa i dati della tabella
    cursor.execute("SELECT * FROM users")  # Seleziona tutti i record
    rows = cursor.fetchall()  # Ottieni tutte le righe
    print("Contenuto della tabella 'users' in check_username_in_db:")
    for row in rows:
        print(row)
    print("\n")

    try:
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

        return result is not None
    except sqlite3.Error as e:
        print("Database error: ", e)
        return False


