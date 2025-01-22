import sqlite3
import hashlib
import os

def hash_password(password, salt):
    hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()
    return hashed_password

def create_connection(db_file):
    return sqlite3.connect(db_file)

def create_user(username, password):
    try:
        conn = create_connection("users.db")
        cursor = conn.cursor()
        salt = os.urandom(16)
        cursor.execute("INSERT INTO users (username, hashed_password, salt) VALUES (?, ?, ?)", (username, hash_password(password, salt), salt.hex()))
        conn.commit()
        conn.close()
        return True, None
    except sqlite3.IntegrityError:
        print("User already exists")
        return False
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        return False, str(e)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False, str(e)

def check_user_credentials(username, password):
    try:
        conn = create_connection("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, hashed_password, salt FROM users WHERE username=?", (username,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            user_name, hashed_password, salt = user_data
            retrieved_salt = bytes.fromhex(salt)
            if hashed_password == hash_password(password, retrieved_salt):
                return True, None
    except (sqlite3.DatabaseError, TypeError, ValueError) as e:
        print(f"An error occurred while processing the request: {e}")
        print("You probably need to initializate the database")
        return False, str(e)
    return False, None


def check_username_in_db(username):
    try:
        conn = create_connection("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        print("'user' table content in check_username_in_db:")
        for row in rows:
            print(row)
        print("\n")
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

        return result is not None
    except sqlite3.Error as e:
        print("Database error: ", e)
        return False


