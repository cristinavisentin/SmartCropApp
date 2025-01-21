import sqlite3

def create_tables():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        hashed_password TEXT NOT NULL,
        salt TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    print("Table 'users' created (if it didn't already exist).")


def add_test_user():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, hashed_password, salt) VALUES (?, ?, ?)",
                       ("admin", "h_pdw", "1234"))
        conn.commit()
        print("Test user 'admin' added.")
    except sqlite3.IntegrityError:
        print("User 'admin' already exists.")

    conn.close()


def display_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT username, hashed_password, salt FROM users")
    users = cursor.fetchall()
    if users:
        print("\nUsers in database:")
        for user in users:
            print(f"Username: {user[0]}, Hashed Password: {user[1]}, Salt: {user[2]}")
    else:
        print("No users found in database.")


    conn.close()


if __name__ == "__main__":
    create_tables()
    add_test_user()
    display_database()
    print("\nDatabase setup completed")
