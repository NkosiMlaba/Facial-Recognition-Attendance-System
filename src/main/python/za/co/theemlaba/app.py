import cv2
from flask import Flask, render_template, Response
from face_recognition_service import load_faces_from_db, recognize_face
from database import mark_attendance

app = Flask(__name__)
video_capture = cv2.VideoCapture(0)
known_encodings, user_ids = load_faces_from_db()

def generate_frames(route):
    while True:
        success, img = video_capture.read()
        if not success:
            break

        img_small = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)
        
        user_id = recognize_face(img_small, known_encodings, user_ids)
        
        if user_id:
            mark_attendance(user_id, route)
            cv2.putText(img, f'User {user_id} marked', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

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