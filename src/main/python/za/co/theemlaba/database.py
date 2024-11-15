# database.py
import sqlite3
from datetime import datetime

DATABASE_PATH = 'src/main/resources/Database/attendance.db'

def get_connection():
    return sqlite3.connect(DATABASE_PATH)

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_type TEXT CHECK(user_type IN ('Employee', 'Student')) NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT,
            phone_number TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create Employee table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employee (
            employee_id INTEGER PRIMARY KEY REFERENCES Users(user_id),
            position TEXT,
            department TEXT,
            start_date DATE,
            end_date DATE
        )
    ''')

    # Create Student table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Student (
            student_id INTEGER PRIMARY KEY REFERENCES Users(user_id),
            student_number TEXT NOT NULL,
            course TEXT,
            year_of_study INTEGER
        )
    ''')

    # Create Attendance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES Users(user_id),
            check_in_time TIMESTAMP,
            check_out_time TIMESTAMP,
            attendance_date DATE NOT NULL
        )
    ''')

    # Create Monthly_Hours table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Monthly_Hours (
            monthly_hours_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES Users(user_id),
            month DATE NOT NULL,
            total_hours DECIMAL(5, 2) NOT NULL,
            user_type TEXT CHECK(user_type IN ('Employee', 'Student')) NOT NULL
        )
    ''')

    # Create User_Photos table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User_Photos (
            user_id INTEGER REFERENCES Users(user_id),
            photo BLOB,
            PRIMARY KEY (user_id)
        )
    ''')

    conn.commit()
    conn.close()

def insert_example_data():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Insert example user - Employee
    cursor.execute('''
        INSERT INTO Users (user_type, first_name, last_name, email, phone_number)
        VALUES ('Employee', 'John', 'Doe', 'john.doe@example.com', '123-456-7890')
    ''')
    employee_id = cursor.lastrowid

    # Insert into Employee table
    cursor.execute('''
        INSERT INTO Employee (employee_id, position, department, start_date)
        VALUES (?, 'Software Engineer', 'Engineering', '2022-01-15')
    ''', (employee_id,))

    # Insert example user - Student
    cursor.execute('''
        INSERT INTO Users (user_type, first_name, last_name, email, phone_number)
        VALUES ('Student', 'Jane', 'Smith', 'jane.smith@example.edu', '987-654-3210')
    ''')
    student_id = cursor.lastrowid

    # Insert into Student table
    cursor.execute('''
        INSERT INTO Student (student_id, student_number, course, year_of_study)
        VALUES (?, 'S12345', 'Computer Science', 2)
    ''', (student_id,))

    # Insert example attendance data for employee
    cursor.execute('''
        INSERT INTO Attendance (user_id, check_in_time, check_out_time, attendance_date)
        VALUES (?, '2023-10-01 09:00:00', '2023-10-01 17:00:00', '2023-10-01')
    ''', (employee_id,))

    # Insert example attendance data for student
    cursor.execute('''
        INSERT INTO Attendance (user_id, check_in_time, check_out_time, attendance_date)
        VALUES (?, '2023-10-01 10:00:00', '2023-10-01 15:00:00', '2023-10-01')
    ''', (student_id,))

    # Insert example monthly hours for employee
    cursor.execute('''
        INSERT INTO Monthly_Hours (user_id, month, total_hours, user_type)
        VALUES (?, '2023-10', 160.00, 'Employee')
    ''', (employee_id,))

    # Insert example monthly hours for student
    cursor.execute('''
        INSERT INTO Monthly_Hours (user_id, month, total_hours, user_type)
        VALUES (?, '2023-10', 60.00, 'Student')
    ''', (student_id,))

    # # Add photos for employee and student from file
    # with open("King/nkosikhona_mlaba_photo.jpeg", "rb") as file:
    #     employee_photo = file.read()
    # cursor.execute('''
    #     INSERT INTO User_Photos (user_id, photo)
    #     VALUES (?, ?)
    # ''', (employee_id, employee_photo))

    with open("King/nkosikhona_mlaba_photo.jpeg", "rb") as file:
        student_photo = file.read()
    cursor.execute('''
        INSERT INTO User_Photos (user_id, photo)
        VALUES (?, ?)
    ''', (student_id, student_photo))

    conn.commit()
    conn.close()

def fetch_user_photos():
    """Fetches user_id and photo data from User_Photos table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT user_id, photo FROM User_Photos")
    records = cursor.fetchall()
    
    conn.close()
    return records

def mark_attendance(user_id, route):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().date()

    cursor.execute("SELECT attendance_id FROM Attendance WHERE user_id = ? AND attendance_date = ?", (user_id, today))
    record = cursor.fetchone()

    if record:
        if route == 'arrival':
            cursor.execute("UPDATE Attendance SET check_in_time = ? WHERE attendance_id = ?", (datetime.now(), record[0]))
        elif route == 'departure':
            cursor.execute("UPDATE Attendance SET check_out_time = ? WHERE attendance_id = ?", (datetime.now(), record[0]))
    else:
        if route == 'arrival':
            cursor.execute("INSERT INTO Attendance (user_id, check_in_time, attendance_date) VALUES (?, ?, ?)", (user_id, datetime.now(), today))

    conn.commit()
    conn.close()