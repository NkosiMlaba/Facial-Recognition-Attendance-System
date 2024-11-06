import cv2
import face_recognition
import os
import numpy as np
from flask import Flask, jsonify
from datetime import datetime
import logging

# Initialize the Flask app and logging
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Path to images directory
IMAGE_PATH = 'images'
ENCODINGS = []
CLASS_NAMES = []

# Load and encode known images
def load_known_faces():
    images = []
    classNames = []
    myList = os.listdir(IMAGE_PATH)
    logging.info(f"Images found for encoding: {myList}")
    
    for cl in myList:
        curImg = cv2.imread(f'{IMAGE_PATH}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    
    global ENCODINGS, CLASS_NAMES
    ENCODINGS = find_encodings(images)
    CLASS_NAMES = classNames
    logging.info("Encoding complete")

def find_encodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except IndexError:
            logging.warning("No face found in one of the images; skipping.")
    return encodeList

def mark_attendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.split(',')[0] for line in myDataList]
        
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
            logging.info(f"Marked attendance for {name} at {dtString}")

# Main function to capture video and process frames
def run_face_recognition():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logging.error("Failed to open camera.")
        return "Camera initialization error"

    while True:
        success, img = cap.read()
        if not success:
            logging.error("Failed to capture frame.")
            break

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(ENCODINGS, encodeFace)
            faceDis = face_recognition.face_distance(ENCODINGS, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = CLASS_NAMES[matchIndex].upper()
                logging.info(f"Face matched with {name}")
                
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                mark_attendance(name)

        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return "Face recognition completed"

# Flask route to start face recognition
@app.route('/start-recognition', methods=['GET'])
def start_recognition():
    try:
        result = run_face_recognition()
        return jsonify({"status": "success", "result": result})
    except Exception as e:
        logging.exception("Error processing frame:")
        return jsonify({"status": "error", "message": "Failed to process frame."}), 500

# Load encodings and start Flask app
if __name__ == "__main__":
    load_known_faces()
    app.run(port=5000)
