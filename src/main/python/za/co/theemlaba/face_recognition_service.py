import numpy as np
import cv2
import face_recognition
from database import fetch_user_photos, get_user_count
import time

known_encodings = []
user_ids = []
initial_user_count = 0

def load_faces_from_db():
    global known_encodings, user_ids, initial_user_count
    
    records = fetch_user_photos()

    known_encodings = []
    user_ids = []
    for user_id, photo_blob in records:
        photo = np.frombuffer(photo_blob, np.uint8)
        img = cv2.imdecode(photo, cv2.IMREAD_COLOR)
        encoding = face_recognition.face_encodings(img)[0]
        known_encodings.append(encoding)
        user_ids.append(user_id)
    
    initial_user_count = len(user_ids)
    return known_encodings, user_ids

def recognize_face(frame, encodings, ids):
    global known_encodings, user_ids, initial_user_count

    if known_encodings == [] or user_ids == []:
        return None
    
    faces_cur_frame = face_recognition.face_locations(frame)
    encodes_cur_frame = face_recognition.face_encodings(frame, faces_cur_frame)

    for encode_face in encodes_cur_frame:
        matches = face_recognition.compare_faces(known_encodings, encode_face)
        face_distances = face_recognition.face_distance(known_encodings, encode_face)
        match_index = np.argmin(face_distances)

        if matches[match_index]:
            return user_ids[match_index]
    return None

def load_new_faces_from_db():
    """Append new faces and user IDs from the database."""
    global known_encodings, user_ids, initial_user_count
    
    records = fetch_user_photos()
    
    # new faces if any
    new_encodings = []
    new_user_ids = []
    
    for user_id, photo_blob in records:
        if user_id not in user_ids:
            photo = np.frombuffer(photo_blob, np.uint8)
            img = cv2.imdecode(photo, cv2.IMREAD_COLOR)
            encoding = face_recognition.face_encodings(img)[0]
            new_encodings.append(encoding)
            new_user_ids.append(user_id)
    
    known_encodings.extend(new_encodings)
    user_ids.extend(new_user_ids)
    
    initial_user_count = len(user_ids)
    return known_encodings, user_ids

def update_faces_if_new_user():
    """Checks for new users every 60 seconds and updates face recognition data."""
    global initial_user_count, known_encodings, user_ids
    while True:
        time.sleep(10)
        current_user_count = get_user_count()
        
        if current_user_count > initial_user_count:
            load_new_faces_from_db()
            initial_user_count = current_user_count
            print("New user added to facial recognition system.")