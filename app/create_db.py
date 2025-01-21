import sqlite3
import uuid


def create_tables():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id_username INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        salt TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users_sessions (
        user_id INTEGER NOT NULL,
        session_id TEXT NOT NULL,
        is_active INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, session_id),
        FOREIGN KEY (user_id) REFERENCES users (id_username)
    )
    """)

    conn.commit()
    conn.close()
    print("Tables 'users' and 'users_sessions' created (if they didn't already exist).")


def add_test_user():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, hashed_password, salt) VALUES (?, ?, ?)",
                       ("admin", "admin", "1234"))
        conn.commit()
        print("Test user 'admin' added.")
    except sqlite3.IntegrityError:
        print("User 'admin' already exists.")

    conn.close()


def add_test_session():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id_username FROM users WHERE username = ?", ("admin",))
    user = cursor.fetchone()

    if user:
        user_id = user[0]
        session_id = str(uuid.uuid4())  # Genera un session_id unico
        try:
            cursor.execute("INSERT INTO users_sessions (user_id, session_id) VALUES (?, ?)",
                           (user_id, session_id))
            conn.commit()
            print(f"Test session added for user_id {user_id} with session_id {session_id}.")
        except sqlite3.IntegrityError:
            print(f"Session for user_id {user_id} already exists.")
    else:
        print("No test user found. Cannot create a session.")

    conn.close()


def display_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id_username, username, hashed_password, salt FROM users")
    users = cursor.fetchall()
    if users:
        print("\nUsers in database:")
        for user in users:
            print(f"ID: {user[0]}, Username: {user[1]}, Hashed Password: {user[2]}, Salt: {user[3]}")
    else:
        print("No users found in database.")

    cursor.execute("SELECT user_id, session_id, created_at FROM users_sessions")
    sessions = cursor.fetchall()
    if sessions:
        print("\nSessions in database:")
        for session in sessions:
            print(f"User ID: {session[0]}, Session ID: {session[1]}, Created At: {session[2]}")
    else:
        print("No sessions found in database.")

    conn.close()


if __name__ == "__main__":
    create_tables()
    add_test_user()
    add_test_session()
    display_database()
    print("\nDatabase setup completed")
