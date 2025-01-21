import sqlite3

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
print("Created 'users' table (if it didn't already exist)")
try:
    cursor.execute("INSERT INTO users (username, hashed_password, salt) VALUES (?, ?, ?)", ("admin", "admin", "1234"))
    conn.commit()
    print("test user 'admin' added")
except sqlite3.IntegrityError:
    print("'admin' user already exist")

# Includi id_username nella query
cursor.execute("SELECT id_username, username, hashed_password, salt FROM users")
users = cursor.fetchall()

if users:
    print("\nUsers in database:")
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}, Hashed Password: {user[2]}, Salt: {user[3]}")
else:
    print("No results found in database.")

conn.close()
print("\nDatabase connection closed")
