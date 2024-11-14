import cv2
import numpy as np
import face_recognition
import sqlite3
from datetime import datetime
from flask import Flask, render_template, Response, redirect, url_for

app = Flask(__name__)
video_capture = cv2.VideoCapture(0)

# Connect to SQLite database
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
    employee_id = cursor.lastrowid  # Get the generated user_id for the employee

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
    student_id = cursor.lastrowid  # Get the generated user_id for the student

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

# Load and encode faces from the database
def load_faces_from_db():
    init_db()
    insert_example_data()
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, photo FROM User_Photos")
    records = cursor.fetchall()
    conn.close()

    known_encodings = []
    user_ids = []
    for user_id, photo_blob in records:
        photo = np.frombuffer(photo_blob, np.uint8)
        img = cv2.imdecode(photo, cv2.IMREAD_COLOR)
        encoding = face_recognition.face_encodings(img)[0]
        known_encodings.append(encoding)
        user_ids.append(user_id)
    return known_encodings, user_ids

known_encodings, user_ids = load_faces_from_db()

# Mark attendance in the database
def mark_attendance(user_id, route):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().date()

    cursor.execute("SELECT attendance_id FROM Attendance WHERE user_id = ? AND attendance_date = ?", (user_id, today))
    record = cursor.fetchone()

    if record:
        # If an attendance record exists, update it based on the route
        if route == 'arrival':
            cursor.execute("UPDATE Attendance SET check_in_time = ? WHERE attendance_id = ?", (datetime.now(), record[0]))
        elif route == 'departure':
            cursor.execute("UPDATE Attendance SET check_out_time = ? WHERE attendance_id = ?", (datetime.now(), record[0]))
    else:
        # If no attendance record exists, insert a new one
        if route == 'arrival':
            cursor.execute("INSERT INTO Attendance (user_id, check_in_time, attendance_date) VALUES (?, ?, ?)", (user_id, datetime.now(), today))

    conn.commit()
    conn.close()

# Face recognition process
def recognize_face(frame):
    faces_cur_frame = face_recognition.face_locations(frame)
    encodes_cur_frame = face_recognition.face_encodings(frame, faces_cur_frame)

    for encode_face in encodes_cur_frame:
        matches = face_recognition.compare_faces(known_encodings, encode_face)
        face_distances = face_recognition.face_distance(known_encodings, encode_face)
        match_index = np.argmin(face_distances)

        if matches[match_index]:
            return user_ids[match_index]
    return None

def generate_frames(route):
    while True:
        success, img = video_capture.read()
        if not success:
            break

        img_small = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)
        
        user_id = recognize_face(img_small)
        
        if user_id:
            mark_attendance(user_id, route)
            cv2.putText(img, f'User {user_id} marked', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/arrival')
def arrival():
    return render_template('arrival.html')

@app.route('/departure')
def departure():
    return render_template('departure.html')

@app.route('/video_feed_arrival')
def video_feed_arrival():
    return Response(generate_frames('arrival'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_departure')
def video_feed_departure():
    return Response(generate_frames('departure'), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
