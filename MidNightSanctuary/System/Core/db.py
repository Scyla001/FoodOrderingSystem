import sqlite3
import os

DB_NAME = "cafeteria.db"

def create_database():
    db_path = os.path.abspath(DB_NAME)
    if not os.path.exists(db_path):
        open(db_path, "w").close()
        print(f"Database '{DB_NAME}' created successfully.")

def get_conn():
    create_database()
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    return conn
