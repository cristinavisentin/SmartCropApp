import sqlite3
import hashlib
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "users.db")

def hash_password(password, salt):
    hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()
    return hashed_password

def create_connection():
    print("db path: ", DB_FILE )
    return sqlite3.connect(DB_FILE)

def create_user(username, password):
    try:
        conn = create_connection()
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
        conn = create_connection()
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
        print("You probably need to initialize the database")
        return False, str(e)
    return False, None


def check_username_in_db(username):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

        return result is not None
    except sqlite3.Error as e:
        print("Database error: ", e)
        return False


def add_prediction_to_db(username, plant, country, hectares, prediction):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO prediction_table (username, plant, country, hectares, prediction) VALUES (?, ?, ?, ?, ?)", (username, plant, country, hectares, prediction))
        conn.commit()
        print("PREDICTION ADDED TO DATABASE: ", username, plant, country, hectares, prediction)
        conn.close()
        return True, None
    except sqlite3.IntegrityError:
        print("This prediction is already been made")
        return False
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        return False, str(e)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False, str(e)


def get_predictions_by_username(username):
    try:
        conn = sqlite3.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT plant, country, hectares, prediction
            FROM prediction_table
            WHERE username = ?
        """, (username,))
        results = cursor.fetchall()
        conn.close()
        return results
    except sqlite3.Error as e:
        print("Database error: ", e)
    return None


