# database.py
import sqlite3
from datetime import datetime

DATABASE_PATH = 'src/main/resources/Database/attendance.db'

def get_connection():
    return sqlite3.connect(DATABASE_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users ... ''')
    # Repeat for other tables as in original code
    
    conn.commit()
    conn.close()

def insert_example_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Users ...''')
    # Repeat for example data as in original code

    conn.commit()
    conn.close()
