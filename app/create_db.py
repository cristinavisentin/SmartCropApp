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

    # Creazione della tabella delle previsioni associata agli utenti
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prediction_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        plant TEXT NOT NULL,
        country TEXT NOT NULL,
        hectares INTEGER NOT NULL,
        prediction REAL NOT NULL,
        FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()
    print("Tables 'users' and 'prediction_table' created (if they didn't already exist).")

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

def add_test_prediction():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO prediction_table (username, plant, country, hectares, prediction) VALUES (?, ?, ?, ?, ?)",
                       ("admin", "Wheat", "Italy", 2.5, 300.0))
        conn.commit()
        print("Test prediction added for user 'admin'.")
    except sqlite3.IntegrityError as e:
        print(f"Error adding test prediction: {e}")

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

    cursor.execute("SELECT id, username, plant, country, hectares, prediction FROM prediction_table")
    predictions = cursor.fetchall()
    if predictions:
        print("\nPredictions in database:")
        for prediction in predictions:
            print(f"ID: {prediction[0]}, Username: {prediction[1]}, Plant: {prediction[2]}, Country: {prediction[3]}, Hectares: {prediction[4]}, Prediction: {prediction[5]} grams")
    else:
        print("No predictions found in database.")

    conn.close()


if __name__ == "__main__":
    create_tables()
    add_test_user()
    add_test_prediction()
    display_database()
    print("\nDatabase setup completed.")