// Access the video element
const video = document.getElementById('webcam');
const startButton = document.getElementById('startRecognition');
const statusText = document.getElementById('status');

// Access the webcam and stream it to the video element
async function startWebcam() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (error) {
        console.error("Error accessing webcam: ", error);
        statusText.textContent = "Failed to access webcam.";
    }
}

// Convert video frame to image data
function captureFrame() {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/jpeg');
}

// Send frame to server for recognition
async function sendFrame() {
    const frameData = captureFrame();
    try {
        const response = await fetch('/process-frame', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: frameData })
        });
        const result = await response.json();
        statusText.textContent = result.message || "Face recognition in progress...";
    } catch (error) {
        console.error("Error sending frame to server: ", error);
        statusText.textContent = "Failed to process frame.";
    }
}

// Start face recognition process
startButton.addEventListener('click', () => {
    statusText.textContent = "Starting recognition...";
    sendFrame();
});

startWebcam();
