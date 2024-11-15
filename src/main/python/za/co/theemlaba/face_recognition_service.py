# face_recognition_service.py
import numpy as np
import cv2
import face_recognition
from database import get_connection

def load_faces_from_db():
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

def recognize_face(frame, known_encodings, user_ids):
    faces_cur_frame = face_recognition.face_locations(frame)
    encodes_cur_frame = face_recognition.face_encodings(frame, faces_cur_frame)

    for encode_face in encodes_cur_frame:
        matches = face_recognition.compare_faces(known_encodings, encode_face)
        face_distances = face_recognition.face_distance(known_encodings, encode_face)
        match_index = np.argmin(face_distances)

        if matches[match_index]:
            return user_ids[match_index]
    return None
