from flask import Flask, render_template, Response
import cv2
import face_recognition

app = Flask(__name__)

# Initialize the video capture from the default camera
video_capture = cv2.VideoCapture(0)

def gen_frames():
    """Generate frames for the video feed with face recognition."""
    while True:
        # Capture a single frame
        success, frame = video_capture.read()
        if not success:
            break

        # Resize frame for faster processing and convert to RGB
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Draw boxes around detected faces
        for (top, right, bottom, left) in face_locations:
            # Scale back up face locations since the frame we detected on was scaled
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue  # Skip this frame if encoding fails
        frame = buffer.tobytes()

        # Use yield to stream the frame to the client
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
