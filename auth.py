# auth.py
import sqlite3
import hashlib

DB_PATH = "inventory.db"

def create_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        return True, "User created successfully!"
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
    user = cursor.fetchone()
    conn.close()
    return (True, "Login successful!") if user else (False, "Invalid username or password.")
