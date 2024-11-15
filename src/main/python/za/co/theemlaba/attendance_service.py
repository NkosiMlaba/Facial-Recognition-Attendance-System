# attendance_service.py
from datetime import datetime
from database import get_connection

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
